# Best Practices

Guidelines for effective notification management with Notify-MCP.

---

## Priority Levels

**Use appropriate priority levels:**

- **Critical**: Production outages, security incidents
- **High**: Important decisions, breaking changes
- **Medium**: Regular updates, milestones (default)
- **Low**: FYI information, minor updates

❌ Don't make everything critical—causes alert fatigue!

---

## Tagging Strategy

**Use consistent, descriptive tags:**

✅ Good: `["backend", "database", "migration", "postgres"]`  
❌ Bad: `["stuff", "things", "update"]`

**Tag categories:**
- Technical area: `backend`, `frontend`, `infrastructure`
- Component: `api`, `database`, `ui`, `auth`
- Type: `bugfix`, `feature`, `refactor`
- Urgency: `urgent`, `blocking`, `nice-to-have`

---

## Channel Organization

**Create focused channels:**

- `engineering` - Technical decisions and updates
- `alerts` - Production incidents
- `project-alpha` - Project-specific updates
- `architecture` - Architectural decisions
- `security` - Security-related notifications

**Avoid:**
- Too many channels (creates noise)
- Too few channels (everything mixed together)

---

## Notification Content

**Write clear, actionable titles:**

✅ "Database Migration Strategy Decided - Blue-Green Approach"  
❌ "Update"

**Include context in the body:**
- What happened or was decided
- Why it matters
- What action is needed (if any)
- Links to detailed documentation

---

## Filtering Strategy

**Subscribe with appropriate filters:**

```python
# Dev team: Technical content only
subscribe("engineering", priority=["high", "critical"], tags=["backend", "frontend"])

# Executives: High-level updates only
subscribe("project-alpha", priority=["high", "critical"])

# Security team: Security-related only
subscribe("security", tags=["security", "compliance"])
```

---

## Team Conventions

Establish team norms:

- Daily status updates: Optional
- Blockers: Immediate notification (priority: high)
- Milestones: Always announce (boosts morale)
- Questions: Use medium priority unless urgent

---

For real-world examples, see:
- [Use Cases](../use-cases/index.md)
- [Real-World Scenarios](../use-cases/real-world-scenarios.md)
- [Team Coordination](../use-cases/team-coordination.md)
