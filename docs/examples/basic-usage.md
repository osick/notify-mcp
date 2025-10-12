# Basic Usage Examples

Practical examples for common Notify-MCP workflows.

---

## Example 1: Create Channel and Publish

**Create a project channel:**

```
Create a channel called 'project-alpha' for Project Alpha team updates
```

**Publish a notification:**

```
Publish to project-alpha:
Title: "Sprint 5 Complete"
Body: "All 23 stories completed, 87% test coverage, beta ready for deployment"
Priority: Medium
Tags: sprint, milestone
```

**Retrieve notifications:**

```
Show me recent notifications from project-alpha
```

---

## Example 2: Architecture Decision

**Using slash command (Claude Code):**

```
/notify-decision
```

**Or directly:**

```
Publish architecture decision to engineering channel:
Decision: Migrating to microservices architecture
Context: Monolith becoming hard to scale and deploy
Rationale: Need independent deployment and scaling
Impact: 6-month migration timeline
Priority: High
Tags: architecture, microservices
```

---

## Example 3: Critical Alert

**Publish production alert:**

```
Publish critical alert to production channel:
Title: "Database Connection Pool Exhausted"
Issue: 250/250 connections in use
Impact: API response times degraded
Action: Investigate connection leaks immediately
Priority: Critical
Tags: production, database, incident
```

---

## Example 4: Filtered Subscriptions

**Subscribe with filters:**

```
Subscribe to engineering channel with:
- Priority: high and critical only
- Tags: backend, database, security
```

**Result:** Only notifications matching ALL criteria are visible.

---

## Example 5: Cross-Team Notification

**Product Manager (using ChatGPT):**

```
Publish to all-hands channel:
Title: "Q1 OKRs Finalized"
Body: "Q1 objectives published to wiki. Please review your team's goals by EOW."
Priority: High
Tags: okr, planning, quarterly
```

**Developer (using Claude):**

```
Show me recent notifications from all-hands
```

**Result:** Sees the OKR notification despite different AI platforms!

---

## Example 6: Sprint Workflow

**Week 1:**
```
Publish to sprint-24: "Sprint kickoff - Payment feature"
```

**Week 2:**
```
Publish to sprint-24: "Milestone: Backend API complete"
```

**Week 3:**
```
Publish to sprint-24: "Blocker: Stripe API rate limit issue"
Publish to sprint-24: "Blocker resolved: Implemented exponential backoff"
```

**Week 4:**
```
Publish to sprint-24: "Sprint complete - Payment feature shipped!"
```

**Retrospective:**
```
Show me all notifications from sprint-24
```

**Result:** Complete sprint timeline for retrospective!

---

## Example 7: Question and Discussion

**Ask the team:**

```
Publish question to architecture channel:
Title: "Should we upgrade to Node 20 or stay on Node 18?"
Context: Node 20 offers performance improvements but may have compatibility issues
Options:
1. Upgrade now (risks: compatibility)
2. Wait for LTS (risks: miss performance gains)
3. Gradual rollout (risks: complexity)
Priority: Medium
Tags: infrastructure, nodejs, decision-needed
```

**Team members respond:**

```
Publish to architecture:
Title: "Re: Node 20 Upgrade"
Body: "Recommend option 3 (gradual rollout). Migrate dev first, then staging, then prod."
Priority: Medium
Tags: infrastructure, nodejs
```

---

## Complete Usage Documentation

For comprehensive usage examples including platform-specific guides, see:

**[Complete Usage Guide](../USAGE_GUIDE.md)**

Includes:
- Claude Code workflows
- ChatGPT integration patterns
- Gemini usage examples
- Advanced filtering strategies
- Integration patterns (CI/CD, monitoring)

---

## Next Steps

- [Advanced Workflows](advanced-workflows.md)
- [Integration Examples](integration.md)
- [Real-World Scenarios](../use-cases/real-world-scenarios.md)
