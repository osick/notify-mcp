# Notify-MCP Usage Guide

## Overview

This guide provides practical examples and best practices for using the Notify-MCP server for team collaboration across genAI platforms.

---

## Quick Start

### 1. Connect to Server

```javascript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

const client = new Client({
  name: "my-client",
  version: "1.0.0"
});

// Connect via stdio
await client.connect(transport);

// Initialize
await client.initialize();
```

### 2. Subscribe to a Channel

```javascript
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha"
  }
});
```

### 3. Handle Notifications

```javascript
client.onNotification("notifications/message", (msg) => {
  const notification = msg.params.notification;
  console.log(`[${notification.context.priority}] ${notification.information.title}`);
  console.log(notification.information.body);
});
```

---

## Common Use Cases

### Use Case 1: Broadcasting Architecture Decisions

**Scenario:** Dev team makes an architecture decision that all teams need to know about.

**Publisher (Dev Team Member):**
```javascript
await client.request({
  method: "notifications/publish",
  params: {
    channel: "project-alpha",
    notification: {
      schemaVersion: "1.0.0",
      sender: {
        id: "user-alice",
        name: "Alice Developer",
        role: "dev",
        aiTool: "claude"
      },
      context: {
        theme: "architecture-decision",
        priority: "high",
        tags: ["architecture", "database", "backend"],
        validity: "2025-10-18T00:00:00Z",
        projectId: "proj-alpha"
      },
      information: {
        title: "Migrating to Blue-Green Deployment",
        body: `# Decision: Blue-Green Database Migration

## Context
Our current database migration approach causes downtime.

## Decision
Implement Blue-Green deployment strategy for zero-downtime migrations.

## Consequences
- ✅ Zero downtime during migrations
- ✅ Easy rollback capability
- ⚠️ Requires dual database capacity temporarily
- ⚠️ More complex deployment process

## Timeline
Implementation starts next sprint.`,
        format: "markdown",
        attachments: [
          {
            type: "link",
            url: "https://wiki.company.com/blue-green-migration",
            name: "Detailed Migration Plan"
          }
        ]
      },
      actions: [
        {
          "type": "review",
          "label": "Review Full Plan",
          "url": "https://wiki.company.com/blue-green-migration"
        },
        {
          "type": "acknowledge",
          "label": "Acknowledge"
        }
      ],
      visibility: {
        teams: ["dev", "consulting", "business"]
      }
    }
  }
});
```

**Subscribers (All Teams):**
```javascript
// Dev team subscribes to all decisions
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      themes: ["architecture-decision", "state-update"],
      priority: ["medium", "high", "critical"]
    }
  }
});

// Business team subscribes to high-priority only
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      priority: ["high", "critical"],
      tags: ["architecture", "security"]
    }
  }
});
```

---

### Use Case 2: AI Conversation Memory Sync

**Scenario:** One team member's AI session discovers important context that should be shared.

**Publisher (Consulting Team):**
```javascript
await client.request({
  method: "notifications/publish",
  params: {
    channel: "project-alpha",
    notification: {
      schemaVersion: "1.0.0",
      sender: {
        id: "user-bob",
        name: "Bob Consultant",
        role: "consulting",
        aiTool: "chatgpt"
      },
      context: {
        theme: "memory-sync",
        priority: "medium",
        tags: ["requirements", "client-feedback"],
        relatedConversationId: "conv-chatgpt-789",
        projectId: "proj-alpha"
      },
      information: {
        title: "Client Clarified Performance Requirements",
        body: `During today's client call with ChatGPT assistance, we clarified performance requirements:

**Key Points:**
- System must handle 10K concurrent users (up from 5K)
- Response time must be <200ms (down from <500ms)
- 99.9% uptime SLA required

**Impact:**
This affects our current architecture choice. We may need to reconsider the caching layer.

**Next Steps:**
Dev team please review and update architecture plan accordingly.`,
        format: "markdown"
      },
      actions: [
        {
          type: "respond",
          label: "Discuss Requirements"
        }
      ],
      visibility: {
        teams: ["dev", "consulting"]
      }
    }
  }
});
```

---

### Use Case 3: Critical Alert

**Scenario:** Production issue detected, immediate team notification needed.

