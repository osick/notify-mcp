# Notify-MCP Server Architecture

## Overview

The Notify-MCP server is a Pub-Sub (Publish-Subscribe) notification system built on the Model Context Protocol (MCP). It enables team collaboration across genAI platforms (ChatGPT, Claude, Gemini) by providing a flexible, channel-based notification infrastructure.

**Architecture Pattern:** Pub-Sub (Publish-Subscribe)
**Protocol:** Model Context Protocol (MCP) over JSON-RPC 2.0
**Communication Style:** Asynchronous, event-driven

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MCP Clients                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Claude  │  │ ChatGPT  │  │  Gemini  │  │  Custom  │       │
│  │  Client  │  │  Client  │  │  Client  │  │   App    │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │              │             │              │
│       └─────────────┴──────────────┴─────────────┘              │
│                     │                                           │
│              MCP Transport Layer                                │
│         (stdio / HTTP / WebSocket)                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                  Notify-MCP Server                              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              MCP Protocol Handler                         │ │
│  │  • Request handling                                       │ │
│  │  • Notification delivery                                  │ │
│  │  • JSON-RPC 2.0 message processing                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                            │                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Core Services Layer                          │ │
│  │                                                           │ │
│  │  ┌──────────────────┐  ┌──────────────────┐            │ │
│  │  │  Subscription    │  │   Notification   │            │ │
│  │  │   Manager        │  │     Router       │            │ │
│  │  │                  │  │                  │            │ │
│  │  │ • Subscribe      │  │ • Publish        │            │ │
│  │  │ • Unsubscribe    │  │ • Route          │            │ │
│  │  │ • List channels  │  │ • Filter         │            │ │
│  │  └──────────────────┘  └──────────────────┘            │ │
│  │                                                           │ │
│  │  ┌──────────────────┐  ┌──────────────────┐            │ │
│  │  │     Channel      │  │    Notification  │            │ │
│  │  │     Manager      │  │     Validator    │            │ │
│  │  │                  │  │                  │            │ │
│  │  │ • Create channel │  │ • Schema check   │            │ │
│  │  │ • Delete channel │  │ • Validate       │            │ │
│  │  │ • Permissions    │  │ • Transform      │            │ │
│  │  └──────────────────┘  └──────────────────┘            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                            │                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Storage Layer (Optional)                     │ │
│  │                                                           │ │
│  │  ┌──────────────────┐  ┌──────────────────┐            │ │
│  │  │   Subscription   │  │   Notification   │            │ │
│  │  │      Store       │  │     History      │            │ │
│  │  │                  │  │                  │            │ │
│  │  │ • In-memory      │  │ • In-memory      │            │ │
│  │  │ • File-based     │  │ • File-based     │            │ │
│  │  │ • Redis (future) │  │ • Redis (future) │            │ │
│  │  └──────────────────┘  └──────────────────┘            │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **MCP Protocol Handler**

**Responsibility:** Handle MCP protocol communication with clients

**Functions:**
- Accept client connections (stdio, HTTP, WebSocket)
- Parse JSON-RPC 2.0 messages
- Route requests to appropriate services
- Send notifications to subscribed clients
- Handle capability negotiation

**MCP Methods Supported:**
- `initialize`: Client initialization
- `notifications/subscribe`: Subscribe to channels
- `notifications/unsubscribe`: Unsubscribe from channels
- `notifications/publish`: Publish notification
- `notifications/list`: List available channels
- Server-sent notifications via MCP notification mechanism

---

### 2. **Subscription Manager**

**Responsibility:** Manage client subscriptions to notification channels

**Data Structure:**
```javascript
{
  "channel-name": [
    {
      "clientId": "client-123",
      "filters": {
        "priority": ["high", "critical"],
        "tags": ["backend", "security"],
        "roles": ["dev", "consulting"]
      },
      "subscribedAt": "2025-10-11T14:00:00Z"
    }
  ]
}
```

**Operations:**
- `subscribe(clientId, channel, filters)`: Add subscription
- `unsubscribe(clientId, channel)`: Remove subscription
- `getSubscribers(channel)`: Get all subscribers for a channel
- `getSubscriptions(clientId)`: Get all subscriptions for a client
- `applyFilters(notification, filters)`: Check if notification matches filters

---

### 3. **Notification Router**

**Responsibility:** Route notifications to subscribed clients

**Algorithm:**
1. Receive notification from publisher
2. Identify target channel(s)
3. Get all subscribers for channel(s)
4. Apply filters for each subscriber
5. Deliver notification to matching subscribers
6. Track delivery status

