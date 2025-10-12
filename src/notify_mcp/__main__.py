"""CLI entry point for notify-mcp."""

import asyncio
import logging
import sys

from .server import NotifyMCPServer


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,  # Log to stderr to keep stdout clean for MCP protocol
    )


async def main() -> None:
    """Main entry point."""
    setup_logging()

    server = NotifyMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
