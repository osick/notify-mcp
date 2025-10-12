"""Storage configuration using Pydantic Settings.

This module provides configuration for persistent storage backends,
allowing configuration via environment variables or .env files.

Environment Variables:
    NOTIFY_MCP_STORAGE_TYPE: Type of storage backend (memory, sqlite, postgresql)
    NOTIFY_MCP_SQLITE_PATH: Path to SQLite database file
    NOTIFY_MCP_POSTGRESQL_URL: PostgreSQL connection URL
    NOTIFY_MCP_MAX_HISTORY: Maximum notifications per channel (for LRU cache)

Example .env file:
    NOTIFY_MCP_STORAGE_TYPE=sqlite
    NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db
    NOTIFY_MCP_MAX_HISTORY=1000
"""

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    """Configuration for storage backends.

    Attributes:
        storage_type: Type of storage backend to use
        sqlite_path: Path to SQLite database file (used when storage_type='sqlite')
        postgresql_url: PostgreSQL connection URL (used when storage_type='postgresql')
        max_history: Maximum number of notifications to keep per channel (LRU cache)
    """

    model_config = SettingsConfigDict(
        env_prefix="NOTIFY_MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    storage_type: Literal["memory", "sqlite", "postgresql"] = Field(
        default="memory",
        description="Type of storage backend to use",
    )

    sqlite_path: str = Field(
        default="~/.notify-mcp/storage.db",
        description="Path to SQLite database file",
    )

    postgresql_url: str | None = Field(
        default=None,
        description="PostgreSQL connection URL (e.g., postgresql+asyncpg://user:pass@host/db)",
    )

    max_history: int = Field(
        default=1000,
        ge=1,
        description="Maximum notifications per channel (LRU cache)",
    )

    @field_validator("sqlite_path")
    @classmethod
    def expand_sqlite_path(cls, v: str) -> str:
        """Expand ~ and environment variables in SQLite path."""
        return str(Path(v).expanduser())

    @field_validator("postgresql_url")
    @classmethod
    def validate_postgresql_url(cls, v: str | None) -> str | None:
        """Validate PostgreSQL URL format."""
        if v is not None and not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError(
                "PostgreSQL URL must start with 'postgresql://' or 'postgresql+asyncpg://'"
            )
        return v

    def validate_configuration(self) -> None:
        """Validate that required configuration is present for selected storage type.

        Raises:
            ValueError: If configuration is invalid for selected storage type
        """
        if self.storage_type == "postgresql" and self.postgresql_url is None:
            raise ValueError(
                "postgresql_url must be set when storage_type is 'postgresql'"
            )
