# API Reference

Complete reference for Notify-MCP tools, resources, and configuration.

---

## Tools

Notify-MCP provides 6 MCP tools for managing notifications:

| Tool | Purpose |
|------|---------|
| **publish_notification** | Publish a notification to a channel |
| **subscribe_to_channel** | Subscribe to a channel with filters |
| **unsubscribe_from_channel** | Unsubscribe from a channel |
| **list_channels** | List all available channels |
| **create_channel** | Create a new notification channel |
| **get_my_subscriptions** | Get your current subscriptions |

[:octicons-arrow-right-24: Tools Documentation](tools.md)

---

## Resources

3 MCP resources for accessing notification data:

| Resource | Purpose |
|----------|---------|
| `notification://<channel>/recent` | Get last 50 notifications from a channel |
| `channel://<channel>/info` | Get channel information and statistics |
| `schema://notification` | Get the notification JSON schema |

[:octicons-arrow-right-24: Resources Documentation](resources.md)

---

## Prompts

2 prompt templates for common workflows:

- **Architecture Decision** - Structured template for ADRs
- **Critical Alert** - Template for urgent notifications

[:octicons-arrow-right-24: Prompts Documentation](prompts.md)

---

## Configuration

Environment variables and settings:

[:octicons-arrow-right-24: Configuration Options](configuration.md)

---

## Complete API Documentation

For detailed JSON-RPC API documentation, see:

**[Complete API Reference](../API.md)**

Includes:
- All API methods with request/response examples
- Error codes and handling
- Rate limits
- Transport-specific details
- Usage examples
