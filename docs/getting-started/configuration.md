# Configuration

Configure Notify-MCP to work with your AI assistant and team.

---

## Claude Desktop / Claude Code

Add Notify-MCP to your Claude configuration file:

**File Location:**
- macOS/Linux: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "notify_mcp"],
      "cwd": "/absolute/path/to/notify-mcp/packages/community",
      "env": {
        "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
        "NOTIFY_MCP_SQLITE_PATH": "~/.notify-mcp/storage.db",
        "NOTIFY_MCP_MAX_HISTORY": "1000"
      }
    }
  }
}
```

**Restart Claude Desktop** after saving the configuration.

---

## Storage Configuration

### In-Memory Storage (Default)

Fast but not persistent across restarts. Good for individual use:

```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "memory"
  }
}
```

### SQLite Storage (Recommended for Teams)

Persistent storage that enables team collaboration:

```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "~/.notify-mcp/storage.db",
    "NOTIFY_MCP_MAX_HISTORY": "1000"
  }
}
```

**For team collaboration**, use a shared network location:

```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "/shared/team/notify-mcp.db"
  }
}
```

All team members pointing to the same database file will share channels and notifications!

[:octicons-arrow-right-24: Detailed Storage Configuration](../guides/storage-configuration.md)

---

## Configuration Reference

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `NOTIFY_MCP_STORAGE_TYPE` | `memory`, `sqlite` | `memory` | Storage backend type |
| `NOTIFY_MCP_SQLITE_PATH` | file path | `~/.notify-mcp/storage.db` | SQLite database path |
| `NOTIFY_MCP_MAX_HISTORY` | integer | `1000` | Max notifications per channel |

---

## ChatGPT Configuration

ChatGPT MCP support is in development. Use an MCP bridge for now:

```bash
# 1. Run notify-mcp server
uv run python -m notify_mcp

# 2. Use MCP-to-HTTP bridge
mcp-bridge --stdio "uv run python -m notify_mcp" --http localhost:8080

# 3. Configure ChatGPT Custom GPT to use the bridge endpoint
```

Native ChatGPT MCP support expected in 2025.

---

## Gemini Configuration

Gemini MCP integration is in development. Use the Gemini API with an MCP adapter:

```python
from google.generativeai import GenerativeModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "notify_mcp"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Use Gemini with MCP tools
```

Full Gemini MCP integration expected in 2025.

---

## Slash Commands (Claude Code)

Notify-MCP includes 6 convenient slash commands:

- `/notify-decision` - Create architecture decision notification
- `/notify-alert` - Create critical alert
- `/notify-status` - Share status update
- `/notify-channels` - List all channels
- `/notify-subscribe` - Subscribe to a channel
- `/notify-recent` - View recent notifications

These commands are automatically available in Claude Code once Notify-MCP is configured.

---

## Next Steps

- **[Follow the Quick Start Tutorial →](quick-start.md)**
- **[Review Storage Configuration Details →](../guides/storage-configuration.md)**
- **[Explore Use Cases →](../use-cases/index.md)**

---

## Troubleshooting

### Server Not Starting

```bash
# Test manually
uv run python -m notify_mcp

# Check if uv is in PATH
which uv

# Use absolute path if needed
"command": "/full/path/to/uv"
```

### Claude Doesn't See the Server

1. Check the configuration file path is correct
2. Ensure you restarted Claude Desktop
3. Verify the `cwd` path points to the correct directory
4. Check Claude logs for error messages

---

For more help, see the [Troubleshooting Guide](../guides/troubleshooting.md).
