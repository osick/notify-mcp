# MCP Server Primitives: Tools, Resources, and Prompts

## Overview

The Model Context Protocol (MCP) defines three core primitives that servers can expose to clients. This document explains how to define and implement these primitives in the Notify-MCP server.

**Specification Version:** 2025-06-18
**Protocol:** JSON-RPC 2.0

---

## The Three Primitives

### 1. **Tools** (Model-controlled)
**Definition:** Executable functions that perform actions or computations.

**Control:** The AI model decides when to invoke tools based on user requests.

**Purpose:** Enable the AI to interact with external systems, perform operations, and modify state.

**Examples in Notify-MCP:**
- `publish_notification`: Publish a notification to a channel
- `create_channel`: Create a new notification channel
- `subscribe_to_channel`: Subscribe to notifications

---

### 2. **Resources** (Application-controlled)
**Definition:** Data sources that provide context to the AI without side effects.

**Control:** The application (client) provides these as context to the model.

**Purpose:** Give the AI access to data for reading and understanding.

**Examples in Notify-MCP:**
- `notification://project-alpha/recent`: Recent notifications from a channel
- `channel://project-alpha/info`: Channel information and metadata
- `subscription://my-subscriptions`: Current user's subscriptions

---

### 3. **Prompts** (User-controlled)
**Definition:** Pre-defined templates that guide AI interactions.

**Control:** The user explicitly selects which prompts to use.

**Purpose:** Provide reusable templates for common workflows and interactions.

**Examples in Notify-MCP:**
- `create_decision_notification`: Template for architecture decisions
- `send_alert`: Template for critical alerts
- `start_discussion`: Template for team discussions

---

## Tools Definition

### Tool Structure

```json
{
  "name": "publish_notification",
  "title": "Publish Notification",
  "description": "Publish a notification to a channel",
  "inputSchema": {
    "type": "object",
    "properties": {
      "channel": {
        "type": "string",
        "description": "Target channel name"
      },
      "title": {
        "type": "string",
        "description": "Notification title"
      },
      "body": {
        "type": "string",
        "description": "Notification body"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "critical"],
        "description": "Priority level"
      },
      "theme": {
        "type": "string",
        "enum": ["architecture-decision", "state-update", "alert", "question", "discussion"],
        "description": "Notification theme"
      }
    },
    "required": ["channel", "title", "body"]
  }
}
```

### Tool Methods

#### List Tools
**Method:** `tools/list`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": "tools-1"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "publish_notification",
        "title": "Publish Notification",
        "description": "Publish a notification to a channel",
        "inputSchema": { /* JSON Schema */ }
      },
      {
        "name": "subscribe_to_channel",
        "title": "Subscribe to Channel",
        "description": "Subscribe to notifications from a channel",
        "inputSchema": { /* JSON Schema */ }
      }
    ]
  },
  "id": "tools-1"
}
```

#### Call Tool
**Method:** `tools/call`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "publish_notification",
    "arguments": {
      "channel": "project-alpha",
      "title": "Database Migration Decided",
      "body": "Team decided on Blue-Green deployment",
      "priority": "high",
      "theme": "architecture-decision"
    }
  },
  "id": "call-1"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Notification published successfully to project-alpha. Notification ID: notif-7b8e9f10, delivered to 5 subscribers."
      }
    ]
  },
  "id": "call-1"
}
```

### Notify-MCP Tools

#### 1. `publish_notification`
Publish a notification to a channel.

**Input:**
- `channel` (required): Target channel
- `title` (required): Notification title
- `body` (required): Notification content
- `priority`: Priority level (default: medium)
- `theme`: Notification theme
- `tags`: Array of tags
- `format`: Content format (text/markdown/json)

**Output:** Notification ID and delivery status

---

#### 2. `subscribe_to_channel`
Subscribe to a notification channel.

**Input:**
- `channel` (required): Channel to subscribe to
- `priority_filter`: Filter by priority
- `tag_filter`: Filter by tags
- `theme_filter`: Filter by themes

**Output:** Subscription confirmation and ID

---

#### 3. `unsubscribe_from_channel`
Unsubscribe from a channel.

**Input:**
- `channel` (required): Channel to unsubscribe from

**Output:** Unsubscribe confirmation

---

#### 4. `list_channels`
List available channels.

**Input:**
- `filter_tags`: Optional tag filter

