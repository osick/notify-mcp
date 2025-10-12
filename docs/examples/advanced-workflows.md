# Advanced Workflows

Complex scenarios and integration patterns.

---

## Workflow 1: Multi-Step Sprint Coordination

Track an entire sprint with notifications:

### Week 1: Planning
```
Publish to sprint-24: "Sprint 24 kickoff - User notification preferences feature"
```

### Week 2: Development
```
Publish to sprint-24: "Backend API complete - notification_preferences table ready"
Publish to sprint-24: "Frontend UI started - using mocked API"
```

### Week 3: Integration
```
Publish to sprint-24: "Integration complete - frontend connected to real API"
Publish to sprint-24: "BLOCKER: API returns 500 for null quiet_hours"
Publish to sprint-24: "Blocker resolved - null handling fixed"
```

### Week 4: Launch
```
Publish to sprint-24: "QA complete - all tests passing"
Publish to sprint-24: "LAUNCHED: Notification preferences live in production!"
```

### Retrospective
```
Show me all notifications from sprint-24
```

---

## Workflow 2: Incident Response

### Detection
```
Publish critical alert to production:
"Database connection pool exhausted - 250/250 connections in use"
```

### Response
```
Publish to production: "Investigating - checking for connection leaks"
Publish to production: "Root cause identified - retry storm hitting rate limit"
Publish to production: "Mitigation - disabling automatic retries"
```

### Resolution
```
Publish to production: "RESOLVED - Error rate back to 0%, implementing exponential backoff"
```

---

## Workflow 3: Cross-Platform Decision Making

### Research (Perplexity/Gemini)
```
Publish to architecture: "Research: Microservices migration patterns - 60% report increased complexity"
```

### Discussion (ChatGPT)
```
Publish to architecture: "Concern: Timeline impact - current monolith works, what's the ROI?"
```

### Decision (Claude)
```
Publish to architecture: "DECISION: Phased migration - modular monolith first, then extract services"
```

---

For complete examples, see: [Usage Guide](../USAGE_GUIDE.md)
