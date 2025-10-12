# Quick Start Tutorial

Get hands-on with Notify-MCP in 10 minutes! This tutorial walks you through creating channels, publishing notifications, and retrieving them across AI platforms.

---

## Prerequisites

Before starting:

- ✅ [Notify-MCP installed](installation.md)
- ✅ [Claude Desktop configured](configuration.md)
- ✅ Claude Desktop restarted

---

## Step 1: Create Your First Channel

Channels organize notifications by topic, team, or project. Let's create an engineering channel:

**In Claude:**

```
Create a channel called 'engineering' for technical updates and decisions
```

**Claude will use the `create_channel` tool:**

```json
{
  "channel_id": "engineering",
  "name": "Engineering Team",
  "description": "Technical updates and decisions"
}
```

**Result:** Channel created! ✅

---

## Step 2: Subscribe to the Channel

Subscribe to receive notifications from the channel. You can add filters for priority, tags, or themes:

**In Claude:**

```
Subscribe me to the engineering channel with high and critical priority only
```

**Claude will use the `subscribe_to_channel` tool:**

```json
{
  "channel": "engineering",
  "priority_filter": ["high", "critical"]
}
```

**Result:** Subscribed with filters! 🔔

---

## Step 3: Publish a Notification

Let's publish an architecture decision to the engineering channel:

**In Claude:**

```
Publish to engineering channel: We've decided to migrate to PostgreSQL for better
performance. This is a high-priority architecture decision tagged with database and backend.
```

**Claude will use the `publish_notification` tool:**

```json
{
  "channel": "engineering",
  "title": "Architecture Decision: Migrate to PostgreSQL",
  "body": "We've decided to migrate to PostgreSQL for better performance and scalability.",
  "priority": "high",
  "theme": "architecture-decision",
  "tags": ["database", "backend", "migration"]
}
```

**Result:** Notification published! 📢

---

## Step 4: Retrieve Notifications

Now let's retrieve notifications from the channel:

**In Claude:**

```
Show me recent notifications from the engineering channel
```

**Claude will read the `notification://engineering/recent` resource:**

**Result:** You'll see your published notification! 📬

---

## Step 5: Test Cross-Platform (Optional)

If you have ChatGPT or Gemini configured with Notify-MCP:

**In ChatGPT or Gemini:**

```
Show me recent notifications from the engineering channel
```

**Result:** You'll see the same notification published from Claude! 🌐

This demonstrates cross-platform collaboration!

---

## Common Usage Patterns

### Pattern 1: Architecture Decisions

```
Publish an architecture decision to engineering:
Title: "Migration to Microservices"
Context: Current monolith is hard to scale
Decision: Moving to microservices with Docker and Kubernetes
Priority: High
Tags: architecture, microservices, infrastructure
```

### Pattern 2: Critical Alerts

```
Publish a critical alert to production channel:
Title: "Database Connection Pool Exhausted"
Status: 250/250 connections in use
Impact: API response times degraded
Priority: Critical
```

### Pattern 3: Status Updates

```
Publish to project-alpha channel:
Title: "Sprint 5 Complete - Beta Release Ready"
Achievements: All 23 stories completed, 87% test coverage
Next Steps: Deploy beta tomorrow at 10 AM
Priority: Medium
```

---

## Using Slash Commands (Claude Code)

For faster workflows, use slash commands:

### Create Architecture Decision

```
/notify-decision
```

Claude will prompt you for:
- Decision title
- Context/background
- What was decided
- Consequences

### Create Critical Alert

```
/notify-alert
```

Claude will prompt you for alert details.

### View Recent Notifications

```
/notify-recent
```

Select which channel to view.

---

## Advanced: Filtering

Subscribe with specific filters to receive only relevant notifications:

### Priority Filtering

```
Subscribe to production channel with critical priority only
```

Only critical alerts will reach you.

### Tag Filtering

```
Subscribe to engineering channel with tags: security, database
```

Only notifications tagged with security or database will be visible.

### Combined Filtering

```
Subscribe to project-alpha with high priority and tags: frontend, ui
```

Only high-priority frontend/UI notifications will match.

---

## What's Next?

Now that you've mastered the basics:

- **[Explore Real-World Use Cases →](../use-cases/index.md)**
- **[Review API Reference →](../api-reference/index.md)**
- **[Learn Best Practices →](../guides/best-practices.md)**
- **[Browse Code Examples →](../examples/basic-usage.md)**

---

## Need Help?

- **Questions?** Check the [Troubleshooting Guide](../guides/troubleshooting.md)
- **API Reference?** See [Tools Documentation](../api-reference/tools.md)
- **Team Setup?** Review [Team Collaboration Guide](../guides/team-collaboration.md)
- **Issues?** Report on [GitHub](https://github.com/osick/notify-mcp/issues)

---

**Congratulations!** You've completed the Quick Start tutorial. 🎉

**Ready to see real-world scenarios? [Explore Use Cases →](../use-cases/index.md)**