**Publisher (Dev Team):**
```javascript
await client.request({
  method: "notifications/publish",
  params: {
    channel: "project-alpha",
    notification: {
      schemaVersion: "1.0.0",
      sender: {
        id: "monitoring-system",
        name: "Monitoring System",
        role: "dev"
      },
      context: {
        theme: "alert",
        priority: "critical",
        tags: ["production", "outage", "database"],
        validity: "2025-10-11T16:00:00Z"
      },
      information: {
        title: "🚨 Database Connection Pool Exhausted",
        body: `**CRITICAL ALERT**

Database connection pool exhausted on production server.

**Status:** Active connections: 250/250
**Impact:** API response times degraded, some requests timing out
**Started:** 2025-10-11T14:45:00Z

**Immediate Actions Needed:**
1. Investigate connection leaks
2. Consider increasing pool size
3. Restart affected services if necessary

**Incident Channel:** #incident-2025-10-11`,
        format: "markdown"
      },
      actions: [
        {
          type: "acknowledge",
          label: "I'm On It"
        },
        {
          type: "custom",
          label: "View Metrics",
          url: "https://monitoring.company.com/incident/2025-10-11"
        }
      ],
      visibility: {
        teams: ["dev"],
        private: false
      }
    }
  }
});
```

---

### Use Case 4: Question/Discussion Thread

**Scenario:** Team member has a question that needs collaborative input.

**Initial Question:**
```javascript
const response = await client.request({
  method: "notifications/publish",
  params: {
    channel: "project-alpha",
    notification: {
      schemaVersion: "1.0.0",
      sender: {
        id: "user-carol",
        name: "Carol Business Analyst",
        role: "business",
        aiTool: "gemini"
      },
      context: {
        theme: "question",
        priority: "medium",
        tags: ["ux", "user-research"]
      },
      information: {
        title: "Should We Support Mobile Safari <14?",
        body: `Question for the team: Should we support Mobile Safari versions older than 14?

**Context from Gemini analysis:**
- 2.3% of our users on Safari <14
- Missing critical CSS features
- Would require significant polyfill overhead

**Options:**
1. Support Safari <14 (add polyfills)
2. Drop support, show upgrade message
3. Degraded experience for old browsers

What does the team think?`,
        format: "markdown"
      },
      actions: [
        {
          type: "respond",
          label: "Share Opinion"
        }
      ]
    }
  }
});

// Save notification ID for threading
const questionId = response.result.notificationId;
```

**Reply to Thread:**
```javascript
await client.request({
  method: "notifications/publish",
  params: {
    channel: "project-alpha",
    notification: {
      schemaVersion: "1.0.0",
      sender: {
        id: "user-alice",
        name: "Alice Developer",
        role: "dev"
      },
      context: {
        theme: "discussion",
        priority: "medium",
        tags: ["ux", "user-research"]
      },
      information: {
        title: "Re: Safari Support Decision",
        body: `I vote for option 2 (drop support).

**Reasoning:**
- 2.3% is very small
- Polyfills add 45KB to bundle
- Maintenance burden not worth it
- Most browsers auto-update now

Let's show a friendly upgrade message for these users.`,
        format: "markdown"
      },
      metadata: {
        replyTo: questionId  // Thread connection
      }
    }
  }
});
```

---

### Use Case 5: State Update Notification

**Scenario:** Project milestone reached, notify all stakeholders.

**Publisher (Dev Lead):**
```javascript
await client.request({
  method: "notifications/publish",
  params: {
    channel: "project-alpha",
    notification: {
      schemaVersion: "1.0.0",
      sender: {
        id: "user-dave",
        name: "Dave Team Lead",
        role: "dev"
      },
      context: {
        theme: "state-update",
        priority: "medium",
        tags: ["milestone", "sprint", "release"],
        projectId: "proj-alpha"
      },
      information: {
        title: "✅ Sprint 5 Complete - Beta Release Ready",
        body: `# Sprint 5 Completed

We've successfully completed Sprint 5 and the beta release is ready!

## Achievements
- ✅ All 23 planned stories completed
- ✅ Test coverage at 87%
- ✅ Performance benchmarks exceeded
- ✅ Security audit passed

## Beta Release
- Version: v0.5.0-beta
- Deployment: Tomorrow 10 AM
- Testing period: 2 weeks

## Next Sprint Focus
- Production hardening
- Customer feedback integration
- Documentation completion

Great work, team! 🎉`,
        format: "markdown"
      },
      actions: [
        {
          type: "acknowledge",
          label: "Acknowledge"
        },
        {
          type: "review",
          label: "View Release Notes",
          url: "https://github.com/company/project/releases/v0.5.0-beta"
        }
      ],
      visibility: {
        teams: ["dev", "consulting", "business"]
      }
    }
  }
});
```

---

## Channel Management

### Creating Project-Specific Channels

```javascript
// Create a channel for a new project
await client.request({
  method: "notifications/channels/create",
  params: {
    channel: {
      id: "project-beta",
      name: "Project Beta - Customer Portal",
      description: "Notifications for the new customer portal project",
      permissions: {
        subscribe: ["dev", "consulting", "business", "viewer"],
        publish: ["dev", "consulting", "business"],
        admin: ["dev"]
      },
      metadata: {
        projectId: "proj-beta",
        team: "customer-experience",
        tags: ["active", "customer-facing"]
      }
    }
  }
});
```

### Creating Role-Specific Channels

```javascript
// Dev-only technical discussions
await client.request({
  method: "notifications/channels/create",
  params: {
    channel: {
      id: "dev-technical",
      name: "Development - Technical",
      description: "Technical discussions and decisions for dev team",
      permissions: {
        subscribe: ["dev"],
        publish: ["dev"],
        admin: ["dev"]
      },
      metadata: {
        tags: ["technical", "dev-only"]
      }
    }
  }
});

