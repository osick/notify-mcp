# Storage Configuration

Configure persistent storage for team collaboration.

---

## Overview

Notify-MCP v1.1.0+ supports two storage modes:

| Storage Type | Best For | Persistence | Team Collaboration |
|--------------|----------|-------------|-------------------|
| **In-Memory** | Individual use, testing | ❌ No | ❌ No |
| **SQLite** | Team collaboration | ✅ Yes | ✅ Yes |

---

## Quick Configuration

### In-Memory (Default)

```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "memory"
  }
}
```

- Fast, no disk I/O
- Data lost on restart
- Good for testing

### SQLite (Team Collaboration)

```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "~/.notify-mcp/storage.db",
    "NOTIFY_MCP_MAX_HISTORY": "1000"
  }
}
```

- Persistent across restarts
- Share database file for team collaboration
- Automatic LRU cache enforcement

---

## Team Collaboration Setup

### Shared Network Drive

All team members point to the same database file:

**macOS:**
```json
{
  "NOTIFY_MCP_SQLITE_PATH": "/Volumes/TeamDrive/notify-mcp.db"
}
```

**Linux:**
```json
{
  "NOTIFY_MCP_SQLITE_PATH": "/mnt/teamdrive/notify-mcp.db"
}
```

**Windows:**
```json
{
  "NOTIFY_MCP_SQLITE_PATH": "Z:\\notify-mcp.db"
}
```

Everyone sharing the database sees the same channels and notifications!

---

## Configuration Reference

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `NOTIFY_MCP_STORAGE_TYPE` | `memory`, `sqlite` | `memory` | Storage backend |
| `NOTIFY_MCP_SQLITE_PATH` | file path | `~/.notify-mcp/storage.db` | Database location |
| `NOTIFY_MCP_MAX_HISTORY` | integer | `1000` | Max notifications per channel |

---

## Database Management

### Backup

```bash
# Create backup
cp ~/.notify-mcp/storage.db ~/.notify-mcp/backup-$(date +%Y%m%d).db
```

### Inspect

```bash
# Open SQLite shell
sqlite3 ~/.notify-mcp/storage.db

# List tables
.tables

# Query notifications
SELECT channel, COUNT(*) FROM notifications GROUP BY channel;
```

---

## Troubleshooting

### Database Locked

```bash
# Stop all servers
pkill -f "notify_mcp"

# Remove lock files
rm ~/.notify-mcp/storage.db-wal
rm ~/.notify-mcp/storage.db-shm
```

### Permission Denied

```bash
# Fix permissions
chmod 644 ~/.notify-mcp/storage.db
chmod 755 ~/.notify-mcp/
```

---

**For complete storage documentation**, see the detailed [Storage Guide](../STORAGE_GUIDE.md).

---

## Next Steps

- **[Team Collaboration Guide](team-collaboration.md)**
- **[Best Practices](best-practices.md)**
- **[Architecture: Storage](../architecture/storage.md)**
