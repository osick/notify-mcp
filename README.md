# Notify-MCP

Pub-Sub MCP server for team collaboration across genAI platforms (ChatGPT, Claude, Gemini).

## Features

- 📢 **Notification Channels**: Create and manage team notification channels
- 🔔 **Pub-Sub Architecture**: Subscribe to channels with flexible filters
- 🎯 **Smart Filtering**: Filter by priority, tags, themes, and sender roles
- 🤖 **MCP Integration**: Full Model Context Protocol support
- 🚀 **Phase 1 (MVP)**: stdio transport with in-memory storage

## Installation

```bash
# Clone/navigate to repository
cd notify-mcp

# Install dependencies with uv
uv sync

# Run the server
uv run python -m notify_mcp
```

## Configuration

### Claude Code MCP Configuration

Add to `~/.config/claude-code/mcp_servers.json`:

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "notify_mcp"],
      "cwd": "/home/os/development/notify-mcp"
    }
  }
}
```

## Quick Reference

### 🛠️ Tools (6)
- `publish_notification` - Publish to channel
- `subscribe_to_channel` - Subscribe with filters  
- `unsubscribe_from_channel` - Unsubscribe
- `list_channels` - List all channels
- `create_channel` - Create new channel
- `get_my_subscriptions` - View subscriptions

### 📚 Resources (2)
- `notification://<channel>/recent` - Last 50 notifications
- `channel://<channel>/info` - Channel details

### 📝 Prompts (2)
- `create_decision_notification` - Architecture decisions
- `send_alert` - Critical alerts

## License

MIT
