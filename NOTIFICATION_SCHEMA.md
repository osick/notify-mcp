# Notification Schema Documentation

## Overview

The Team Notification Schema is an extensible, version-based schema designed for team collaboration across genAI platforms (ChatGPT, Claude, Gemini). It enables dev, consulting, and business teams to share work state, decisions, and memory through structured notifications.

**Current Version:** 1.0.0
**Schema File:** `schemas/notification-schema.json`

---

## Design Principles

### 1. **Extensibility**
- All major sections support `additionalProperties: true`
- New fields can be added without breaking existing implementations
- Custom extensions can be namespace-prefixed (e.g., `x-custom-field`)

### 2. **Versioning**
- Every notification includes `schemaVersion` field
- Follows semantic versioning (MAJOR.MINOR.PATCH)
- Enables backward compatibility and graceful degradation
- Consumers can handle multiple schema versions

### 3. **Separation of Concerns**
- **Core fields** (sender, context, information): User-provided content
- **Metadata**: System-generated tracking information
- **Extensions** (actions, visibility): Optional enhanced functionality

### 4. **JSON-RPC 2.0 Compatible**
- Designed to work with MCP protocol's notification system
- Lightweight and efficient for real-time communication
- Standard JSON format for interoperability

---

## Schema Structure

```json
{
  "schemaVersion": "1.0.0",
  "sender": { ... },
  "context": { ... },
  "information": { ... },
  "metadata": { ... },
  "actions": [ ... ],
  "visibility": { ... }
}
```

---

## Field Definitions

### **schemaVersion** (required)
- **Type:** String (semantic version pattern)
- **Description:** Schema version for backward compatibility
- **Example:** `"1.0.0"`
- **Usage:** Always check this field to ensure compatibility

---

### **sender** (required)
Information about who is sending the notification.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the sender |
| `name` | string | Yes | Display name of the sender |
| `role` | enum | Yes | Team role: `dev`, `consulting`, `business`, `other` |
| `aiTool` | enum | No | AI tool used: `claude`, `chatgpt`, `gemini`, `other` |
| `email` | email | No | Sender's email address |

**Extensible:** Additional custom fields allowed.

**Example:**
```json
{
  "sender": {
    "id": "user-123",
    "name": "Alice Developer",
    "role": "dev",
    "aiTool": "claude",
    "email": "alice@example.com"
  }
}
```

---

### **context** (required)
Contextual metadata about the notification.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `theme` | enum | Yes | Notification category (see themes below) |
| `priority` | enum | Yes | Priority level: `low`, `medium`, `high`, `critical` |
| `validity` | date-time | No | Expiration timestamp (ISO 8601) |
| `tags` | array[string] | No | Tags for filtering/categorization |
| `relatedConversationId` | string | No | ID of related AI conversation |
| `projectId` | string | No | Associated project identifier |

**Themes:**
- `architecture-decision`: Architecture and design decisions
- `state-update`: Project or system state changes
- `memory-sync`: Shared context/memory updates
- `question`: Questions needing response
- `decision`: General decisions
- `alert`: Important alerts
- `info`: Informational messages
- `discussion`: Discussion topics

**Extensible:** Additional custom fields allowed.

**Example:**
```json
{
  "context": {
    "theme": "architecture-decision",
    "priority": "high",
    "validity": "2025-10-18T10:00:00Z",
    "tags": ["backend", "database", "migration"],
    "projectId": "project-alpha"
  }
}
```

---

### **information** (required)
The actual notification content.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Short notification title (max 200 chars) |
| `body` | string | Yes | Detailed notification content |
| `format` | enum | No | Content format: `text`, `markdown`, `json`, `html` (default: `text`) |
| `attachments` | array | No | Optional attachments (links, files, images) |

**Attachment Structure:**
```json
{
  "type": "link",
  "url": "https://example.com/doc",
  "name": "Architecture Diagram"
}
```

**Extensible:** Additional custom fields allowed.

**Example:**
```json
{
  "information": {
    "title": "Database Migration Strategy Decided",
    "body": "After team discussion, we decided to use Blue-Green deployment for the database migration...",
    "format": "markdown",
    "attachments": [
      {
        "type": "link",
        "url": "https://wiki.example.com/migration-plan",
        "name": "Full Migration Plan"
      }
    ]
  }
}
```

---

### **metadata** (required)
System-generated metadata for tracking and management.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique notification identifier (UUID recommended) |
| `timestamp` | date-time | Yes | Creation timestamp (ISO 8601) |
| `version` | string | No | Message version for updates |
| `channel` | string | No | Pub-Sub channel name |
| `replyTo` | string | No | Parent notification ID (for threading) |
| `sequence` | integer | No | Sequence number for ordering |

**Extensible:** Additional custom fields allowed.

**Example:**
```json
{
  "metadata": {
    "id": "notif-7b8e9f10",
    "timestamp": "2025-10-11T14:30:00Z",
    "channel": "project-alpha",
    "sequence": 42
  }
}
```

---

### **actions** (optional)
Suggested actions that recipients can take.

**Structure:**
```json
{
  "actions": [
    {
      "type": "acknowledge|respond|review|approve|reject|custom",
      "label": "Action Button Label",
      "url": "https://...",
      "data": { /* custom data */ }
    }
  ]
}
```