// Business decisions channel
await client.request({
  method: "notifications/channels/create",
  params: {
    channel: {
      id: "business-decisions",
      name: "Business Decisions",
      description: "Strategic and business decisions",
      permissions: {
        subscribe: ["business", "consulting", "dev"],
        publish: ["business", "consulting"],
        admin: ["business"]
      },
      metadata: {
        tags: ["strategic", "business"]
      }
    }
  }
});
```

---

## Subscription Strategies

### Strategy 1: Team-Based Filtering

```javascript
// Dev team: Subscribe to technical content
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      themes: ["architecture-decision", "alert", "state-update"],
      tags: ["backend", "frontend", "database", "security"]
    }
  }
});

// Business team: Subscribe to high-level updates only
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      priority: ["high", "critical"],
      themes: ["decision", "state-update"]
    }
  }
});

// Consulting: Subscribe to client-related content
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      tags: ["client", "requirements", "feedback"],
      themes: ["memory-sync", "decision", "question"]
    }
  }
});
```

### Strategy 2: Priority-Based Filtering

```javascript
// Get only critical alerts
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "production",
    filters: {
      priority: ["critical"],
      themes: ["alert"]
    }
  }
});

// Get important updates
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      priority: ["high", "critical"]
    }
  }
});
```

### Strategy 3: Tag-Based Filtering

```javascript
// Security team: Security-related only
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      tags: ["security", "compliance", "audit"]
    }
  }
});

// Frontend team: Frontend-related only
await client.request({
  method: "notifications/subscribe",
  params: {
    channel: "project-alpha",
    filters: {
      tags: ["frontend", "ui", "ux"]
    }
  }
});
```

---

## Best Practices

### 1. Use Appropriate Priority Levels

```javascript
// ❌ BAD: Everything is critical
context: { priority: "critical" }  // Alert fatigue!

// ✅ GOOD: Reserve critical for emergencies
context: { priority: "critical" }  // Only for production outages

context: { priority: "high" }      // Important decisions

context: { priority: "medium" }    // Standard updates (default)

context: { priority: "low" }       // FYI information
```

### 2. Use Descriptive Titles

```javascript
// ❌ BAD: Vague titles
information: {
  title: "Update"
}

// ✅ GOOD: Clear, actionable titles
information: {
  title: "Database Migration Strategy Decided - Blue-Green Approach"
}
```

### 3. Include Context in Tags

```javascript
// ✅ GOOD: Rich tagging
context: {
  tags: ["backend", "database", "migration", "postgres", "production"]
}
```

### 4. Set Validity for Time-Sensitive Content

```javascript
// ✅ GOOD: Expires after meeting
context: {
  validity: "2025-10-18T16:00:00Z",  // Expires after scheduled meeting
  priority: "high"
}
```

### 5. Use Threading for Discussions

```javascript
// ✅ GOOD: Thread related notifications
metadata: {
  replyTo: "notif-original-question-id"
}
```

### 6. Choose Right Format

```javascript
// For rich documentation
information: {
  format: "markdown",
  body: "# Title\n\n## Section..."
}

// For structured data
information: {
  format: "json",
  body: JSON.stringify({ metric: "cpu", value: 95, unit: "%" })
}

