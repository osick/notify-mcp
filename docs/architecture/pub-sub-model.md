# Pub-Sub Model

Notify-MCP implements a publish-subscribe messaging pattern.

---

## Core Concepts

### Publishers

- Publish notifications to channels
- Don't know who subscribes
- Fire-and-forget model

### Subscribers

- Subscribe to channels
- Receive matching notifications
- Apply filters (priority, tags, themes)

### Channels

- Named topics for organizing notifications
- Support multiple publishers
- Support multiple subscribers

---

## Communication Patterns

### Broadcast

Publisher → Channel → All Subscribers

### Filtered

Publisher → Channel → Matching Subscribers (based on filters)

### Threaded

Notifications can reference parents (`replyTo`)

---

## Benefits

- **Decoupling:** Publishers and subscribers independent
- **Scalability:** Add subscribers without changing publishers
- **Flexibility:** Subscribers control what they receive

---

For complete architecture documentation, see: [Architecture Overview](../ARCHITECTURE.md)
