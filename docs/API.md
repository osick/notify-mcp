# Notify-MCP Server API Documentation

## Overview

This document defines the MCP server API for the Notify-MCP notification system. All communication uses JSON-RPC 2.0 over the Model Context Protocol.

**Protocol:** MCP (Model Context Protocol)
**Message Format:** JSON-RPC 2.0
**Transport Options:** stdio, HTTP, WebSocket

---

## MCP Server Information

### Server Metadata

```json
{
  "name": "notify-mcp",
  "version": "1.0.0",
  "description": "Team notification server for genAI collaboration",
  "capabilities": {
    "notifications": {
      "supported": true,
      "channels": true,
      "filters": true,
      "history": false
    }
  }
}
```

---

## API Methods

### 1. Initialize

**Method:** `initialize`
**Description:** Initialize MCP connection and negotiate capabilities
**Required by:** MCP Protocol

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "1.0",
    "clientInfo": {
      "name": "claude-client",
      "version": "1.0.0"
    },
    "capabilities": {
      "notifications": {
        "supported": true
      }
    }
  },
  "id": "init-1"
}
```

#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "1.0",
    "serverInfo": {
      "name": "notify-mcp",
      "version": "1.0.0"
    },
    "capabilities": {
      "notifications": {
        "supported": true,
        "channels": true,
        "filters": true
      }
    }
  },
  "id": "init-1"
}
```

---

### 2. Subscribe to Channel

**Method:** `notifications/subscribe`
**Description:** Subscribe to a notification channel with optional filters

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/subscribe",
  "params": {
    "channel": "project-alpha",
    "filters": {
      "priority": ["high", "critical"],
      "tags": ["backend", "security"],
      "themes": ["architecture-decision", "alert"],
      "roles": ["dev"]
    }
  },
  "id": "sub-1"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel` | string | Yes | Channel name to subscribe to |
| `filters` | object | No | Filter criteria (see below) |

#### Filter Options

| Filter | Type | Description | Example |
|--------|------|-------------|---------|
| `priority` | array[string] | Priority levels | `["high", "critical"]` |
| `tags` | array[string] | Tag matching | `["backend", "security"]` |
| `themes` | array[string] | Notification themes | `["decision", "alert"]` |
| `roles` | array[string] | Sender roles | `["dev", "consulting"]` |
| `senders` | array[string] | Specific sender IDs | `["user-123"]` |

#### Response (Success)
```json
{
  "jsonrpc": "2.0",
  "result": {
    "subscribed": true,
    "channel": "project-alpha",
    "subscriptionId": "sub-7b8e9f10",
    "subscribedAt": "2025-10-11T14:30:00Z",
    "subscriberCount": 5
  },
  "id": "sub-1"
}
```

#### Response (Error)
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32001,
    "message": "Channel not found",
    "data": {
      "channel": "project-alpha"
    }
  },
  "id": "sub-1"
}
```

---

### 3. Unsubscribe from Channel

**Method:** `notifications/unsubscribe`
**Description:** Unsubscribe from a notification channel

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/unsubscribe",
  "params": {
    "channel": "project-alpha"
  },
  "id": "unsub-1"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel` | string | Yes | Channel name to unsubscribe from |

#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "unsubscribed": true,
    "channel": "project-alpha"
  },
  "id": "unsub-1"
}
```

---

### 4. Publish Notification

**Method:** `notifications/publish`
**Description:** Publish a notification to a channel

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/publish",
  "params": {
    "channel": "project-alpha",
    "notification": {
      "schemaVersion": "1.0.0",
      "sender": {
        "id": "user-alice-123",
        "name": "Alice Developer",
        "role": "dev",
        "aiTool": "claude"
      },
      "context": {
        "theme": "architecture-decision",
        "priority": "high",
        "tags": ["backend", "database"],
        "projectId": "proj-456"
      },
      "information": {
        "title": "Database Migration Strategy",
        "body": "Team decided to use Blue-Green deployment...",
        "format": "markdown"
      },
      "actions": [
        {
          "type": "review",
          "label": "Review Decision",
          "url": "https://wiki.example.com/decision"
        }
      ],
      "visibility": {
        "teams": ["dev", "consulting"]
      }
    }
  },
  "id": "pub-1"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel` | string | Yes | Target channel name |
| `notification` | object | Yes | Notification object (see schema) |

#### Response (Success)
```json
{
  "jsonrpc": "2.0",
  "result": {
    "published": true,
    "notificationId": "notif-7b8e9f10",
    "channel": "project-alpha",
    "timestamp": "2025-10-11T14:30:00Z",
    "deliveredTo": 5,
    "metadata": {
      "id": "notif-7b8e9f10",
      "sequence": 42
    }
  },
  "id": "pub-1"
}
```

#### Response (Error - Invalid Schema)
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32002,
    "message": "Invalid notification schema",
    "data": {
      "schemaErrors": [
        {
          "field": "sender.role",
          "error": "must be one of: dev, consulting, business, other"
        }
      ]
    }
  },
  "id": "pub-1"
}
```

