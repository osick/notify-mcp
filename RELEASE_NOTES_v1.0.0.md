# notify-mcp v1.0.0 - Phase 1 MVP

First stable release of notify-mcp, an MCP server for intelligent notification management and cross-team coordination.

## Features

### MCP Tools (6)
- **publish_notification** - Publish notifications to channels with priority, tags, and themes
- **subscribe_to_channel** - Subscribe with smart filtering (priority, tags, theme, role)
- **unsubscribe_from_channel** - Unsubscribe from channels
- **list_channels** - View all available channels with stats
- **create_channel** - Create new notification channels
- **get_subscriptions** - View active subscriptions

### MCP Resources (3)
- **notification://<channel>/recent** - Retrieve recent notifications from a channel
- **channel://<channel>/info** - Get channel metadata and statistics
- **schema://notification** - Access the notification JSON schema

### Platform Support
- **Claude Desktop/Code** - Native MCP support with comprehensive setup instructions
- **ChatGPT** - MCP bridge integration (with future native support)
- **Gemini** - Python API adapter approach (with future Google AI Studio support)

### Development Quality
- 48 unit tests passing
- 64% code coverage
- Type checking with mypy
- Linting with ruff
- Comprehensive documentation

### Documentation & Examples
- Complete README with multi-platform setup
- Basic client example (`examples/basic_client.py`)
- Team workflow example (`examples/team_workflow.py`)
- 6 Claude Code slash commands for quick access
- Troubleshooting guide

### Storage
- In-memory storage with LRU caching (max 1000 notifications per channel)
- Persistent storage planned for Phase 2

## Bug Fixes
- Fixed JSON schema validation with optional fields
- Fixed AnyUrl object handling in resource readers
- Fixed notification delivery messaging for stdio mode
- Added `exclude_none=True` to all model serialization

## Requirements
- Python 3.11+
- uv package manager (recommended)
- MCP-compatible AI assistant (Claude, ChatGPT with bridge, or Gemini with adapter)

## Installation

```bash
git clone https://github.com/yourusername/notify-mcp.git
cd notify-mcp
uv sync
```

See the [README](README.md) for detailed setup instructions for your platform.

## What's Next?
Phase 2 will add persistent storage (SQLite/PostgreSQL), notification history, and enhanced filtering capabilities.
