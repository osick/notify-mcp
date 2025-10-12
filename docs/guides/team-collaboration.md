# Team Collaboration

Enable seamless collaboration across your team using Notify-MCP.

---

## Quick Setup

1. **Choose a shared storage location** (network drive, cloud sync folder)
2. **Configure all team members** to use the same SQLite database
3. **Create team channels** for different projects or topics
4. **Subscribe with filters** to receive relevant notifications

---

## Shared Database Configuration

All team members point to the same database file:

```json
{
  "env": {
    "NOTIFY_MCP_STORAGE_TYPE": "sqlite",
    "NOTIFY_MCP_SQLITE_PATH": "/shared/team/notify-mcp.db"
  }
}
```

---

## Best Practices

- Create channels per project or team
- Use filters to reduce notification noise
- Set appropriate priority levels
- Use tags consistently
- Document channel purposes

---

## Cross-Platform Collaboration

Team members can use different AI assistants:
- Developer A uses Claude Code
- Developer B uses ChatGPT  
- Developer C uses Gemini

All see the same notifications via the shared database!

---

For complete details, see:
- [Storage Configuration](storage-configuration.md)
- [Cross-Platform AI Use Case](../use-cases/cross-platform-ai.md)
- [Real-World Scenarios](../use-cases/real-world-scenarios.md)
