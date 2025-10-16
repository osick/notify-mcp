#!/usr/bin/env python
"""Example: Run notify-mcp server with HTTP transport.

This example demonstrates how to run the notify-mcp server with HTTP transport,
allowing multiple clients to connect remotely.

Usage:
    # Default (0.0.0.0:8000)
    python examples/run_http_server.py

    # Custom host/port
    NOTIFY_MCP_HTTP_HOST=127.0.0.1 NOTIFY_MCP_HTTP_PORT=3000 python examples/run_http_server.py

    # Or set transport via environment
    NOTIFY_MCP_TRANSPORT_TYPE=http python examples/run_http_server.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from notify_mcp.server import NotifyMCPServer


async def main():
    """Run HTTP server."""
    server = NotifyMCPServer()

    print("Starting Notify-MCP HTTP server...")
    print("- Transport: HTTP")
    print("- Endpoint: http://0.0.0.0:8000/mcp")
    print("- Press Ctrl+C to stop")
    print()

    try:
        # Run with HTTP transport (reads config from environment)
        await server.run(transport="http")
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    asyncio.run(main())
