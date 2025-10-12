# Release Notes v1.1.0 - Persistent Storage

**Release Date:** 2025-01-12
**Type:** Minor Feature Release
**Phase:** 2A - Persistent Storage

---

## 🎉 What's New

### Persistent Storage with SQLite

**The biggest update yet!** v1.1.0 introduces SQLite-based persistent storage, enabling **true team collaboration** across AI platforms.

#### Key Capabilities

- **💾 Persistent across restarts**: Your notifications, channels, and subscriptions survive server restarts
- **🤝 Team collaboration**: Share a database file so your whole team sees the same notifications
- **📦 Zero setup**: File-based SQLite requires no server installation
- **🔄 Backward compatible**: Defaults to in-memory storage, no breaking changes

---

## 🚀 Features

### 1. SQLite Storage Adapter

A production-ready persistent storage implementation:

```python
# Automatic based on environment variables
NOTIFY_MCP_STORAGE_TYPE=sqlite
NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db
```

**Features:**
- Async SQLite operations with `aiosqlite`
- SQLAlchemy 2.0+ ORM models
- Foreign key constraints with cascade deletes
- JSON serialization of nested Pydantic models
- WAL mode for improved concurrency
- Automatic LRU cache enforcement

**Database Schema:**
- 3 tables: `channels`, `subscriptions`, `notifications`
- Optimized indexes for common queries
- JSON columns for flexible nested data
- Full ACID transactions

### 2. Storage Configuration System

Flexible configuration via environment variables:

```bash
# In-memory (default, fast, ephemeral)
NOTIFY_MCP_STORAGE_TYPE=memory
NOTIFY_MCP_MAX_HISTORY=1000

# SQLite (persistent, shareable)
NOTIFY_MCP_STORAGE_TYPE=sqlite
NOTIFY_MCP_SQLITE_PATH=/shared/team/notify-mcp.db
NOTIFY_MCP_MAX_HISTORY=1000
```

**Configuration Options:**
- `NOTIFY_MCP_STORAGE_TYPE`: `memory` | `sqlite`
- `NOTIFY_MCP_SQLITE_PATH`: Database file path (supports `~` expansion)
- `NOTIFY_MCP_MAX_HISTORY`: Max notifications per channel (LRU cache)

Supports `.env` files and standard environment variable precedence.

### 3. Storage Factory Pattern

Clean abstraction for storage backends:

```python
from notify_mcp.config.storage_config import StorageSettings
from notify_mcp.storage.factory import create_storage

settings = StorageSettings()  # Loads from env
storage = await create_storage(settings)
```

**Benefits:**
- Easy to extend with new storage types
- Type-safe configuration with Pydantic
- Automatic initialization and cleanup
- Graceful degradation

### 4. Team Collaboration Support

**Shared Database Setup:**

All team members configure the same database path:

```json
{
  "mcpServers": {
    "notify-mcp": {
      "env": {
        "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
        "NOTIFY_MCP_SQLITE_PATH": "/shared/team/notify-mcp.db"
      }
    }
  }
}
```

**Result:** Everyone sees the same channels, subscriptions, and notification history! 🎉

**Use Cases:**
- Architect publishes decision → All developers see it
- DevOps alerts production issue → Entire team notified
- Cross-platform AI coordination (Claude ↔ ChatGPT ↔ Gemini)

---

## 📊 Testing

### Comprehensive Test Coverage

- **62 total tests** (+14 new SQLite tests)
- **70% code coverage** (up from 64%)
- **100% coverage** on new storage components

### New Test Suite

`tests/test_sqlite_storage.py` - 14 comprehensive tests:

✅ Channel CRUD operations
✅ Subscription management
✅ Notification persistence
✅ LRU cache enforcement
✅ Foreign key cascade deletes
✅ Pagination and ordering
✅ JSON serialization
✅ Concurrent operations

**All 62 tests passing** ✨

---

## 🔧 Technical Details

### Dependencies Added

```toml
dependencies = [
    "mcp>=0.9.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "jsonschema>=4.20.0",
    "python-dotenv>=1.0.0",
    "sqlalchemy[asyncio]>=2.0.0",  # NEW
    "aiosqlite>=0.19.0",            # NEW
    "alembic>=1.13.0",              # NEW (for future migrations)
]
```

### Architecture Changes

