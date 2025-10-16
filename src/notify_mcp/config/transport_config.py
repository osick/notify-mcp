"""Transport configuration for notify-mcp server."""

from typing import Literal

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class TransportSettings(BaseSettings):
    """Transport configuration settings.

    Attributes:
        transport_type: Type of transport to use (stdio or http)
        http_host: Host address for HTTP server (default: 0.0.0.0)
        http_port: Port for HTTP server (default: 8000)
    """

    model_config = ConfigDict(
        env_prefix="NOTIFY_MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    transport_type: Literal["stdio", "http"] = "stdio"
    http_host: str = "0.0.0.0"
    http_port: int = 8000
