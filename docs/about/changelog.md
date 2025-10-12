# Changelog

Release history and version notes for Notify-MCP.

---

## Version 1.1.0 - Persistent Storage (2025-01-12)

### New Features

✅ **Persistent SQLite Storage**
- File-based SQLite database for team collaboration
- Automatic LRU cache enforcement
- Foreign key constraints with cascade deletes
- WAL mode for better concurrency

✅ **Team Collaboration**
- Share notifications via shared database files
- Cross-platform synchronization
- Persistent notification history

✅ **Storage Configuration**
- Environment variable configuration
- Configurable max history per channel
- Path expansion support (~, $HOME)

### Improvements

- Storage factory pattern for extensibility
- Enhanced test coverage (70%)
- 62 passing unit tests
- Comprehensive storage documentation

### Technical Details

- 3 database tables: channels, subscriptions, notifications
- JSON columns for nested Pydantic models
- Indexes on common queries (channel, timestamp)
- Async SQLAlchemy with aiosqlite

---

## Version 1.0.0 - MVP Release (2025-01-10)

### Initial Release

✅ **Core Features**
- Pub-sub architecture with channels
- 6 MCP tools for notification management
- 3 MCP resources for data access
- 2 prompt templates (ADR, alerts)
- Smart filtering (priority, tags, themes, roles)

✅ **Storage**
- In-memory storage with LRU cache
- Notification history (last 50 per channel)

✅ **Quality**
- 48 unit tests
- Pydantic validation
- JSON Schema support
- Type-safe implementation

✅ **Documentation**
- API reference
- Architecture guide
- Usage examples
- Installation guide

---

## Roadmap

See [Roadmap](roadmap.md) for upcoming features.