**New Files:**
- `config/storage_config.py` - Pydantic settings for storage
- `storage/models.py` - SQLAlchemy ORM models
- `storage/factory.py` - Storage factory pattern
- `storage/sqlite_storage.py` - SQLite adapter (350+ lines)
- `tests/test_sqlite_storage.py` - SQLite test suite

**Modified Files:**
- `server.py` - Now uses storage factory
- `.gitignore` - Added SQLite database file patterns
- `pyproject.toml` - Version bump + new dependencies

### Database Schema

**channels table:**
```sql
CREATE TABLE channels (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    permissions JSON,
    metadata JSON,
    created_at TIMESTAMP NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    subscriber_count INTEGER DEFAULT 0,
    notification_count INTEGER DEFAULT 0,
    last_notification_at TIMESTAMP
);
```

**subscriptions table:**
```sql
CREATE TABLE subscriptions (
    id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    channel VARCHAR(255) NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
    filters JSON,
    subscribed_at TIMESTAMP NOT NULL
);
CREATE INDEX ix_subscriptions_channel ON subscriptions(channel);
CREATE INDEX ix_subscriptions_client_id ON subscriptions(client_id);
```

**notifications table:**
```sql
CREATE TABLE notifications (
    id VARCHAR(255) PRIMARY KEY,
    channel VARCHAR(255) NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    priority VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    schema_version VARCHAR(20) NOT NULL,
    sender_data JSON NOT NULL,
    context_data JSON NOT NULL,
    information JSON NOT NULL,
    actions JSON,
    visibility JSON NOT NULL,
    metadata_data JSON NOT NULL
);
CREATE INDEX ix_notifications_channel ON notifications(channel);
CREATE INDEX ix_notifications_channel_timestamp ON notifications(channel, timestamp DESC);
```

---

## 📈 Performance

### Benchmarks (Approximate)

| Storage Type | Write Latency | Read Latency | Capacity | Persistence |
|--------------|---------------|--------------|----------|-------------|
| In-Memory | <1ms | <1ms | ~10K notifications | ❌ Lost on restart |
| SQLite | ~5-10ms | ~2-5ms | ~100K notifications | ✅ Survives restart |

### LRU Cache

Both storage types enforce LRU cache automatically:

- **In-Memory**: Python dict-based, very fast
- **SQLite**: Database-enforced, deletes oldest notifications

Default: 1000 notifications per channel (configurable via `NOTIFY_MCP_MAX_HISTORY`)

---

## 🔄 Migration Guide

### Upgrading from v1.0.0

**Step 1:** Update dependencies
```bash
cd /path/to/notify-mcp
uv sync
```

**Step 2:** Choose storage type

**Option A: Keep in-memory (default, no changes needed)**
```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "memory"
  }
}
```

**Option B: Enable SQLite persistence**
```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "~/.notify-mcp/storage.db"
  }
}
```

**Step 3:** Restart your AI assistant (Claude, ChatGPT, etc.)

**Note:** Existing in-memory data is **not** automatically migrated to SQLite. This is a fresh start with persistence.

---

## ⚠️ Breaking Changes

**None!** This release is fully backward compatible.

- Defaults to in-memory storage
- Existing configurations continue to work
- No API changes

---

## 🐛 Bug Fixes

No bug fixes in this release (focused on new features).

---

## 📚 Documentation

### New Documentation

- **[Storage Guide](docs/STORAGE_GUIDE.md)** - Complete guide to storage configuration
- **[Database Schema](docs/product/database-schema.md)** - Detailed schema documentation
- **[README Updates](README.md)** - Added storage configuration section

### Updated Documentation

- README.md - New storage configuration section
- README.md - Updated test counts (62 tests, 70% coverage)
- README.md - Updated roadmap showing Phase 2A complete

---

## 🎯 Use Cases Enabled

### Before v1.1.0 (In-Memory Only)

- ✅ Single developer using one AI assistant
- ❌ Team collaboration across AI platforms
- ❌ Persistent notification history
- ❌ Audit trail and compliance

### After v1.1.0 (With SQLite)

- ✅ Single developer with persistent history
- ✅ **Team collaboration across AI platforms** 🎉
- ✅ **Persistent notification history** 🎉
- ✅ **Audit trail and compliance** 🎉
- ✅ Shared context across Claude, ChatGPT, Gemini