**Output:** Array of channel information

---

#### 5. `create_channel`
Create a new notification channel.

**Input:**
- `channel_id` (required): Unique channel identifier
- `name` (required): Display name
- `description`: Channel description
- `permissions`: Access control settings

**Output:** Channel creation confirmation

---

#### 6. `get_my_subscriptions`
Get current user's subscriptions.

**Input:** None

**Output:** Array of subscription details

---

## Resources Definition

### Resource Structure

Resources are identified by URI:
```
<scheme>://<path>
```

**Examples:**
- `notification://project-alpha/recent`
- `channel://project-alpha/info`
- `subscription://my-subscriptions`

### Resource Methods

#### List Resources
**Method:** `resources/list`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "id": "res-1"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "resources": [
      {
        "uri": "notification://project-alpha/recent",
        "name": "Recent Notifications - Project Alpha",
        "description": "Last 50 notifications from Project Alpha channel",
        "mimeType": "application/json"
      },
      {
        "uri": "channel://project-alpha/info",
        "name": "Project Alpha Channel Info",
        "description": "Metadata and statistics for Project Alpha channel",
        "mimeType": "application/json"
      }
    ]
  },
  "id": "res-1"
}
```

#### Read Resource
**Method:** `resources/read`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "resources/read",
  "params": {
    "uri": "notification://project-alpha/recent"
  },
  "id": "read-1"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "contents": [
      {
        "uri": "notification://project-alpha/recent",
        "mimeType": "application/json",
        "text": "[{\"id\": \"notif-1\", \"title\": \"...\", ...}, ...]"
      }
    ]
  },
  "id": "read-1"
}
```

### Notify-MCP Resources

#### 1. `notification://<channel>/recent`
Recent notifications from a channel.

**Returns:** Last 50 notifications (JSON array)

**Example:**
```json
[
  {
    "id": "notif-7b8e9f10",
    "title": "Database Migration Decided",
    "priority": "high",
    "timestamp": "2025-10-11T14:30:00Z",
    ...
  }
]
```

---

#### 2. `channel://<channel>/info`
Channel information and metadata.

**Returns:** Channel details (JSON object)

**Example:**
```json
{
  "id": "project-alpha",
  "name": "Project Alpha",
  "subscriberCount": 12,
  "notificationCount": 156,
  "permissions": {...}
}
```

---

#### 3. `subscription://my-subscriptions`
Current user's subscriptions.

**Returns:** Array of subscription details

---

#### 4. `notification://<channel>/history?days=7`
Historical notifications from a channel.

**Parameters:**
- `days`: Number of days to look back

**Returns:** Notification history

---

## Prompts Definition

### Prompt Structure

```json
{
  "name": "create_decision_notification",
  "title": "Create Architecture Decision Notification",
  "description": "Template for broadcasting architecture decisions to the team",
  "arguments": [
    {
      "name": "decision_title",
      "description": "Brief title of the decision",
      "required": true
    },
    {
      "name": "context",
      "description": "Background and context for the decision",
      "required": true
    },
    {
      "name": "decision",
      "description": "The decision that was made",
      "required": true
    }
  ]
}
```

### Prompt Methods

#### List Prompts
**Method:** `prompts/list`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompts/list",
  "id": "prompt-1"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "prompts": [
      {
        "name": "create_decision_notification",
        "title": "Create Architecture Decision",
        "description": "Template for architecture decisions",
        "arguments": [...]
      },
      {
        "name": "send_alert",
        "title": "Send Critical Alert",
        "description": "Template for critical alerts",
        "arguments": [...]
      }
    ]
  },
  "id": "prompt-1"
}
```

#### Get Prompt
**Method:** `prompts/get`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompts/get",
  "params": {
    "name": "create_decision_notification",
    "arguments": {
      "decision_title": "Blue-Green Database Migration",
      "context": "Need zero-downtime deployments",
      "decision": "Implement Blue-Green deployment strategy"
    }
  },
  "id": "get-1"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please create an architecture decision notification with the following details:\n\nTitle: Blue-Green Database Migration\n\nContext: Need zero-downtime deployments\n\nDecision: Implement Blue-Green deployment strategy\n\nFormat this as a professional team notification with consequences and next steps."
        }
      }
    ]
  },
  "id": "get-1"
}
```

### Notify-MCP Prompts

