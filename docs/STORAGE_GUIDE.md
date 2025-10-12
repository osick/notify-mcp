# Storage Configuration Guide

**Version:** 1.1.0
**Last Updated:** 2025-01-12

---

## Overview

Notify-MCP v1.1.0 introduces **persistent storage** to enable team collaboration through shared databases. This guide covers storage configuration, migration strategies, and best practices.

---

## Storage Types

### In-Memory Storage (Default)

**Best for**: Individual developers, testing, ephemeral workloads

**Characteristics**:
- ⚡ Fastest performance (no I/O)
- 🔄 Data lost on server restart
- 💻 Single-process only
- 📊 Configurable LRU cache

**Configuration**:
```bash
NOTIFY_MCP_STORAGE_TYPE=memory
NOTIFY_MCP_MAX_HISTORY=1000
```

**Use Cases**:
- Local development and testing
- Proof-of-concept demos
- Short-lived AI assistant sessions
- When persistence is not needed

---

### SQLite Storage (v1.1.0+)

**Best for**: Teams, persistent notifications, shared collaboration

**Characteristics**:
- 💾 Persistent across restarts
- 🤝 Multiple team members can share one database
- 📦 No server setup required (file-based)
- 🔒 ACID transactions with foreign key constraints
- 📈 Handles ~100K notifications efficiently
- 🗂️ Automatic LRU cache enforcement

**Configuration**:
```bash
NOTIFY_MCP_STORAGE_TYPE=sqlite
NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db
NOTIFY_MCP_MAX_HISTORY=1000
```

**Use Cases**:
- Team collaboration (shared network drive)
- Persistent notification history
- Cross-platform AI coordination
- Audit trail and compliance
- Local development with persistence

**Database Schema**:
- 3 tables: `channels`, `subscriptions`, `notifications`
- JSON columns for nested data (Pydantic models)
- Indexes on common queries (channel, timestamp)
- Foreign key cascade deletes
- WAL mode for better concurrency

---

## Configuration Methods

### 1. Environment Variables (Recommended)

Set environment variables in your MCP server configuration:

**Claude Desktop (`claude_desktop_config.json`)**:
```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "notify_mcp"],
      "cwd": "/path/to/notify-mcp",
      "env": {
        "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
        "NOTIFY_MCP_SQLITE_PATH": "/shared/team/notify-mcp.db",
        "NOTIFY_MCP_MAX_HISTORY": "1000"
      }
    }
  }
}
```

**System Environment**:
```bash
export NOTIFY_MCP_STORAGE_TYPE=sqlite
export NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db
export NOTIFY_MCP_MAX_HISTORY=1000
```

### 2. .env File

Create a `.env` file in the notify-mcp directory:

```bash
# .env
NOTIFY_MCP_STORAGE_TYPE=sqlite
NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db
NOTIFY_MCP_MAX_HISTORY=1000
```

The server will automatically load this file using `python-dotenv`.

---

## Configuration Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NOTIFY_MCP_STORAGE_TYPE` | `memory` \| `sqlite` | `memory` | Storage backend to use |
| `NOTIFY_MCP_SQLITE_PATH` | string | `~/.notify-mcp/storage.db` | Path to SQLite database file |
| `NOTIFY_MCP_MAX_HISTORY` | integer | `1000` | Max notifications per channel (LRU) |

**Path Expansion**:
- `~` expands to user home directory
- Environment variables are expanded: `$HOME/notify.db`
- Relative paths are resolved from working directory

---

## Team Collaboration Setup

### Scenario 1: Shared Network Drive

All team members point to the same database file on a shared network location:

**Team Member 1 (macOS)**:
```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "/Volumes/TeamDrive/notify-mcp.db"
  }
}
```

**Team Member 2 (Linux)**:
```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "/mnt/teamdrive/notify-mcp.db"
  }
}
```

**Team Member 3 (Windows)**:
```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "Z:\\notify-mcp.db"
  }
}
```

### Scenario 2: Cloud Sync (Dropbox, Google Drive)

Store the database in a cloud-synced folder:

```bash
NOTIFY_MCP_SQLITE_PATH=~/Dropbox/notify-mcp/storage.db
```

**⚠️ Warning**: Cloud sync may cause conflicts with concurrent writes. Use with caution for small teams.

### Scenario 3: Git Repository

Store the database in a shared git repository:

```bash
NOTIFY_MCP_SQLITE_PATH=~/projects/team-notifications/notify-mcp.db
```

Add to `.gitignore` if needed:
```gitignore
# Optionally exclude from git
*.db
*.db-wal
*.db-shm
```

**Best Practice**: Commit the database for audit trail, or exclude for sensitive data.

---

## Migration Guide

### Migrating from In-Memory to SQLite

**Step 1**: Stop the MCP server (restart Claude/AI assistant)

**Step 2**: Update configuration:
```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "~/.notify-mcp/storage.db"
  }
}
```

**Step 3**: Restart the MCP server

**Note**: In-memory data is **lost** during migration. There is no automatic data transfer.

### Starting Fresh with SQLite

```bash
# Remove old database if exists
rm ~/.notify-mcp/storage.db*

# Configure SQLite
export NOTIFY_MCP_STORAGE_TYPE=sqlite
export NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db

# Start server
uv run python -m notify_mcp
```

The database schema is created automatically on first startup.

---

## Database Management

### Backup SQLite Database

```bash
# Create backup
cp ~/.notify-mcp/storage.db ~/.notify-mcp/storage-backup-$(date +%Y%m%d).db

# Or use SQLite backup command
sqlite3 ~/.notify-mcp/storage.db ".backup /path/to/backup.db"
```

### Restore from Backup

```bash
# Stop the server first
cp /path/to/backup.db ~/.notify-mcp/storage.db
# Restart the server
```

