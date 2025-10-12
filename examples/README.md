# Notify-MCP Examples

This directory contains example client scripts demonstrating how to use the notify-mcp server.

## Prerequisites

1. **Install the MCP Python SDK:**
   ```bash
   pip install mcp
   ```

2. **Make sure notify-mcp server is accessible:**
   ```bash
   cd /path/to/notify-mcp
   uv sync
   ```

## Examples

### 1. basic_client.py

A simple example demonstrating core functionality:
- Creating channels
- Subscribing to channels with filters
- Publishing notifications
- Retrieving notification history
- Managing subscriptions

**Run it:**
```bash
python examples/basic_client.py
```

**What you'll learn:**
- How to connect to notify-mcp via stdio
- Basic MCP tool calls (create_channel, subscribe, publish, etc.)
- How to use priority filters
- How to retrieve notifications via resources
- Complete subscribe → publish → retrieve workflow

### 2. team_workflow.py

A realistic team collaboration scenario demonstrating:
- Multi-channel setup for different teams (dev, consulting, business)
- Role-specific subscriptions with filters
- Architecture decision broadcasting
- Critical alert handling
- Status updates and requirement changes
- Cross-team coordination

**Run it:**
```bash
python examples/team_workflow.py
```

**What you'll learn:**
- How teams use notify-mcp for collaboration
- Different notification themes (architecture-decision, alert, state-update)
- Tag-based and priority-based filtering
- Realistic notification content and formatting
- How different team roles interact with channels

## Usage Patterns

### Connecting to notify-mcp

Both examples use stdio transport:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="uv",
    args=["run", "python", "-m", "notify_mcp"],
    env=None
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # ... use session to call tools
```

### Publishing Notifications

```python
result = await session.call_tool(
    "publish_notification",
    arguments={
        "channel": "dev-team",
        "title": "API v2.0 Released",
        "body": "The new API is now live...",
        "priority": "high",
        "theme": "state-update",
        "tags": ["api", "release"]
    }
)
```

### Subscribing with Filters

```python
# Priority filter (only high/critical)
result = await session.call_tool(
    "subscribe_to_channel",
    arguments={
        "channel": "alerts",
        "priority_filter": ["high", "critical"]
    }
)

# Tag filter (only specific topics)
result = await session.call_tool(
    "subscribe_to_channel",
    arguments={
        "channel": "business",
        "tag_filter": ["requirements", "priorities"]
    }
)
```

### Retrieving Notifications

```python
import json

notifications = await session.read_resource(
    uri="notification://dev-team/recent"
)

notifs = json.loads(notifications.contents[0].text)

for notif in notifs:
    print(f"Title: {notif['information']['title']}")
    print(f"Priority: {notif['context']['priority']}")
```

## Customization

Feel free to modify these examples:
- Change channel names to match your team structure
- Add custom notification themes
- Adjust filter criteria
- Add more notification types
- Integrate with your existing workflows

## Integration with AI Assistants

These examples show programmatic access, but the real power comes from using
notify-mcp with AI assistants:

- **Claude Code**: Use the slash commands in `.claude/commands/`
- **ChatGPT**: Configure as an MCP server
- **Gemini**: Use MCP integration (when available)

Teams can then coordinate seamlessly across different AI platforms!

## Troubleshooting

**Server not found:**
- Make sure you're running from the notify-mcp root directory
- Check that `uv run python -m notify_mcp` works manually

**Connection timeout:**
- The server starts on-demand; first request may take 1-2 seconds
- Check stderr output for server errors

**Import errors:**
- Install MCP SDK: `pip install mcp`
- Make sure Python 3.11+ is installed

## Next Steps

After running these examples:
1. Try creating your own channels for your team
2. Experiment with different filter combinations
3. Integrate with your team's workflow
4. Build custom notification templates
5. Set up persistent channels for your projects

## Support

For issues or questions:
- Check the main README.md
- Review the API documentation in docs/API.md
- See notification schema in schemas/notification-schema.json
