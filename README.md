# Notify-MCP

**A Pub-Sub MCP server for seamless team collaboration across AI platforms** 🤖

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io/)
[![Tests](https://img.shields.io/badge/tests-48%20passing-brightgreen.svg)](./tests/)
[![Coverage](https://img.shields.io/badge/coverage-64%25-yellow.svg)](./tests/)

---

## Overview

Notify-MCP enables **teams to share notifications, decisions, and status updates** across different AI assistants (Claude, ChatGPT, Gemini). It implements a flexible pub-sub architecture where team members can:

- 📢 **Broadcast** architecture decisions to all stakeholders
- 🚨 **Alert** teams about critical incidents
- 📊 **Share** project status and updates
- 🔔 **Subscribe** to relevant channels with smart filters
- 🤝 **Coordinate** work across different AI platforms

### Use Cases

- **Development Teams**: Share technical decisions, code reviews, deployment status
- **Consulting Teams**: Coordinate client updates, project milestones, recommendations
- **Business Teams**: Broadcast strategic decisions, requirement changes, priorities
- **Cross-functional**: Maintain shared context across teams and AI assistants

---

## Features

### Core Capabilities

- 📢 **Multi-Channel System**: Create dedicated channels for teams, projects, or topics
- 🎯 **Smart Filtering**: Subscribe with filters (priority, tags, themes, sender roles)
- 🔔 **Pub-Sub Architecture**: Decoupled notification delivery via channels
- 📚 **Notification History**: Retrieve recent notifications (last 50 per channel)
- 🔐 **Type-Safe**: Full Pydantic validation with JSON Schema
- 🧪 **Well-Tested**: 48 unit tests with 64% code coverage

### MCP Protocol Support

- **6 Tools**: publish, subscribe, unsubscribe, list channels, create channel, get subscriptions
- **3 Resources**: notification history, channel info, notification schema
- **2 Prompts**: Architecture decision and alert templates
- **Transport**: stdio (Phase 1), HTTP planned (Phase 2)

### Notification Schema

Rich notification model with:
- **Sender info**: User ID, name, role, AI tool
- **Context**: Theme, priority (low/medium/high/critical), tags
- **Information**: Title, body (text/markdown/json), format
- **Metadata**: ID, timestamp, channel, sequence, threading
- **Actions**: Optional action buttons
- **Visibility**: Expiry, allowed users, read receipts

---

## Installation

### Prerequisites

- **Python 3.11+**
- **uv** (fast Python package manager)

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install Notify-MCP

```bash
# Clone the repository
git clone <repository-url>
cd notify-mcp

# Install dependencies
uv sync

# Verify installation
uv run python -m notify_mcp --help
```

---

## Configuration

### Claude Desktop / Claude Code

**File**: `~/.config/Claude/claude_desktop_config.json` (macOS/Linux) or `%APPDATA%/Claude/claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "notify_mcp"],
      "cwd": "/absolute/path/to/notify-mcp",
      "env": {
        "NOTIFY_MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Alternative** (with activated venv):
```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "/absolute/path/to/notify-mcp/.venv/bin/python",
      "args": ["-m", "notify_mcp"]
    }
  }
}
```

**Restart Claude** after updating the config file.

#### Using Slash Commands in Claude Code

Six convenient slash commands are available in `.claude/commands/`:

- `/notify-decision` - Create architecture decision notification
- `/notify-alert` - Create critical alert
- `/notify-status` - Share status update
- `/notify-channels` - List all channels
- `/notify-subscribe` - Subscribe to a channel
- `/notify-recent` - View recent notifications

### ChatGPT (via MCP)

ChatGPT supports MCP through custom integrations. Two options:

#### Option 1: Using MCP Bridge (Recommended)

Use an MCP-to-HTTP bridge to connect ChatGPT:

1. **Run notify-mcp server** (stdio):
   ```bash
   uv run python -m notify_mcp
   ```

2. **Use MCP bridge** (e.g., [mcp-bridge](https://github.com/example/mcp-bridge)):
   ```bash
   mcp-bridge --stdio "uv run python -m notify_mcp" --http localhost:8080
   ```

3. **Configure ChatGPT Custom GPT**:
   - Create a Custom GPT
   - Add "notify-mcp" action
   - Point to bridge endpoint: `http://localhost:8080`
   - Import OpenAPI spec from bridge

#### Option 2: Direct Integration (Future)

When OpenAI adds native MCP support, configuration will be similar to Claude:

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "notify_mcp"],
      "cwd": "/absolute/path/to/notify-mcp"
    }
  }
}
```

**Note**: As of January 2025, ChatGPT doesn't have native MCP support yet. Monitor OpenAI announcements.

### Google Gemini (via MCP)

Gemini MCP integration is in development. Two approaches:

#### Option 1: Via Google AI Studio (Future)

When Gemini adds MCP support:

1. **Open Google AI Studio**
2. **Go to Extensions → MCP Servers**
3. **Add Server**:
   ```json
   {
     "name": "notify-mcp",
     "command": "uv",
     "args": ["run", "python", "-m", "notify_mcp"],
     "workingDirectory": "/absolute/path/to/notify-mcp"
   }
   ```

#### Option 2: Using Gemini API with MCP Adapter

Use Gemini API with an MCP adapter (Python):

```python
# example_gemini_client.py
from google.generativeai import GenerativeModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Connect to notify-mcp
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "notify_mcp"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Use Gemini with MCP tools
            model = GenerativeModel('gemini-pro')
            # ... integrate MCP tools with Gemini calls
