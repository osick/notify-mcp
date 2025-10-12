# MCP Tools Reference

Complete reference for all Notify-MCP tools.

---

## publish_notification

Publish a notification to a channel.

**Arguments:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `channel` | string | Yes | - | Channel name |
| `title` | string | Yes | - | Notification title |
| `body` | string | Yes | - | Notification body |
| `priority` | string | No | "medium" | Priority level |
| `theme` | string | No | "info" | Notification theme |
| `tags` | array | No | [] | List of tags |

**Priority values:** `low`, `medium`, `high`, `critical`

**Theme values:** `info`, `state-update`, `alert`, `architecture-decision`, `question`, `decision`, `memory-sync`, `discussion`

**Returns:** Notification ID and delivery statistics

---

## subscribe_to_channel

Subscribe to a channel with optional filters.

**Arguments:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel` | string | Yes | Channel name |
| `priority_filter` | array | No | Filter by priority |
| `tag_filter` | array | No | Filter by tags |

**Returns:** Subscription ID and filter details

---

## unsubscribe_from_channel

Unsubscribe from a channel.

**Arguments:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel` | string | Yes | Channel name |

**Returns:** Success status

---

## list_channels

List all available channels.

**Arguments:** None

**Returns:** Array of channels with statistics

---

## create_channel

Create a new notification channel.

**Arguments:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `channel_id` | string | Yes | Unique channel ID |
| `name` | string | Yes | Channel name |
| `description` | string | No | Channel description |

**Returns:** Channel details

---

## get_my_subscriptions

Get current subscriptions.

**Arguments:** None

**Returns:** Array of subscriptions with filters

---

For complete API documentation, see: [API Documentation](../API.md)
