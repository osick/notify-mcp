# MCP Prompts Reference

Notify-MCP provides 2 prompt templates for common workflows.

---

## Architecture Decision Prompt

Template for structured architecture decision records (ADRs).

**Usage:** Use this prompt when making architectural decisions.

**Prompts for:**
- Decision title
- Context/background
- What was decided
- Consequences (pros/cons)
- Alternatives considered

**Output:** Well-structured ADR notification

---

## Critical Alert Prompt

Template for urgent production alerts.

**Usage:** Use this prompt for critical incidents.

**Prompts for:**
- Alert title
- Severity level
- Impact description
- Affected systems
- Required actions

**Output:** High-priority alert notification

---

## Using Prompts

### In Claude Code

Prompts are automatically available as slash commands:

```
/notify-decision
/notify-alert
```

### In Other AI Assistants

Request the prompt explicitly:

```
Use the architecture decision prompt to create a notification
```

---

For complete API documentation, see: [API Documentation](../API.md)