// For simple messages
information: {
  format: "text",
  body: "Build completed successfully"
}
```

---

## Integration Patterns

### Pattern 1: CI/CD Integration

```javascript
// Post build results to team channel
async function notifyBuildResult(buildInfo) {
  await client.request({
    method: "notifications/publish",
    params: {
      channel: "ci-cd",
      notification: {
        schemaVersion: "1.0.0",
        sender: {
          id: "ci-system",
          name: "CI/CD System",
          role: "dev"
        },
        context: {
          theme: buildInfo.success ? "info" : "alert",
          priority: buildInfo.success ? "low" : "high",
          tags: ["build", buildInfo.branch]
        },
        information: {
          title: `Build ${buildInfo.success ? '✅ Passed' : '❌ Failed'}: ${buildInfo.branch}`,
          body: `Commit: ${buildInfo.commit}\nDuration: ${buildInfo.duration}s`,
          format: "text"
        },
        actions: buildInfo.success ? [] : [
          {
            type: "review",
            label: "View Logs",
            url: buildInfo.logsUrl
          }
        ]
      }
    }
  });
}
```

### Pattern 2: Monitoring Integration

```javascript
// Alert on threshold breach
async function notifyMetricAlert(metric) {
  if (metric.value > metric.threshold) {
    await client.request({
      method: "notifications/publish",
      params: {
        channel: "monitoring",
        notification: {
          schemaVersion: "1.0.0",
          sender: {
            id: "monitoring",
            name: "Monitoring System",
            role: "dev"
          },
          context: {
            theme: "alert",
            priority: metric.severity,
            tags: ["monitoring", metric.name]
          },
          information: {
            title: `⚠️ ${metric.name} threshold exceeded`,
            body: `Current: ${metric.value}${metric.unit}\nThreshold: ${metric.threshold}${metric.unit}`,
            format: "text"
          }
        }
      }
    });
  }
}
```

---

## Troubleshooting

### Issue: Not Receiving Notifications

**Check:**
1. Subscription status
```javascript
const subs = await client.request({
  method: "notifications/subscriptions/list"
});
console.log(subs);
```

2. Filter settings (might be too restrictive)
3. Channel permissions
4. Connection status

### Issue: Too Many Notifications

**Solution:** Refine filters
```javascript
// Before: Getting everything
filters: {}

// After: Only high-priority architectural decisions
filters: {
  priority: ["high", "critical"],
  themes: ["architecture-decision", "alert"],
  tags: ["backend"]  // Your area of focus
}
```

---

## Platform-Specific Usage

### Using with Claude Code

Claude Code is Anthropic's CLI tool that integrates with MCP servers. Here's how to use Notify-MCP with Claude Code.

#### 1. Configure MCP Server in Claude Code

Add to your Claude Code settings (`~/.config/claude-code/mcp_servers.json` or project `.claude/mcp_servers.json`):

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "node",
      "args": ["/path/to/notify-mcp/dist/index.js"],
      "env": {
        "NOTIFY_MCP_CONFIG": "/path/to/config.json"
      }
    }
  }
}
```

#### 2. Using MCP Tools in Claude Code

Claude Code can automatically invoke MCP tools when relevant to user requests.

**Example: Publishing a notification during development**

```
User: We just decided to use PostgreSQL instead of MongoDB.
      Can you notify the team about this architecture decision?

Claude: I'll publish this architecture decision to the team channel.
```

Claude Code will automatically:
1. Detect the need to notify the team
2. Call the `publish_notification` tool from Notify-MCP
3. Format the notification appropriately
4. Confirm delivery

**Behind the scenes:**
```javascript
// Claude Code automatically calls
tools/call {
  name: "publish_notification",
  arguments: {
    channel: "project-alpha",
    title: "Architecture Decision: PostgreSQL Selected",
    body: "After evaluation, team decided to use PostgreSQL instead of MongoDB...",
    priority: "high",
    theme: "architecture-decision",
    tags: ["database", "architecture", "backend"]
  }
}
```

#### 3. Using MCP Resources in Claude Code

Claude Code can read resources to understand context.

**Example: Checking recent notifications**

```
User: What have I missed in the project-alpha channel today?

Claude: Let me check recent notifications from project-alpha.
```

Claude Code will:
1. Read the `notification://project-alpha/recent` resource
2. Analyze recent notifications
3. Summarize for the user

**Behind the scenes:**
```javascript
// Claude Code automatically calls
resources/read {
  uri: "notification://project-alpha/recent"
}
```