**Delivery Modes:**
- **Broadcast:** Send to all subscribers (no filters)
- **Filtered:** Send only to matching subscribers
- **Direct:** Send to specific client(s)

---

### 4. **Channel Manager**

**Responsibility:** Manage notification channels

**Channel Properties:**
```javascript
{
  "id": "project-alpha",
  "name": "Project Alpha",
  "description": "Notifications for Project Alpha team",
  "createdAt": "2025-10-11T10:00:00Z",
  "createdBy": "user-123",
  "permissions": {
    "publish": ["dev", "consulting", "business"],
    "subscribe": ["dev", "consulting", "business", "viewer"]
  },
  "metadata": {
    "projectId": "proj-456",
    "tags": ["active", "high-priority"]
  }
}
```

**Operations:**
- `createChannel(name, permissions)`: Create new channel
- `deleteChannel(channelId)`: Delete channel
- `listChannels()`: List all channels
- `getChannel(channelId)`: Get channel details
- `updatePermissions(channelId, permissions)`: Update access control

---

### 5. **Notification Validator**

**Responsibility:** Validate and transform notifications

**Functions:**
- Schema validation (using `schemas/notification-schema.json`)
- Version compatibility checking
- Default value injection
- Metadata generation (id, timestamp, sequence)
- Format transformation (if needed)

**Validation Flow:**
```
Incoming Notification
    │
    ├─> Check schemaVersion
    ├─> Validate against JSON Schema
    ├─> Inject system metadata
    ├─> Apply defaults
    ├─> Transform if needed
    │
    └─> Valid Notification → Router
         Invalid → Error response
```

---

### 6. **Storage Layer** (Pluggable)

**Responsibility:** Persist subscriptions and notification history

**Initial Implementation:** In-memory
**Future Options:** File-based, Redis, PostgreSQL

**Storage Interface:**
```typescript
interface StorageAdapter {
  // Subscriptions
  saveSubscription(subscription: Subscription): Promise<void>;
  deleteSubscription(clientId: string, channel: string): Promise<void>;
  getSubscriptions(channel: string): Promise<Subscription[]>;

  // Notification history
  saveNotification(notification: Notification): Promise<void>;
  getNotifications(channel: string, limit?: number): Promise<Notification[]>;

  // Channels
  saveChannel(channel: Channel): Promise<void>;
  deleteChannel(channelId: string): Promise<void>;
  getChannels(): Promise<Channel[]>;
}
```

---

## Data Flow

### Publishing a Notification

```
┌─────────┐
│ Client  │
│ (Alice) │
└────┬────┘
     │
     │ 1. publish_notification
     │    {channel: "project-alpha", ...}
     ▼
┌─────────────────┐
│  MCP Protocol   │
│    Handler      │
└────┬────────────┘
     │
     │ 2. Validate
     ▼
┌─────────────────┐
│  Notification   │
│   Validator     │
└────┬────────────┘
     │
     │ 3. Route
     ▼
┌─────────────────┐
│  Notification   │
│     Router      │
└────┬────────────┘
     │
     │ 4. Get subscribers
     ▼
┌─────────────────┐
│  Subscription   │
│    Manager      │
└────┬────────────┘
     │
     │ 5. Filter & Deliver
     ├────────────────┬────────────────┐
     ▼                ▼                ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client  │     │ Client  │     │ Client  │
│  (Bob)  │     │ (Carol) │     │ (Dave)  │
└─────────┘     └─────────┘     └─────────┘
   (Dev)        (Consulting)      (Business)
```

### Subscribing to a Channel

```
┌─────────┐
│ Client  │
│ (Bob)   │
└────┬────┘
     │
     │ 1. subscribe
     │    {channel: "project-alpha", filters: {...}}
     ▼
┌─────────────────┐
│  MCP Protocol   │
│    Handler      │
└────┬────────────┘
     │
     │ 2. Check permissions
     ▼
┌─────────────────┐
│     Channel     │
│     Manager     │
└────┬────────────┘
     │
     │ 3. Add subscription
     ▼
┌─────────────────┐
│  Subscription   │
│    Manager      │
└────┬────────────┘
     │
     │ 4. Persist (optional)
     ▼
┌─────────────────┐
│  Storage Layer  │
└─────────────────┘
     │
     │ 5. Success response
     ▼
┌─────────┐
│ Client  │
│ (Bob)   │
└─────────┘
```

---

## Communication Patterns

### 1. **Broadcast Pattern**
- Publisher sends to channel
- All subscribers receive notification
- No filtering applied
- Use case: General announcements

