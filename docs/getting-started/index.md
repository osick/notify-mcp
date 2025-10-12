# Getting Started with Notify-MCP

Welcome to Notify-MCP! This guide will help you get up and running with cross-platform AI collaboration in minutes.

---

## What is Notify-MCP?

Notify-MCP is a **pub-sub MCP server** that enables teams to share notifications, decisions, and status updates across different AI assistants (Claude, ChatGPT, Gemini). It breaks down the information silos that form when team members use different AI platforms.

### Key Benefits

- 🌐 **Cross-Platform**: Works with Claude, ChatGPT, Gemini, and any MCP-compatible AI assistant
- 💾 **Persistent**: SQLite-based storage enables team collaboration through shared databases
- 🔔 **Smart Filtering**: Subscribe to channels with filters for priority, tags, themes, and sender roles
- 🚀 **Zero Setup**: In-memory mode for testing, SQLite for team sharing—no server required

---

## Quick Start Path

Follow this 3-step path to get started:

### 1. **[Install Notify-MCP](installation.md)** (5 minutes)

Install Python, uv package manager, and Notify-MCP:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone <repository-url>
cd notify-mcp
uv sync
```

[:octicons-arrow-right-24: Installation Guide](installation.md)

---

### 2. **[Configure Your AI Assistant](configuration.md)** (5 minutes)

Add Notify-MCP to your Claude Desktop, ChatGPT, or Gemini configuration:

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "notify_mcp"],
      "cwd": "/path/to/notify-mcp"
    }
  }
}
```

[:octicons-arrow-right-24: Configuration Guide](configuration.md)

---

### 3. **[Start Collaborating](quick-start.md)** (10 minutes)

Create your first channel, publish a notification, and retrieve it:

```python
# Create a channel
"Create a channel called 'engineering' for technical updates"

# Publish a notification
"Publish to engineering: API v2.0 has been released to production"

# Retrieve notifications
"Show me recent notifications from the engineering channel"
```

[:octicons-arrow-right-24: Quick Start Guide](quick-start.md)

---

## What You'll Learn

### [Installation Guide](installation.md)

- Installing Python 3.11+ and uv
- Cloning and setting up Notify-MCP
- Verifying the installation
- Platform-specific instructions (macOS, Linux, Windows)

### [Configuration Guide](configuration.md)

- Configuring Claude Desktop / Claude Code
- Setting up storage (in-memory vs. SQLite)
- Configuring for team collaboration
- Environment variables reference

### [Quick Start Tutorial](quick-start.md)

- Creating your first channel
- Publishing notifications
- Subscribing with filters
- Retrieving notification history
- Common usage patterns

---

## Next Steps

After completing the Getting Started guides:

- **[Explore Use Cases](../use-cases/index.md)** - See real-world scenarios demonstrating Notify-MCP's value
- **[Review API Reference](../api-reference/index.md)** - Learn about all available tools and resources
- **[Follow Best Practices](../guides/best-practices.md)** - Optimize your team's notification workflow
- **[Browse Examples](../examples/basic-usage.md)** - Study code examples and integration patterns

---

## Need Help?

- **Installation Issues?** Check the [Installation Guide](installation.md#troubleshooting)
- **Configuration Problems?** See [Configuration Guide](configuration.md#troubleshooting)
- **General Questions?** Visit the [Troubleshooting Guide](../guides/troubleshooting.md)
- **Bug Reports?** Create an issue on [GitHub](https://github.com/osick/notify-mcp/issues)

---

**Ready to get started? [Begin with Installation →](installation.md)**