#### 1. `create_decision_notification`
Template for architecture/design decisions.

**Arguments:**
- `decision_title`: Brief title
- `context`: Background
- `decision`: What was decided
- `consequences`: Optional consequences
- `next_steps`: Optional next steps

**Output:** Formatted message for publishing decision

---

#### 2. `send_alert`
Template for critical alerts.

**Arguments:**
- `alert_title`: Alert title
- `severity`: Severity level
- `impact`: Impact description
- `action_required`: Required actions

**Output:** Formatted alert notification

---

#### 3. `start_discussion`
Template for starting team discussions.

**Arguments:**
- `topic`: Discussion topic
- `question`: Question to pose
- `context`: Background context
- `options`: Optional list of options

**Output:** Formatted discussion starter

---

#### 4. `sync_memory`
Template for sharing AI conversation insights.

**Arguments:**
- `insight_title`: Title of the insight
- `source_ai`: AI tool used (Claude/ChatGPT/Gemini)
- `conversation_summary`: Summary of relevant conversation
- `key_points`: Key takeaways
- `impact`: How this affects the team

**Output:** Formatted memory sync notification

---

#### 5. `milestone_update`
Template for project milestone notifications.

**Arguments:**
- `milestone_name`: Milestone title
- `achievements`: List of achievements
- `metrics`: Optional metrics/stats
- `next_focus`: What's next

**Output:** Formatted milestone update

---

## Capability Declaration

MCP servers must declare which primitives they support during initialization:

```json
{
  "capabilities": {
    "tools": {
      "listChanged": true
    },
    "resources": {
      "subscribe": true,
      "listChanged": true
    },
    "prompts": {
      "listChanged": true
    }
  }
}
```

---

## Security Considerations

### Tools
- **Require user approval** for destructive operations
- Validate all inputs against schema
- Implement rate limiting
- Log all tool invocations

### Resources
- Implement access controls
- Validate resource URIs
- Prevent resource enumeration attacks
- Rate limit resource reads

### Prompts
- Sanitize all prompt arguments
- Prevent injection attacks
- Validate argument types
- Limit prompt complexity

---

## Implementation Example

### TypeScript MCP Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({
  name: "notify-mcp",
  version: "1.0.0"
}, {
  capabilities: {
    tools: { listChanged: true },
    resources: { subscribe: true, listChanged: true },
    prompts: { listChanged: true }
  }
});

// Register tools
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "publish_notification",
      title: "Publish Notification",
      description: "Publish a notification to a channel",
      inputSchema: { /* ... */ }
    }
  ]
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "publish_notification") {
    // Handle notification publishing
    return {
      content: [{
        type: "text",
        text: "Notification published successfully"
      }]
    };
  }
});

// Register resources
server.setRequestHandler("resources/list", async () => ({
  resources: [
    {
      uri: "notification://project-alpha/recent",
      name: "Recent Notifications - Project Alpha",
      mimeType: "application/json"
    }
  ]
}));

server.setRequestHandler("resources/read", async (request) => {
  const { uri } = request.params;

  // Fetch and return resource data
  return {
    contents: [{
      uri,
      mimeType: "application/json",
      text: JSON.stringify(data)
    }]
  };
});

// Register prompts
server.setRequestHandler("prompts/list", async () => ({
  prompts: [
    {
      name: "create_decision_notification",
      title: "Create Architecture Decision",
      arguments: [/* ... */]
    }
  ]
}));

server.setRequestHandler("prompts/get", async (request) => {
  const { name, arguments: args } = request.params;

  // Generate prompt message
  return {
    messages: [{
      role: "user",
      content: {
        type: "text",
        text: generatePromptText(args)
      }
    }]
  };
});
```

---

## Comparison: Tools vs Resources vs Prompts

| Aspect | Tools | Resources | Prompts |
|--------|-------|-----------|---------|
| **Control** | Model-controlled | App-controlled | User-controlled |
| **Purpose** | Perform actions | Provide context | Guide interactions |
| **Side Effects** | Yes | No | No |
| **Invocation** | AI decides | AI reads as needed | User selects |
| **Examples** | publish, create, delete | Recent notifications, channel info | Decision template, alert template |
| **Security** | User approval needed | Access controls | Input sanitization |

---

## References

- [MCP Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/)
- [MCP Tools Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [MCP Resources Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)
- [MCP Prompts Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)
