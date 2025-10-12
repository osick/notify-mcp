# Storage Architecture

Overview of Notify-MCP's storage layer.

---

## Storage Types

### In-Memory Storage

**Implementation:** Python dictionaries
**Performance:** Fastest (no I/O)
**Persistence:** None
**Use case:** Individual use, testing

### SQLite Storage

**Implementation:** SQLAlchemy + aiosqlite
**Performance:** Fast (file-based)
**Persistence:** Yes
**Use case:** Team collaboration

---

## Database Schema

**Tables:**
- `channels` - Channel definitions
- `subscriptions` - Client subscriptions
- `notifications` - Notification history

**Features:**
- Foreign key constraints
- Cascade deletes
- JSON columns for nested data
- Indexes on common queries
- WAL mode for concurrency

---

## LRU Cache

Automatic enforcement of max history per channel:

- Default: 1000 notifications per channel
- Configurable via `NOTIFY_MCP_MAX_HISTORY`
- Old notifications automatically removed

---

For complete storage documentation, see: [Storage Guide](../STORAGE_GUIDE.md)