**Example:**
```json
{
  "actions": [
    {
      "type": "review",
      "label": "Review Decision Document",
      "url": "https://docs.example.com/decision-123"
    },
    {
      "type": "acknowledge",
      "label": "Mark as Read"
    }
  ]
}
```

---

### **visibility** (optional)
Access control settings for the notification.

| Field | Type | Description |
|-------|------|-------------|
| `teams` | array[enum] | Teams with access: `dev`, `consulting`, `business`, `all` |
| `private` | boolean | Whether notification is private (default: false) |
| `allowedUsers` | array[string] | Specific user IDs with access (if private) |

**Extensible:** Additional custom fields allowed.

**Example:**
```json
{
  "visibility": {
    "teams": ["dev", "consulting"],
    "private": false
  }
}
```

---

## Complete Example

```json
{
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
    "validity": "2025-10-18T10:00:00Z",
    "tags": ["backend", "database", "migration"],
    "projectId": "project-alpha",
    "relatedConversationId": "conv-456"
  },
  "information": {
    "title": "Database Migration Strategy Decided",
    "body": "After analyzing options, the team decided to use Blue-Green deployment strategy for the database migration. This minimizes downtime and provides easy rollback capabilities.",
    "format": "markdown",
    "attachments": [
      {
        "type": "link",
        "url": "https://wiki.example.com/migration-plan",
        "name": "Detailed Migration Plan"
      }
    ]
  },
  "metadata": {
    "id": "notif-7b8e9f10-c5a3-4d8e-9f12-3a4b5c6d7e8f",
    "timestamp": "2025-10-11T14:30:00Z",
    "channel": "project-alpha",
    "sequence": 42
  },
  "actions": [
    {
      "type": "review",
      "label": "Review Migration Plan",
      "url": "https://wiki.example.com/migration-plan"
    },
    {
      "type": "acknowledge",
      "label": "Acknowledge Decision"
    }
  ],
  "visibility": {
    "teams": ["dev", "consulting"],
    "private": false
  }
}
```

---

## Schema Evolution Guidelines

### Adding New Fields
1. Add to appropriate section with `additionalProperties: true`
2. Make new fields optional (no `required` constraint)
3. Provide sensible defaults
4. Update schema MINOR version (e.g., 1.0.0 → 1.1.0)

### Adding New Enums
1. Add to existing enum list
2. Maintain backward compatibility (don't remove old values)
3. Update schema MINOR version

### Breaking Changes
1. Avoid when possible
2. If necessary, increment MAJOR version (e.g., 1.x.x → 2.0.0)
3. Document migration path
4. Provide transition period with dual support

### Custom Extensions
Use namespace prefixes for organization-specific fields:
```json
{
  "context": {
    "theme": "decision",
    "x-acme-department": "engineering",
    "x-acme-cost-center": "R&D-001"
  }
}
```

---

## Validation

Use the JSON Schema file (`schemas/notification-schema.json`) with any JSON Schema validator:

```javascript
// Example with AJV (JavaScript)
const Ajv = require('ajv');
const schema = require('./schemas/notification-schema.json');

const ajv = new Ajv();
const validate = ajv.compile(schema);

const valid = validate(notification);
if (!valid) {
  console.error(validate.errors);
}
```

```python
# Example with jsonschema (Python)
import jsonschema
import json

with open('schemas/notification-schema.json') as f:
    schema = json.load(f)

jsonschema.validate(notification, schema)
```

---

## Best Practices

### 1. **Always Include Schema Version**
```json
{
  "schemaVersion": "1.0.0",
  ...
}
```

### 2. **Use Appropriate Priority Levels**
- `low`: FYI, non-urgent updates
- `medium`: Standard notifications (default)
- `high`: Important, needs attention soon
- `critical`: Urgent, immediate action required

### 3. **Set Validity for Time-Sensitive Notifications**
```json
{
  "context": {
    "validity": "2025-10-18T10:00:00Z"
  }
}
```

### 4. **Use Tags for Filtering**
Enable recipients to subscribe to specific topics:
```json
{
  "context": {
    "tags": ["security", "backend", "urgent"]
  }
}
```

### 5. **Leverage Threading**
Link related notifications:
```json
{
  "metadata": {
    "replyTo": "notif-parent-id"
  }
}
```

### 6. **Choose Appropriate Format**
- `text`: Plain text, widest compatibility
- `markdown`: Rich formatting, documentation
- `json`: Structured data
- `html`: Complex formatting (use sparingly)

---

## Migration Path (Future Versions)

When schema version changes:

1. **Consumers should:**
   - Check `schemaVersion` field
   - Handle multiple versions gracefully
   - Ignore unknown fields (extensibility)
   - Use defaults for missing optional fields

2. **Producers should:**
   - Specify target schema version
   - Fill all required fields
   - Consider backward compatibility
   - Document custom extensions

---

## Changelog

### Version 1.0.0 (2025-10-11)
- Initial schema release
- Core notification structure
- Pub-Sub architecture support
- Extensibility via additionalProperties
- Team role support (dev, consulting, business)
- Multi-AI platform compatibility

---

## References

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [JSON Schema Specification](https://json-schema.org/)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
- [ISO 8601 Date Format](https://www.iso.org/iso-8601-date-and-time-format.html)