```

**Note**: Full Gemini MCP integration expected in 2025. Check [Gemini documentation](https://ai.google.dev/) for updates.

---

## Quick Start

### 1. Create a Channel

```python
# Using MCP tool in Claude/ChatGPT/Gemini
"Create a channel called 'engineering' for technical updates"
```

Or programmatically:

```python
await session.call_tool(
    "create_channel",
    arguments={
        "channel_id": "engineering",
        "name": "Engineering Team",
        "description": "Technical updates and decisions"
    }
)
```

### 2. Subscribe to Channel

```python
# Subscribe with priority filter
await session.call_tool(
    "subscribe_to_channel",
    arguments={
        "channel": "engineering",
        "priority_filter": ["high", "critical"]
    }
)
```

### 3. Publish Notification

```python
await session.call_tool(
    "publish_notification",
    arguments={
        "channel": "engineering",
        "title": "API v2.0 Released",
        "body": "New API version deployed to production",
        "priority": "high",
        "theme": "state-update",
        "tags": ["api", "release"]
    }
)
```

### 4. Retrieve Notifications

```python
notifications = await session.read_resource(
    uri="notification://engineering/recent"
)
```

---

## Usage Examples

### Example 1: Architecture Decision

```bash
# In Claude Code
/notify-decision

# Claude will ask for:
# - Decision title: "Migration to Microservices"
# - Context: "Monolith becoming hard to scale..."
# - Decision: "Move to microservices architecture using Docker/K8s"

# Notification published to 'engineering' channel with theme='architecture-decision'
```

### Example 2: Critical Alert

```bash
# In any AI assistant with notify-mcp
"Send a critical alert about database connection pool exhaustion"

# Uses publish_notification tool:
# - channel: "alerts"
# - priority: "critical"
# - theme: "alert"
```

### Example 3: Cross-Team Coordination

**Developer in Claude**:
```
Subscribe to architecture channel with high priority filter
```

**Architect in ChatGPT**:
```
Publish architecture decision about new caching strategy to engineering channel
```

**Developer in Claude**:
```
Show me recent notifications from architecture channel
```

**Result**: Developer sees architect's decision even though they're using different AI platforms! 🎉

---

## MCP Tools Reference

### publish_notification

Publish a notification to a channel.

**Arguments**:
- `channel` (string, required): Channel name
- `title` (string, required): Notification title
- `body` (string, required): Notification body
- `priority` (string): "low" | "medium" | "high" | "critical" (default: "medium")
- `theme` (string): "info" | "state-update" | "alert" | "architecture-decision" | "question" | "decision" | "memory-sync" | "discussion" (default: "info")
- `tags` (array): List of tags (default: [])

**Returns**: Confirmation with notification ID and delivery stats

### subscribe_to_channel

Subscribe to a channel with optional filters.

**Arguments**:
- `channel` (string, required): Channel name
- `priority_filter` (array): Only receive notifications with these priorities
- `tag_filter` (array): Only receive notifications with these tags

**Returns**: Subscription ID and filter details

### unsubscribe_from_channel

Unsubscribe from a channel.

**Arguments**:
- `channel` (string, required): Channel name

**Returns**: Success/failure status

### list_channels

List all available channels.

**Returns**: List of channels with subscriber/notification counts

### create_channel

Create a new notification channel.

**Arguments**:
- `channel_id` (string, required): Unique channel ID
- `name` (string, required): Channel name
- `description` (string): Channel description

**Returns**: Confirmation with channel details

### get_my_subscriptions

Get current subscriptions.

**Returns**: List of subscriptions with filters and timestamps

---

## MCP Resources Reference

### notification://<channel>/recent

Retrieve last 50 notifications from a channel.

**Example**: `notification://engineering/recent`

**Returns**: JSON array of notifications

### channel://<channel>/info