### 2. **Filtered Pattern**
- Publisher sends to channel
- Subscribers specify filters (priority, tags, roles)
- Only matching subscribers receive notification
- Use case: Targeted team notifications

### 3. **Direct Pattern**
- Publisher sends to specific client(s)
- Bypasses channel subscriptions
- Use case: Direct messages, responses

### 4. **Threading Pattern**
- Notifications can reference parent (replyTo)
- Enables conversation threads
- Use case: Decision discussions

---

## Security & Access Control

### Channel-Level Permissions

```javascript
{
  "permissions": {
    "publish": ["dev", "consulting"],      // Who can publish
    "subscribe": ["dev", "consulting", "business"],  // Who can subscribe
    "admin": ["dev"]                      // Who can manage channel
  }
}
```

### Notification-Level Visibility

```javascript
{
  "visibility": {
    "teams": ["dev", "consulting"],       // Team-based filtering
    "private": false,                     // Private notifications
    "allowedUsers": ["user-123"]          // User-specific access
  }
}
```

### Authentication (Future)

- Client authentication via MCP capabilities
- API tokens or OAuth integration
- Role-based access control (RBAC)

---

## Scalability Considerations

### Phase 1: Single Server (MVP)
- In-memory storage
- Single server instance
- stdio/HTTP transport
- Supports 10-100 concurrent clients

### Phase 2: Persistent Storage
- File-based or Redis storage
- Notification history
- Subscription persistence
- Supports 100-1000 clients

### Phase 3: Distributed (Future)
- Multiple server instances
- Redis Pub-Sub backend
- Load balancing
- Horizontal scaling
- Supports 1000+ clients

---

## Technology Stack

### Language Options
1. **Node.js/TypeScript** (Recommended)
   - Excellent MCP SDK support
   - Strong async/event-driven model
   - Large ecosystem

2. **Python**
   - Good MCP SDK
   - Strong data processing
   - ML/AI integration potential

3. **Go**
   - High performance
   - Native concurrency
   - Small footprint

### Dependencies
- MCP SDK (@modelcontextprotocol/sdk)
- JSON Schema validator (ajv, jsonschema)
- WebSocket library (ws, socket.io)
- Storage adapter (redis, sqlite, etc.)

---

## Deployment Modes

### 1. **Standalone Server**
```
mcp-server --transport stdio
mcp-server --transport http --port 3000
mcp-server --transport ws --port 8080
```

### 2. **Embedded Mode**
- Library integration
- Run within application
- Direct API access

### 3. **Cloud Deployment**
- Docker container
- Kubernetes pod
- Serverless function (future)

---

## Configuration

### Server Configuration

```json
{
  "server": {
    "name": "notify-mcp",
    "version": "1.0.0",
    "transport": "stdio",
    "host": "localhost",
    "port": 3000
  },
  "storage": {
    "type": "memory",
    "path": "./data",
    "ttl": 86400
  },
  "notifications": {
    "maxHistoryPerChannel": 1000,
    "defaultExpiry": 604800,
    "enablePersistence": false
  },
  "security": {
    "requireAuth": false,
    "allowAnonymous": true
  }
}
```

---

## MCP Capabilities

### Server Capabilities
```json
{
  "capabilities": {
    "notifications": {
      "supported": true,
      "channels": true,
      "filters": true,
      "persistence": false
    }
  }
}
```

---

## Error Handling

### Error Types
- `INVALID_SCHEMA`: Notification doesn't match schema
- `CHANNEL_NOT_FOUND`: Target channel doesn't exist
- `PERMISSION_DENIED`: Client lacks permission
- `RATE_LIMIT_EXCEEDED`: Too many notifications
- `INVALID_FILTER`: Subscription filter invalid

### Error Response Format
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Invalid notification schema",
    "data": {
      "schemaErrors": [...]
    }
  },
  "id": "request-123"
}
```

---

## Monitoring & Observability

### Metrics to Track
- Active connections
- Subscriptions per channel
- Notifications published per channel
- Delivery success rate
- Average latency
- Error rates

### Logging
- Notification events
- Subscription changes
- Errors and exceptions
- Performance metrics

---

## Future Enhancements

### Phase 2
- [ ] Persistent storage (Redis/PostgreSQL)
- [ ] Notification history API
- [ ] Search and filtering
- [ ] Authentication system

### Phase 3
- [ ] Distributed architecture
- [ ] Load balancing
- [ ] High availability
- [ ] Rate limiting

### Phase 4
- [ ] Web UI for management
- [ ] Analytics dashboard
- [ ] Integration webhooks
- [ ] AI-powered notification summarization

---

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Pub-Sub Pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)
