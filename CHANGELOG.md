# Changelog

All notable changes to notify-mcp will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-16

### Added
- **HTTP Transport Support**: Added Streamable HTTP transport using MCP SDK's native `StreamableHTTPSessionManager`
  - Run server with `NOTIFY_MCP_TRANSPORT_TYPE=http` environment variable
  - Multi-client session management for concurrent AI assistant connections
  - Remote access from anywhere on the network
  - Cloud deployment ready (Railway, Render, Fly.io, AWS, Docker)
  - HTTP endpoint: `http://<host>:<port>/mcp`
- **Transport Configuration**: New environment variables for HTTP transport
  - `NOTIFY_MCP_TRANSPORT_TYPE`: Choose between "stdio" (default) or "http"
  - `NOTIFY_MCP_HTTP_HOST`: HTTP server host address (default: 0.0.0.0)
  - `NOTIFY_MCP_HTTP_PORT`: HTTP server port (default: 8000)
- **Documentation**: Comprehensive HTTP deployment guide
  - Local network deployment instructions
  - Cloud platform deployment guides (Railway, Render, Fly.io, AWS EC2)
  - Docker deployment configuration
  - Security recommendations and best practices
  - Performance tuning guidance
- **Examples**: Added `examples/run_http_server.py` for standalone HTTP server
- **Tests**: Added 7 new HTTP transport integration tests (69 total tests)

### Changed
- **Server Architecture**: Refactored to support dual transport (stdio + HTTP)
  - Added `run_stdio()`, `run_http()`, and updated `run()` methods
  - Converted `current_client_id` to property for multi-client support
  - Added `active_clients` dictionary for session tracking
  - Added `_client_context` for request-scoped client identification
- **Configuration**: Updated Pydantic settings to use `ConfigDict` (Pydantic v2 style)
- **Documentation**: Updated README with HTTP transport configuration and features
  - Added HTTP transport section with configuration examples
  - Updated roadmap: Phase 2B marked as complete
  - Added security note about no authentication in Community Edition

### Fixed
- Fixed Pydantic deprecation warning in `TransportSettings`

### Security
- **Important**: Community Edition HTTP transport has **no authentication**
  - Recommended for use on private/internal networks only
  - Use VPN for remote access
  - Configure firewall to restrict access
  - For production deployments with authentication, upgrade to Enterprise Edition

### Compatibility
- **Backward Compatible**: Existing stdio transport continues to work (default)
- **Python**: Requires Python 3.11+
- **MCP SDK**: v1.17.0+ (Streamable HTTP support)
- **Dependencies**: Added `starlette` and `uvicorn` (already included as MCP SDK dependencies)

### Performance
- **Concurrent Users**: Community Edition with SQLite supports 5-20 concurrent users
- **Scalability**: For 20-100+ users, upgrade to Enterprise Edition with PostgreSQL

---

## [1.1.0] - 2024-12-XX

### Added
- **SQLite Persistent Storage**: File-based persistent storage for team collaboration
  - Configuration via `NOTIFY_MCP_STORAGE_TYPE` environment variable
  - LRU cache enforcement at database level
  - Foreign key constraints with cascade deletes
- **Storage Factory Pattern**: Configuration-driven storage selection
- **Team Collaboration**: Share notifications via shared SQLite database
- **Storage Configuration**: Environment variables for storage settings
  - `NOTIFY_MCP_STORAGE_TYPE`: "memory", "sqlite" (default: "memory")
  - `NOTIFY_MCP_SQLITE_PATH`: SQLite database file path
  - `NOTIFY_MCP_MAX_HISTORY`: Max notifications per channel (LRU cache)
- **Tests**: Added 14 new SQLite storage tests (62 total tests)
- **Documentation**: Storage configuration guide and migration guide

### Changed
- Storage initialization moved to async `_initialize_server()` method
- Updated architecture to support pluggable storage backends

---

## [1.0.0] - 2024-11-XX

### Added
- **Initial Release**: MVP pub-sub MCP server
- **6 MCP Tools**: publish_notification, subscribe_to_channel, unsubscribe_from_channel, list_channels, create_channel, get_my_subscriptions
- **3 MCP Resources**: notification history, channel info, notification schema
- **2 MCP Prompts**: Architecture decision and alert templates
- **Stdio Transport**: Standard MCP stdio transport for local use
- **In-Memory Storage**: Fast, non-persistent storage for single-user scenarios
- **Smart Filtering**: Filter by priority, tags, themes, sender roles
- **Notification Schema**: Rich notification model with JSON Schema validation
- **Multi-Channel System**: Create and manage multiple notification channels
- **Tests**: 48 unit tests with 70% code coverage
- **Documentation**: Complete API reference, usage guide, and examples

### Compatibility
- Python 3.11+
- MCP SDK 0.9.0+

---

## Release Notes

### v1.2.0 Highlights
This release brings **HTTP transport** to notify-mcp Community Edition, enabling:
- 🌐 Remote collaboration across networks
- 👥 Multiple AI assistants connecting simultaneously
- ☁️ Cloud deployment on platforms like Railway, Render, Fly.io
- 🔄 Real-time team coordination

**Perfect for**: Small teams (5-20 users), development environments, cloud deployments

**Need more?**: Enterprise Edition offers authentication, PostgreSQL, monitoring, and 20-100+ concurrent users

### v1.1.0 Highlights
Persistent storage with SQLite enables team collaboration through shared databases.

### v1.0.0 Highlights
First stable release with complete pub-sub functionality, stdio transport, and in-memory storage.

---

For upgrade instructions, see [Migration Guide](docs/guides/migration-guide.md).
For deployment instructions, see [HTTP Deployment Guide](docs/guides/http-deployment.md).
