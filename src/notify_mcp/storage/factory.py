"""Storage factory for creating storage instances based on configuration.

This module provides a factory function that creates the appropriate storage
backend based on the provided configuration settings.
"""

import logging
from pathlib import Path

from ..config.storage_config import StorageSettings
from ..core.storage_adapter import StorageAdapter
from .memory import InMemoryStorage

logger = logging.getLogger(__name__)


async def create_storage(settings: StorageSettings) -> StorageAdapter:
    """Create a storage instance based on configuration settings.

    Args:
        settings: Storage configuration settings

    Returns:
        Initialized storage adapter instance

    Raises:
        ValueError: If storage type is not supported or configuration is invalid
        RuntimeError: If storage initialization fails
    """
    # Validate configuration
    settings.validate_configuration()

    logger.info(f"Initializing storage: type={settings.storage_type}")

    if settings.storage_type == "memory":
        logger.info(f"Creating in-memory storage (max_history={settings.max_history})")
        return InMemoryStorage(max_history_per_channel=settings.max_history)

    elif settings.storage_type == "sqlite":
        # Import here to avoid dependency issues
        try:
            from .sqlite_storage import SQLiteStorage
        except ImportError as e:
            raise RuntimeError(
                "SQLite storage requires 'sqlalchemy[asyncio]' and 'aiosqlite' packages"
            ) from e

        # Ensure parent directory exists
        db_path = Path(settings.sqlite_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Creating SQLite storage: path={settings.sqlite_path}")
        storage = SQLiteStorage(
            db_path=settings.sqlite_path,
            max_history_per_channel=settings.max_history,
        )

        # Initialize database schema
        await storage.initialize()
        logger.info("SQLite storage initialized successfully")
        return storage

    elif settings.storage_type == "postgresql":
        # Import here to avoid dependency issues
        try:
            from .postgres_storage import PostgreSQLStorage
        except ImportError as e:
            raise RuntimeError(
                "PostgreSQL storage requires 'sqlalchemy[asyncio]' and 'asyncpg' packages. "
                "This feature is available in the Enterprise Edition."
            ) from e

        if settings.postgresql_url is None:
            raise ValueError("postgresql_url must be set when storage_type is 'postgresql'")

        logger.info("Creating PostgreSQL storage (Enterprise Edition)")
        storage = PostgreSQLStorage(
            connection_url=settings.postgresql_url,
            max_history_per_channel=settings.max_history,
        )

        # Initialize database schema
        await storage.initialize()
        logger.info("PostgreSQL storage initialized successfully")
        return storage

    else:
        raise ValueError(
            f"Unsupported storage type: {settings.storage_type}. "
            f"Supported types: memory, sqlite, postgresql"
        )


async def close_storage(storage: StorageAdapter) -> None:
    """Close storage and cleanup resources.

    Args:
        storage: Storage adapter instance to close
    """
    # Check if storage has a close method
    if hasattr(storage, "close"):
        logger.info(f"Closing storage: {type(storage).__name__}")
        await storage.close()
    else:
        logger.debug(f"Storage {type(storage).__name__} does not require cleanup")
