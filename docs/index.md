# Welcome to Notify-MCP

<div class="hero" markdown>
<div class="hero-content" markdown>

## Seamless Team Collaboration Across AI Platforms

**Notify-MCP** is a powerful pub-sub MCP server that enables teams to share notifications, decisions, and status updates across different AI assistants (Claude, ChatGPT, Gemini).

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[View Use Cases](use-cases/index.md){ .md-button }

</div>
</div>

---

## Why Notify-MCP?

<div class="grid cards" markdown>

-   :fontawesome-solid-share-nodes:{ .lg .middle } __Cross-Platform Collaboration__

    ---

    Share information seamlessly between Claude, ChatGPT, Gemini, and other AI assistants. Your team stays synchronized regardless of which platform they use.

    [:octicons-arrow-right-24: Learn more](use-cases/cross-platform-ai.md)

-   :fontawesome-solid-database:{ .lg .middle } __Persistent Storage__

    ---

    SQLite-based persistent storage enables true team collaboration. Share a database file and everyone sees the same channels and notifications.

    [:octicons-arrow-right-24: Storage Guide](guides/storage-configuration.md)

-   :fontawesome-solid-filter:{ .lg .middle } __Smart Filtering__

    ---

    Subscribe to channels with intelligent filters based on priority, tags, themes, and sender roles. Only receive what matters to you.

    [:octicons-arrow-right-24: Configuration](getting-started/configuration.md)

-   :fontawesome-solid-bolt:{ .lg .middle } __Production Ready__

    ---

    62 passing tests, 70% code coverage, comprehensive documentation. Built with SQLAlchemy, aiosqlite, and modern async Python.

    [:octicons-arrow-right-24: Architecture](architecture/overview.md)

</div>

---

## Quick Example

### 1. Developer publishes architecture decision in Claude

```python
# In Claude Code or Claude Desktop
"Create a channel called 'architecture' and publish a decision about
migrating to microservices architecture"
```

### 2. Team members receive notification

All team members subscribed to the `architecture` channel—whether using Claude, ChatGPT, or Gemini—see the decision:

```json
{
  "title": "Migration to Microservices",
  "body": "Decision: Moving from monolith to microservices using Docker/K8s",
  "priority": "high",
  "theme": "architecture-decision",
  "sender": "Alice (Developer)",
  "timestamp": "2025-01-12T10:30:00Z"
}
```

### 3. Everyone stays aligned

No more information silos! Architecture decisions, incidents, and project updates flow seamlessly across your entire team.

---

## Key Features

### 🎯 Multi-Channel System
Create dedicated channels for teams, projects, or topics. Organize notifications logically.

### 🔔 Pub-Sub Architecture
Decoupled notification delivery. Publishers and subscribers don't need to know about each other.

### 💾 Persistent Storage
Version 1.1.0+ includes SQLite storage for team collaboration. Notifications survive server restarts.

### 📊 Rich Notification Model
- **Sender info**: User ID, name, role, AI tool
- **Context**: Theme, priority, tags, validity
- **Information**: Title, body (text/markdown/json)
- **Actions**: Optional action buttons
- **Metadata**: ID, timestamp, sequence, threading

### 🔐 Type-Safe
Full Pydantic validation with JSON Schema. Catch errors early.

### 🧪 Well-Tested
62 unit tests, 70% code coverage, comprehensive test suite.

---

## Use Cases

<div class="grid cards" markdown>

-   **Architecture Decisions**

    Document and broadcast architectural decisions to all stakeholders. Maintain a searchable history of technical choices.

    [:octicons-arrow-right-24: View scenario](use-cases/architecture-decisions.md)

-   **DevOps Incidents**

    Alert teams about production incidents. Critical notifications reach everyone instantly, regardless of their AI platform.

    [:octicons-arrow-right-24: View scenario](use-cases/incident-response.md)

-   **Team Coordination**

    Coordinate work across distributed teams. Share status updates, milestones, and blockers in real-time.

    [:octicons-arrow-right-24: View scenario](use-cases/team-coordination.md)

-   **Project Updates**

    Broadcast project milestones, sprint updates, and requirement changes. Keep stakeholders informed automatically.

    [:octicons-arrow-right-24: View scenario](use-cases/project-updates.md)

</div>

---

## Getting Started

Ready to enable seamless collaboration across your team's AI assistants?

1. **[Install Notify-MCP](getting-started/installation.md)** - Set up in 5 minutes
2. **[Configure Storage](getting-started/configuration.md)** - Enable team collaboration
3. **[Create Channels](getting-started/quick-start.md)** - Organize your notifications
4. **[Explore Use Cases](use-cases/index.md)** - Learn real-world applications

---

## Community & Support

<div class="grid" markdown>

**:fontawesome-brands-github: GitHub**

Find the source code, report issues, and contribute on [GitHub](https://github.com/osick/notify-mcp).

**:fontawesome-solid-book: Documentation**

Comprehensive guides, API reference, and examples available throughout this site.

**:fontawesome-solid-comments: Discussions**

Join the conversation in [GitHub Discussions](https://github.com/osick/notify-mcp/discussions).

**:fontawesome-solid-bug: Bug Reports**

Found a bug? [Create an issue](https://github.com/osick/notify-mcp/issues) on GitHub.

</div>

---

## What's New

### Version 1.1.0 - Persistent Storage 🎉

The latest release introduces SQLite-based persistent storage, enabling true team collaboration:

- ✅ **Persistent across restarts** - Notifications survive server restarts
- ✅ **Team collaboration** - Share database files for cross-team sync
- ✅ **Zero setup** - File-based SQLite requires no server
- ✅ **Production ready** - 62 tests, 70% coverage

[View Release Notes](about/changelog.md){ .md-button }

---

<div class="center-text" markdown>

**Built with ❤️ for seamless AI collaboration**

Made with [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) by Anthropic

</div>