### Inspect Database

```bash
# Open SQLite shell
sqlite3 ~/.notify-mcp/storage.db

# List tables
.tables

# Show schema
.schema channels

# Query notifications
SELECT channel, COUNT(*) FROM notifications GROUP BY channel;

# Exit
.quit
```

### Database Size Management

The LRU cache automatically limits notifications per channel:

```bash
# Set lower limit for smaller database
NOTIFY_MCP_MAX_HISTORY=500
```

Manual cleanup (if needed):
```sql
-- Delete old notifications manually
DELETE FROM notifications
WHERE timestamp < datetime('now', '-30 days');

-- Vacuum to reclaim space
VACUUM;
```

---

## Performance Considerations

### SQLite Optimizations

Notify-MCP automatically applies these optimizations:

- **WAL Mode**: Better concurrency, allows concurrent reads
- **Foreign Keys**: Enabled for referential integrity
- **Indexes**: Optimized for common queries (channel, timestamp)
- **Connection Pooling**: Async connection management

### Recommended Settings

For optimal performance:

| Team Size | Max History | Expected DB Size |
|-----------|-------------|------------------|
| 1-5 users | 1000/channel | < 10 MB |
| 5-20 users | 500/channel | < 50 MB |
| 20+ users | 250/channel | < 100 MB |

### Network Drive Performance

- **Avoid**: High-latency network drives (>50ms)
- **Prefer**: Low-latency NFS/SMB shares (<10ms)
- **Alternative**: Use centralized server with HTTP transport (Phase 2B)

---

## Troubleshooting

### Database Locked Error

**Problem**: `database is locked` error

**Causes**:
- Multiple processes accessing same database
- Network drive with poor locking support
- Long-running transaction

**Solutions**:
```bash
# 1. Ensure only one server instance runs
pkill -f "notify_mcp"

# 2. Check for stale lock files
rm ~/.notify-mcp/storage.db-wal
rm ~/.notify-mcp/storage.db-shm

# 3. Use local storage instead of network drive
NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/local-storage.db
```

### Database Corruption

**Problem**: Database file is corrupted

**Solution**:
```bash
# 1. Stop server
# 2. Try to recover
sqlite3 ~/.notify-mcp/storage.db "PRAGMA integrity_check;"

# 3. If corrupted, restore from backup
cp /path/to/backup.db ~/.notify-mcp/storage.db

# 4. If no backup, start fresh
rm ~/.notify-mcp/storage.db*
```

### Slow Performance

**Problem**: Queries are slow

**Solutions**:
```bash
# 1. Reduce max history
NOTIFY_MCP_MAX_HISTORY=500

# 2. Check database size
ls -lh ~/.notify-mcp/storage.db

# 3. Vacuum database
sqlite3 ~/.notify-mcp/storage.db "VACUUM;"

# 4. Check indexes
sqlite3 ~/.notify-mcp/storage.db ".schema"
```

### Permission Denied

**Problem**: Cannot write to database file

**Solutions**:
```bash
# 1. Check file permissions
ls -l ~/.notify-mcp/storage.db

# 2. Fix permissions
chmod 644 ~/.notify-mcp/storage.db

# 3. Check directory permissions
chmod 755 ~/.notify-mcp/

# 4. Use different path
NOTIFY_MCP_SQLITE_PATH=/tmp/notify-mcp.db
```

---

## Best Practices

### Development

✅ **Do**:
- Use in-memory storage for tests
- Keep separate databases for dev/test/prod
- Commit database schema to version control
- Automate backups

❌ **Don't**:
- Share production database with development
- Store secrets in notifications
- Use SQLite over high-latency networks

### Production (Small Teams)

✅ **Do**:
- Use SQLite on reliable network share
- Set up automated daily backups
- Monitor database size
- Set appropriate `MAX_HISTORY`

❌ **Don't**:
- Share database across >20 concurrent users
- Use cloud-synced folders (Dropbox) for production
- Disable foreign key constraints

### Future: Enterprise Production

For large-scale deployments (20+ users), wait for:
- **Phase 2B**: HTTP transport + Redis
- **Enterprise Edition**: PostgreSQL support

---

## FAQ

### Q: Can I use PostgreSQL instead of SQLite?

**A**: PostgreSQL support is planned for the Enterprise Edition (Phase 2+). Currently, SQLite and in-memory storage are available.

### Q: How do I share notifications across different AI platforms?

**A**: All AI assistants (Claude, ChatGPT, Gemini) should point to the same SQLite database file via their MCP configuration.

### Q: Is the database encrypted?

**A**: SQLite database is not encrypted by default. Use file-system encryption (e.g., LUKS, FileVault, BitLocker) for sensitive data.

### Q: Can I query the database directly?

**A**: Yes! Use the `sqlite3` command-line tool or any SQLite GUI (DB Browser, DBeaver). The schema includes 3 tables: `channels`, `subscriptions`, and `notifications`. See the "Database Schema" section in the release notes or inspect with `sqlite3 <db-file> ".schema"`.

### Q: What happens if two people write simultaneously?

**A**: SQLite uses WAL mode with automatic locking. Writes are serialized, and concurrent reads are supported. However, for high concurrency (20+ users), consider Phase 2B (HTTP + Redis).

### Q: Can I migrate from SQLite to PostgreSQL later?

**A**: Yes, when PostgreSQL support is added (Enterprise Edition), a migration tool will be provided.

---

## Related Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [API Reference](API.md)
- [Usage Guide](USAGE_GUIDE.md)

---

## Support

For issues or questions:
- **GitHub Issues**: Report bugs or feature requests
- **Documentation**: Check `docs/` directory
- **Examples**: See `examples/` for code samples

---

**Version:** 1.1.0
**Last Updated:** 2025-01-12
