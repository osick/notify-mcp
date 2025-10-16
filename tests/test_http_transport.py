"""Tests for HTTP transport functionality."""

import asyncio

import pytest

from notify_mcp.config.transport_config import TransportSettings
from notify_mcp.server import NotifyMCPServer


class TestHTTPTransport:
    """Test HTTP transport configuration and initialization."""

    def test_transport_config_defaults(self):
        """Test default transport configuration."""
        settings = TransportSettings()
        assert settings.transport_type == "stdio"
        assert settings.http_host == "0.0.0.0"
        assert settings.http_port == 8000

    def test_transport_config_from_env(self, monkeypatch):
        """Test transport configuration from environment variables."""
        monkeypatch.setenv("NOTIFY_MCP_TRANSPORT_TYPE", "http")
        monkeypatch.setenv("NOTIFY_MCP_HTTP_HOST", "127.0.0.1")
        monkeypatch.setenv("NOTIFY_MCP_HTTP_PORT", "3000")

        settings = TransportSettings()
        assert settings.transport_type == "http"
        assert settings.http_host == "127.0.0.1"
        assert settings.http_port == 3000

    def test_server_has_http_methods(self):
        """Test server has HTTP transport methods."""
        server = NotifyMCPServer()
        assert hasattr(server, "run_http")
        assert hasattr(server, "run_stdio")
        assert hasattr(server, "run")

    def test_server_multi_client_tracking(self):
        """Test server has multi-client tracking attributes."""
        server = NotifyMCPServer()
        assert hasattr(server, "active_clients")
        assert hasattr(server, "_client_context")
        assert isinstance(server.active_clients, dict)
        assert len(server.active_clients) == 0

    def test_current_client_id_property(self):
        """Test current_client_id property defaults to stdio-client."""
        server = NotifyMCPServer()
        assert server.current_client_id == "stdio-client"

        # Test with custom context
        server._client_context = "test-client-123"
        assert server.current_client_id == "test-client-123"

    @pytest.mark.asyncio
    async def test_http_server_initialization(self):
        """Test HTTP server can be initialized without errors."""
        server = NotifyMCPServer()

        # Test that initialization methods exist and are callable
        await server._initialize_server()

        # Verify components are initialized
        assert server.storage is not None
        assert server.subscription_manager is not None
        assert server.channel_manager is not None
        assert server.router is not None

        # Cleanup
        await server._shutdown_server()

    def test_http_transport_imports(self):
        """Test that HTTP transport dependencies can be imported."""
        try:
            from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

            assert StreamableHTTPSessionManager is not None
        except ImportError as e:
            pytest.fail(f"Failed to import HTTP transport dependencies: {e}")

        try:
            import uvicorn
            from starlette.applications import Starlette
            from starlette.routing import Route

            assert uvicorn is not None
            assert Starlette is not None
            assert Route is not None
        except ImportError as e:
            pytest.fail(f"Failed to import HTTP server dependencies: {e}")