---

### 5. List Channels

**Method:** `notifications/channels/list`
**Description:** Get list of available channels

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/channels/list",
  "params": {
    "filter": {
      "tags": ["active"],
      "permissions": "subscribe"
    }
  },
  "id": "list-1"
}
```

#### Parameters (All Optional)

| Parameter | Type | Description |
|-----------|------|-------------|
| `filter.tags` | array[string] | Filter by channel tags |
| `filter.permissions` | string | Filter by permission: `subscribe`, `publish`, `admin` |

#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "channels": [
      {
        "id": "project-alpha",
        "name": "Project Alpha",
        "description": "Notifications for Project Alpha team",
        "subscriberCount": 12,
        "createdAt": "2025-10-01T10:00:00Z",
        "permissions": {
          "subscribe": ["dev", "consulting", "business"],
          "publish": ["dev", "consulting"]
        },
        "metadata": {
          "projectId": "proj-456",
          "tags": ["active", "high-priority"]
        }
      },
      {
        "id": "general",
        "name": "General Announcements",
        "description": "General team announcements",
        "subscriberCount": 45,
        "createdAt": "2025-09-15T08:00:00Z",
        "permissions": {
          "subscribe": ["all"],
          "publish": ["admin"]
        }
      }
    ],
    "total": 2
  },
  "id": "list-1"
}
```

---

### 6. Create Channel

**Method:** `notifications/channels/create`
**Description:** Create a new notification channel

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/channels/create",
  "params": {
    "channel": {
      "id": "project-beta",
      "name": "Project Beta",
      "description": "Notifications for Project Beta team",
      "permissions": {
        "subscribe": ["dev", "consulting", "business"],
        "publish": ["dev"],
        "admin": ["dev"]
      },
      "metadata": {
        "projectId": "proj-789",
        "tags": ["new", "active"]
      }
    }
  },
  "id": "create-1"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel.id` | string | Yes | Unique channel identifier |
| `channel.name` | string | Yes | Display name |
| `channel.description` | string | No | Channel description |
| `channel.permissions` | object | Yes | Access control settings |
| `channel.metadata` | object | No | Additional metadata |

#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "created": true,
    "channel": {
      "id": "project-beta",
      "name": "Project Beta",
      "createdAt": "2025-10-11T14:35:00Z",
      "createdBy": "user-alice-123"
    }
  },
  "id": "create-1"
}
```

---

### 7. Delete Channel

**Method:** `notifications/channels/delete`
**Description:** Delete a notification channel

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/channels/delete",
  "params": {
    "channel": "project-beta"
  },
  "id": "del-1"
}
```

#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "deleted": true,
    "channel": "project-beta",
    "unsubscribedClients": 5
  },
  "id": "del-1"
}
```

---

### 8. Get Channel Info

**Method:** `notifications/channels/info`
**Description:** Get detailed information about a channel

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/channels/info",
  "params": {
    "channel": "project-alpha"
  },
  "id": "info-1"
}
```

#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "channel": {
      "id": "project-alpha",
      "name": "Project Alpha",
      "description": "Notifications for Project Alpha team",
      "createdAt": "2025-10-01T10:00:00Z",
      "createdBy": "user-admin-1",
      "subscriberCount": 12,
      "notificationCount": 156,
      "lastNotificationAt": "2025-10-11T14:25:00Z",
      "permissions": {
        "subscribe": ["dev", "consulting", "business"],
        "publish": ["dev", "consulting"],
        "admin": ["dev"]
      },
      "metadata": {
        "projectId": "proj-456",
        "tags": ["active", "high-priority"]
      }
    }
  },
  "id": "info-1"
}
```

---

### 9. List My Subscriptions

**Method:** `notifications/subscriptions/list`
**Description:** Get current client's subscriptions