#### 4. Using MCP Prompts in Claude Code

Users can explicitly invoke prompts for common workflows.

**Example: Creating a decision notification**

```
User: /prompt create_decision_notification

Claude: I'll help you create an architecture decision notification.
        Please provide the following information:
        - Decision title?
        - Context/background?
        - What was decided?
        - Consequences?
```

Then Claude uses the prompt template to guide the user through creating a well-structured notification.

#### 5. Practical Claude Code Workflows

**Workflow 1: Document and Notify**
```
User: I just fixed the memory leak in the user service.
      Document this and notify the team.

Claude:
1. [Reads the code changes]
2. [Generates documentation]
3. [Calls publish_notification tool]
   "Bug Fix: Memory Leak Resolved in User Service
    - Fixed unclosed database connections
    - Added connection pooling
    - Memory usage reduced by 40%"
```

**Workflow 2: Question the Team**
```
User: Ask the team if we should upgrade to Node 20 or stay on Node 18.

Claude:
[Calls publish_notification tool with theme: "question"]
"Node.js Version Upgrade Decision Needed

 Should we upgrade to Node 20 LTS or stay on Node 18?

 Node 20 benefits:
 - Performance improvements
 - New fetch API
 - Better TypeScript support

 Risks:
 - Potential compatibility issues
 - Dependency updates needed

 Please share your thoughts."
```

**Workflow 3: Alert on Code Issues**
```
User: Run tests and alert the team if any fail.

Claude:
[Runs tests]
[Tests fail]
[Calls publish_notification tool]
"Critical: 5 Tests Failing on Main Branch

 Failed tests:
 - auth.test.ts: Token validation
 - user.test.ts: Profile update
 ...

 Blocking merge. Please investigate."
```

---

### Using with Google Gemini

Gemini can connect to MCP servers through compatible clients. Here's how to integrate Notify-MCP with Gemini workflows.

#### 1. Configure Gemini MCP Client

Use a Gemini-compatible MCP client:

```javascript
import { GeminiMCPClient } from 'gemini-mcp-adapter';

const client = new GeminiMCPClient({
  apiKey: process.env.GEMINI_API_KEY,
  mcpServer: {
    command: 'node',
    args: ['/path/to/notify-mcp/dist/index.js']
  }
});

await client.connect();
```

#### 2. Gemini + Notify-MCP Use Cases

**Use Case 1: Data Analysis + Team Notification**

```python
# Python example with Gemini
import google.generativeai as genai
from mcp_client import MCPClient

# Configure Gemini
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Connect to Notify-MCP
mcp = MCPClient('notify-mcp')

# Analyze data
response = model.generate_content(
    "Analyze user_metrics.csv and identify trends"
)

# If significant findings, notify team
if "significant" in response.text.lower():
    mcp.call_tool('publish_notification', {
        'channel': 'data-insights',
        'title': 'Significant User Metric Trends Identified',
        'body': f"Gemini analysis results:\n\n{response.text}",
        'priority': 'high',
        'theme': 'info',
        'sender': {
            'aiTool': 'gemini'
        }
    })
```

**Use Case 2: Multimodal Analysis + Notification**

```python
# Gemini analyzes screenshot, notifies about UI issues
import PIL.Image

# Load screenshot
img = PIL.Image.open('app_screenshot.png')

# Gemini analyzes UI
response = model.generate_content([
    "Analyze this UI screenshot for accessibility issues",
    img
])

# Notify design team
if accessibility_issues_found(response.text):
    mcp.call_tool('publish_notification', {
        'channel': 'design-feedback',
        'title': 'Accessibility Issues Detected in UI',
        'body': response.text,
        'priority': 'medium',
        'theme': 'question',
        'tags': ['accessibility', 'ui', 'design'],
        'attachments': [{
            'type': 'image',
            'url': 'app_screenshot.png',
            'name': 'UI Screenshot with Issues'
        }],
        'sender': {
            'aiTool': 'gemini'
        }
    })
```

**Use Case 3: Code Review + Notification**