Get channel information and statistics.

**Example**: `channel://engineering/info`

**Returns**: Channel details with subscriber/notification counts

### schema://notification

Get the notification JSON schema.

**Example**: `schema://notification`

**Returns**: Complete JSON Schema for notifications

---

## Architecture

```
notify-mcp/
├── src/notify_mcp/
│   ├── server.py           # Main MCP server
│   ├── models/             # Pydantic models (Notification, Channel, Subscription)
│   ├── core/               # Business logic
│   │   ├── channel_manager.py        # Channel CRUD
│   │   ├── subscription_manager.py   # Subscription management
│   │   ├── notification_router.py    # Routing & filtering
│   │   └── notification_validator.py # JSON Schema validation
│   ├── storage/            # Storage implementations
│   │   └── memory.py       # In-memory storage (Phase 1)
│   └── utils/              # Filter matching, helpers
├── schemas/                # JSON Schemas
├── tests/                  # Unit tests (48 tests, 64% coverage)
├── examples/               # Example clients
└── docs/                   # Documentation
```

### Storage

**Phase 1 (Current)**: In-memory storage
- Fast (no I/O overhead)
- Suitable for 100-1000 concurrent clients
- Notifications persist during server lifetime
- LRU cache (max 1000 notifications per channel)

**Phase 2 (Planned)**: Redis Pub/Sub
- Persistent storage
- Multi-server support
- Scalable to 10,000+ clients

---

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/notify_mcp --cov-report=html

# Run specific test file
uv run pytest tests/test_storage.py -v
```

### Type Checking

```bash
uv run mypy src/notify_mcp
```

### Linting

```bash
uv run ruff check src/
uv run ruff format src/
```

### Running Examples

```bash
# Basic client example
python examples/basic_client.py

# Team workflow example
python examples/team_workflow.py
```

See `examples/README.md` for detailed usage.

---

## Testing

- **48 unit tests** covering core functionality
- **64% code coverage** (85-100% for business logic)
- **Test categories**:
  - Model validation (Pydantic schemas)
  - Storage operations (CRUD)
  - Filter matching (priority, tags, themes)
  - Subscription management
  - Notification routing
  - Channel management

---

## Roadmap

### Phase 1: MVP ✅ (Complete)
- ✅ stdio transport
- ✅ In-memory storage
- ✅ 6 MCP tools
- ✅ 3 MCP resources
- ✅ Smart filtering
- ✅ 48 unit tests

### Phase 2: Scaling (Planned)
- [ ] HTTP transport
- [ ] Redis Pub/Sub integration
- [ ] Persistent storage
- [ ] Multi-server support
- [ ] Rate limiting
- [ ] Permission enforcement

### Phase 3: Advanced Features (Future)
- [ ] Notification threading (replyTo)
- [ ] Read receipts
- [ ] Notification expiry
- [ ] Webhook delivery
- [ ] Integration with Slack/Discord
- [ ] Web dashboard

---

## Troubleshooting

### Server Not Starting

**Problem**: Server fails to start or Claude can't find it.

**Solution**:
```bash
# Test server manually
uv run python -m notify_mcp

# Check if uv is in PATH
which uv

# Use absolute paths in config
"command": "/full/path/to/uv"
```

### Notifications Not Appearing

**Problem**: Published notifications don't show up.

**Reason**: In stdio mode, notifications are stored but not pushed. You must retrieve them.

**Solution**:
```
# Retrieve notifications via resource
"Show me recent notifications from engineering channel"
```

### Filter Not Working

**Problem**: Subscribed with filter but still see unwanted notifications.

**Solution**: Filters apply when **retrieving** notifications, not at storage time. When you read `notification://<channel>/recent`, only matching notifications are shown based on your subscription filters.

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'mcp'`

**Solution**:
```bash
# Install MCP SDK
pip install mcp

# Or use uv
uv pip install mcp
```

---

## Documentation

- **[API Documentation](docs/API.md)**: Complete MCP API reference
- **[Notification Schema](docs/NOTIFICATION_SCHEMA.md)**: Schema specification
- **[Architecture](docs/ARCHITECTURE.md)**: System design
- **[Usage Guide](docs/USAGE_GUIDE.md)**: Detailed usage scenarios
- **[Examples](examples/README.md)**: Code examples

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `uv run pytest`
5. Run linting: `uv run ruff check src/`
6. Submit a pull request

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/notify-mcp/issues)
- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)

---

## Acknowledgments

- Built with [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) by Anthropic
- Uses [Pydantic](https://docs.pydantic.dev/) for data validation
- Package management by [uv](https://github.com/astral-sh/uv)

---

**Made with ❤️ for seamless AI collaboration**
