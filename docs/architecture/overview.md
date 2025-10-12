# Architecture Overview

Notify-MCP is a pub-sub notification system built on the Model Context Protocol (MCP).

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Clients                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Claude  │  │ ChatGPT  │  │  Gemini  │  │  Custom  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┴──────────────┴─────────────┴──────────────┴─────────┘
        │              │             │              │
        └──────────────┴─────────────┴──────────────┘
                       │
        ┌──────────────▼──────────────────────┐
        │    Notify-MCP Server                │
        │                                     │
        │  ┌─────────────────────────────┐   │
        │  │  MCP Protocol Handler       │   │
        │  └─────────────────────────────┘   │
        │  ┌─────────────────────────────┐   │
        │  │  Core Services              │   │
        │  │  • Subscription Manager     │   │
        │  │  • Notification Router      │   │
        │  │  • Channel Manager          │   │
        │  └─────────────────────────────┘   │
        │  ┌─────────────────────────────┐   │
        │  │  Storage Layer              │   │
        │  │  • In-Memory / SQLite       │   │
        │  └─────────────────────────────┘   │
        └─────────────────────────────────────┘
```

---

## Key Components

### MCP Protocol Handler
- Handles JSON-RPC 2.0 over stdio
- Routes requests to appropriate services
- Delivers notifications to subscribed clients

### Subscription Manager
- Manages client subscriptions to channels
- Applies filters (priority, tags, themes, roles)
- Tracks subscription metadata

### Notification Router
- Routes published notifications to subscribers
- Applies filters for each subscriber
- Tracks delivery status

### Channel Manager
- Creates and manages notification channels
- Enforces permissions
- Maintains channel metadata

### Storage Layer
- **In-Memory**: Fast, not persistent
- **SQLite**: Persistent, enables team collaboration
- Pluggable architecture for future backends

---

## Data Flow

### Publishing a Notification

```
Publisher → MCP Handler → Validator → Router → Subscribers
```

1. Client publishes notification
2. MCP handler receives request
3. Validator checks schema
4. Router identifies subscribers
5. Filters applied per subscriber
6. Notification delivered

---

## Communication Patterns

### Broadcast
- Publisher sends to channel
- All subscribers receive
- No filtering

### Filtered
- Publisher sends to channel
- Only matching subscribers receive
- Filters: priority, tags, themes, roles

### Threaded
- Notifications can reference parents
- Enables conversation threads

---

## Complete Architecture Documentation

For detailed architecture documentation, see:

**[Complete Architecture Guide](../ARCHITECTURE.md)**

Includes:
- Component diagrams
- Data flow details
- Storage architecture
- Scalability considerations
- Technology stack details

---

## Related

- [Storage Architecture](storage.md)
- [Pub-Sub Model](pub-sub-model.md)
- [Storage Configuration](../guides/storage-configuration.md)