```javascript
// Gemini reviews code, notifies about issues
const { GoogleGenerativeAI } = require("@google/generative-ai");
const { MCPClient } = require("mcp-client");

const genai = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genai.getGenerativeModel({ model: "gemini-pro" });
const mcp = new MCPClient("notify-mcp");

// Get code diff
const diff = await git.diff('main...feature-branch');

// Gemini reviews
const result = await model.generateContent(
  `Review this code for security issues, performance problems, and best practices:\n\n${diff}`
);

// Parse severity
const severity = extractSeverity(result.response.text());

if (severity !== 'none') {
  await mcp.callTool('publish_notification', {
    channel: 'code-review',
    title: `Code Review: ${severity.toUpperCase()} Issues Found`,
    body: result.response.text(),
    priority: severity === 'critical' ? 'critical' : 'high',
    theme: 'alert',
    tags: ['code-review', 'security', 'performance'],
    sender: {
      name: 'Gemini Code Reviewer',
      role: 'dev',
      aiTool: 'gemini'
    },
    actions: [{
      type: 'review',
      label: 'View Code Diff',
      url: 'https://github.com/company/repo/compare/main...feature'
    }]
  });
}
```

**Use Case 4: Customer Feedback Analysis**

```python
# Gemini analyzes customer feedback, notifies business team
feedback_data = load_customer_feedback()

prompt = f"""
Analyze the following customer feedback and identify:
1. Common pain points
2. Feature requests
3. Urgent issues
4. Sentiment trends

Feedback: {feedback_data}
"""

response = model.generate_content(prompt)
analysis = response.text

# Extract actionable insights
insights = extract_insights(analysis)

# Notify business and consulting teams
mcp.call_tool('publish_notification', {
    'channel': 'customer-insights',
    'title': 'Weekly Customer Feedback Analysis',
    'body': f"""# Customer Feedback Insights

{analysis}

## Recommended Actions
{format_actions(insights)}
""",
    'format': 'markdown',
    'priority': 'medium',
    'theme': 'info',
    'tags': ['customer-feedback', 'insights', 'weekly-report'],
    'visibility': {
        'teams': ['business', 'consulting', 'dev']
    },
    'sender': {
        'name': 'Gemini Analyst',
        'role': 'business',
        'aiTool': 'gemini'
    }
})
```

---

### Using with ChatGPT

ChatGPT can connect to MCP servers through custom GPT actions or API integrations.

#### 1. Configure ChatGPT Custom GPT Action

In Custom GPT settings, add Notify-MCP as an action:

```yaml
openapi: 3.0.0
info:
  title: Notify-MCP API
  version: 1.0.0
servers:
  - url: http://localhost:3000/mcp
paths:
  /publish:
    post:
      operationId: publishNotification
      summary: Publish notification to team
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                channel: { type: string }
                title: { type: string }
                body: { type: string }
                priority: { type: string }
```

#### 2. Using from ChatGPT Conversations

```
User: We decided to switch from REST to GraphQL. Notify the team.

ChatGPT: I'll notify the team about the API architecture change.

[Calls publishNotification action]

✓ Notification sent to #project-alpha channel
  "Architecture Decision: Migrating to GraphQL"
  Delivered to 12 team members
```

---

### Cross-Platform Collaboration Examples

**Scenario 1: Claude Code → Gemini → Team**

1. Developer using Claude Code makes code changes
2. Claude Code publishes notification about changes
3. Business analyst using Gemini sees notification
4. Gemini helps analyze impact and notifies business team

**Scenario 2: Gemini Analysis → ChatGPT Review → Claude Code Implementation**

1. Gemini analyzes customer data, publishes insights
2. Product manager using ChatGPT sees notification
3. ChatGPT helps draft requirements, publishes to dev channel
4. Developer using Claude Code sees notification and implements

**Scenario 3: Multi-AI Decision Making**

```
# Team discussion across AI platforms

[Claude Code - Dev Team]
"Proposing microservices architecture for user service.
 Pros: Scalability, independent deployment
 Cons: Complexity, distributed debugging
 Thoughts?"

[ChatGPT - Business Team]
"From business perspective: Concerned about timeline impact.
 Current monolith works. What's the ROI?"

[Gemini - Consulting Team]
"Analyzed similar migrations. Average 3-month timeline,
 20% ops cost increase first year, 40% scalability gain.
 Recommend phased approach."

[Claude Code - Dev Team]
"Decision: Phased migration starting Q2.
 Phase 1: Extract user authentication service
 Phase 2: Extract notification service
 Phase 3: Evaluate and continue"
```

---

## References

- [API Documentation](./API.md)
- [Notification Schema](./NOTIFICATION_SCHEMA.md)
- [Architecture Overview](./ARCHITECTURE.md)
- [MCP Primitives (Tools, Resources, Prompts)](./MCP_PRIMITIVES.md)
