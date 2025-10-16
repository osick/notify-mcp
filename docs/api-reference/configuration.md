# Configuration Options

Environment variables and settings for Notify-MCP.

---

## Environment Variables

### Transport Configuration

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `NOTIFY_MCP_TRANSPORT_TYPE` | `stdio`, `http` | `stdio` | Transport protocol |
| `NOTIFY_MCP_HTTP_HOST` | IP address | `0.0.0.0` | HTTP server host |
| `NOTIFY_MCP_HTTP_PORT` | port number | `8000` | HTTP server port |

### Storage Configuration

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `NOTIFY_MCP_STORAGE_TYPE` | `memory`, `sqlite` | `memory` | Storage backend type |
| `NOTIFY_MCP_SQLITE_PATH` | file path | `~/.notify-mcp/storage.db` | SQLite database path |
| `NOTIFY_MCP_MAX_HISTORY` | integer | `1000` | Max notifications per channel (LRU) |

### General Configuration

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `NOTIFY_MCP_LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` | Logging level |

---

## MCP Server Configuration

### Claude Desktop

File: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "notify_mcp"],
      "cwd": "/path/to/notify-mcp",
      "env": {
        "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
        "NOTIFY_MCP_SQLITE_PATH": "~/.notify-mcp/storage.db"
      }
    }
  }
}
```

---

## Storage Configuration

See: [Storage Configuration Guide](../guides/storage-configuration.md)

---

For complete configuration details, see: [Configuration Guide](../getting-started/configuration.md)