#### Request
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/subscriptions/list",
  "params": {},
  "id": "mysubs-1"
}
```

#### Response
```json
{
  "jsonrpc": "2.0",
  "result": {
    "subscriptions": [
      {
        "channel": "project-alpha",
        "subscriptionId": "sub-7b8e9f10",
        "subscribedAt": "2025-10-11T14:00:00Z",
        "filters": {
          "priority": ["high", "critical"],
          "tags": ["backend"]
        }
      },
      {
        "channel": "general",
        "subscriptionId": "sub-8c9fa01",
        "subscribedAt": "2025-10-10T09:00:00Z",
        "filters": {}
      }
    ],
    "total": 2
  },
  "id": "mysubs-1"
}
```

---

## Server-to-Client Notifications

### Notification Delivery

**Method:** `notifications/message` (server-initiated)
**Description:** Server sends notification to subscribed client

#### Notification
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/message",
  "params": {
    "channel": "project-alpha",
    "notification": {
      "schemaVersion": "1.0.0",
      "sender": {
        "id": "user-alice-123",
        "name": "Alice Developer",
        "role": "dev",
        "aiTool": "claude"
      },
      "context": {
        "theme": "architecture-decision",
        "priority": "high",
        "tags": ["backend", "database"],
        "projectId": "proj-456"
      },
      "information": {
        "title": "Database Migration Strategy",
        "body": "Team decided to use Blue-Green deployment for database migration...",
        "format": "markdown"
      },
      "metadata": {
        "id": "notif-7b8e9f10",
        "timestamp": "2025-10-11T14:30:00Z",
        "channel": "project-alpha",
        "sequence": 42
      },
      "actions": [
        {
          "type": "review",
          "label": "Review Decision",
          "url": "https://wiki.example.com/decision"
        }
      ],
      "visibility": {
        "teams": ["dev", "consulting"]
      }
    }
  }
}
```

**Note:** This is a one-way notification from server to client. No response expected.

---

## Error Codes

### Standard JSON-RPC Errors

| Code | Message | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | Request format invalid |
| -32601 | Method not found | Unknown method |
| -32602 | Invalid params | Parameter validation failed |
| -32603 | Internal error | Server internal error |

### Custom Application Errors

| Code | Message | Description |
|------|---------|-------------|
| -32001 | Channel not found | Requested channel doesn't exist |
| -32002 | Invalid notification schema | Notification doesn't match schema |
| -32003 | Permission denied | Client lacks required permission |
| -32004 | Already subscribed | Already subscribed to channel |
| -32005 | Not subscribed | Not subscribed to channel |
| -32006 | Channel already exists | Channel ID already in use |
| -32007 | Rate limit exceeded | Too many requests |
| -32008 | Invalid filter | Subscription filter is invalid |

---

## Usage Examples

### Example 1: Simple Subscribe and Receive

```javascript
// 1. Initialize connection
await client.initialize();

// 2. Subscribe to channel
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha"
  }
});

// 3. Handle incoming notifications
client.onNotification("notifications/message", (notification) => {
  console.log("Received:", notification.params.notification);
});
```

### Example 2: Publish with Filters

```javascript
// 1. Subscribe with filters (dev team only, high priority)
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      priority: ["high", "critical"],
      roles: ["dev"]
    }
  }
});

// 2. Publish notification
await client.request({
  method: "notifications/publish",
  params: {
    channel: "project-alpha",
    notification: {
      schemaVersion: "1.0.0",
      sender: {
        id: "user-alice",
        name: "Alice",
        role: "dev"
      },
      context: {
        theme: "alert",
        priority: "high"
      },
      information: {
        title: "Build Failed",
        body: "Main branch build failed on commit abc123"
      }
    }
  }
});
```

### Example 3: Create Custom Channel

```javascript
// Create a project-specific channel
await client.request({
  method: "notifications/channels/create",
  params: {
    channel: {
      id: "security-alerts",
      name: "Security Alerts",
      description: "Critical security notifications",
      permissions: {
        subscribe: ["dev", "consulting", "business"],
        publish: ["dev"],
        admin: ["dev"]
      },
      metadata: {
        tags: ["security", "critical"]
      }
    }
  }
});
```

---

## Rate Limits

### Default Limits (Configurable)

| Operation | Limit | Window |
|-----------|-------|--------|
| Publish notification | 100 | per minute |
| Subscribe | 20 | per minute |
| Unsubscribe | 20 | per minute |
| List channels | 60 | per minute |
| Create channel | 10 | per hour |

**Rate Limit Response:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32007,
    "message": "Rate limit exceeded",
    "data": {
      "limit": 100,
      "window": "60s",
      "retryAfter": "2025-10-11T14:35:00Z"
    }
  },
  "id": "pub-1"
}
```

---

## Transport-Specific Details

### stdio Transport
- Use for local MCP clients (Claude Desktop, etc.)
- Request/response via stdin/stdout
- One client per process

### HTTP Transport
- RESTful-style over HTTP POST
- Supports multiple concurrent clients
- Endpoint: `http://localhost:3000/mcp`

### WebSocket Transport
- Real-time bidirectional communication
- Best for web clients
- Endpoint: `ws://localhost:8080/mcp`

---

## Versioning

### API Versioning
- Current version: `1.0.0`
- Version negotiated during `initialize`
- Backward compatibility maintained within major version

### Schema Versioning
- Notification schema versioned separately
- Schema version in each notification: `schemaVersion`
- Multiple schema versions supported simultaneously

---

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Notification Schema Documentation](./NOTIFICATION_SCHEMA.md)
- [Architecture Documentation](./ARCHITECTURE.md)