---

## 🚧 Known Limitations

### SQLite Concurrency

- **Good for**: 1-20 concurrent users
- **Not ideal for**: >20 concurrent users writing simultaneously
- **Workaround**: Wait for Phase 2B (HTTP + Redis) for high concurrency

### Network Storage

- SQLite works on network drives (NFS, SMB)
- **Best**: Low-latency local or LAN storage (<10ms)
- **Avoid**: High-latency network storage (>50ms)
- **Alternative**: Local copy + sync, or wait for centralized HTTP server (Phase 2B)

### Database Size

- LRU cache prevents unbounded growth
- Recommended: `MAX_HISTORY=500-1000` per channel
- For very large teams, consider periodic cleanup

---

## 🔮 What's Next

### Phase 2B: Real-Time Collaboration (In Progress)

- HTTP transport
- Redis Pub/Sub for real-time updates
- WebSocket support
- Multi-server deployment

### Enterprise Edition (Planned)

- PostgreSQL support
- Advanced replication
- Automated backups
- Multi-tenancy
- Authentication and RBAC

---

## 🙏 Acknowledgments

This release implements the storage architecture from:
- **Product Decision Record**: `docs/product/PDR-001-community-enterprise-split.md`
- **Database Design**: `docs/product/database-schema.md`

Built with:
- [SQLAlchemy 2.0](https://www.sqlalchemy.org/) - Modern async ORM
- [aiosqlite](https://github.com/omnilib/aiosqlite) - Async SQLite driver
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Type-safe configuration

---

## 📦 Installation

### Fresh Install

```bash
# Clone repository
git clone <repository-url>
cd notify-mcp

# Install dependencies
uv sync

# Configure storage (optional)
export NOTIFY_MCP_STORAGE_TYPE=sqlite
export NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db

# Run tests
uv run pytest -v

# All 62 tests should pass! ✅
```

### Upgrade Existing Installation

```bash
cd /path/to/notify-mcp

# Pull latest changes
git pull origin main

# Update dependencies
uv sync

# Restart MCP server (via AI assistant restart)
```

---

## 🐛 Reporting Issues

Found a bug? Please report it!

- **GitHub Issues**: [Create New Issue](https://github.com/your-org/notify-mcp/issues)
- **Include**: Version (v1.1.0), storage type, error logs, configuration

---

## 🎓 Learning Resources

- **[Storage Guide](docs/STORAGE_GUIDE.md)** - How to configure storage
- **[Usage Examples](examples/)** - Code samples
- **[API Reference](docs/API.md)** - Complete MCP API docs
- **[Architecture](docs/ARCHITECTURE.md)** - System design

---

## 📊 Stats Summary

| Metric | v1.0.0 | v1.1.0 | Change |
|--------|--------|--------|--------|
| **Version** | 1.0.0 | 1.1.0 | Minor update |
| **Test Count** | 48 | 62 | +14 tests |
| **Code Coverage** | 64% | 70% | +6% |
| **Storage Types** | 1 (memory) | 2 (memory, SQLite) | +1 |
| **Dependencies** | 11 | 14 | +3 |
| **LOC (src)** | ~2000 | ~2800 | +40% |
| **Documentation** | 5 docs | 7 docs | +2 |

---

## ✅ Verification Checklist

After upgrading, verify the installation:

```bash
# 1. Check version
grep "version = " pyproject.toml
# Should show: version = "1.1.0"

# 2. Run tests
uv run pytest -v
# Should show: 62 passed

# 3. Test SQLite storage
export NOTIFY_MCP_STORAGE_TYPE=sqlite
export NOTIFY_MCP_SQLITE_PATH=/tmp/test-notify.db
uv run python -m notify_mcp &
# Server should start without errors

# 4. Check database was created
ls -lh /tmp/test-notify.db
# File should exist

# 5. Inspect schema
sqlite3 /tmp/test-notify.db ".schema"
# Should show channels, subscriptions, notifications tables
```

---

## 🎉 Thank You!

Thank you for using Notify-MCP! This release represents a major step forward in enabling seamless team collaboration across AI platforms.

**What's your use case?** Share your team collaboration stories!

---

**Version:** 1.1.0
**Release Date:** 2025-01-12
**Phase:** 2A Complete ✅
**Next Phase:** 2B - Real-Time Collaboration
