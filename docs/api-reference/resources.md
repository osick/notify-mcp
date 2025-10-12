# MCP Resources Reference

Notify-MCP provides 3 MCP resources for accessing notification data.

---

## notification://<channel>/recent

Retrieve last 50 notifications from a channel.

**URI Format:** `notification://<channel_name>/recent`

**Example:** `notification://engineering/recent`

**Returns:** JSON array of notifications (up to 50 most recent)

**Filtering:** Applied based on your subscription filters

---

## channel://<channel>/info

Get channel information and statistics.

**URI Format:** `channel://<channel_name>/info`

**Example:** `channel://engineering/info`

**Returns:** Channel details including:
- Channel name and description
- Subscriber count
- Total notification count
- Last notification timestamp
- Creation date

---

## schema://notification

Get the complete notification JSON schema.

**URI Format:** `schema://notification`

**Returns:** JSON Schema specification for notifications

**Use case:** Understand notification structure, validate custom notifications

---

For complete API documentation, see: [API Documentation](../API.md)
