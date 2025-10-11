#!/usr/bin/env python3
"""Team collaboration workflow example.

This example demonstrates a realistic team workflow:
1. Setting up channels for different teams (dev, consulting, business)
2. Team members subscribing with role-specific filters
3. Broadcasting architecture decisions
4. Sending critical alerts
5. Sharing status updates
6. Cross-team coordination

This simulates how different team roles would use notify-mcp for
collaboration across AI assistants (Claude, ChatGPT, Gemini).

Prerequisites:
- notify-mcp server running
- MCP client library installed: pip install mcp
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def setup_channels(session):
    """Create channels for different teams."""
    print("\n" + "=" * 60)
    print("Setting up team channels...")
    print("=" * 60)

    channels = [
        {
            "channel_id": "architecture",
            "name": "Architecture Decisions",
            "description": "Major technical architecture decisions and ADRs"
        },
        {
            "channel_id": "dev-team",
            "name": "Development Team",
            "description": "Development updates, code reviews, technical discussions"
        },
        {
            "channel_id": "consulting",
            "name": "Consulting Team",
            "description": "Client updates, project status, recommendations"
        },
        {
            "channel_id": "business",
            "name": "Business Team",
            "description": "Strategic decisions, requirements, priorities"
        },
        {
            "channel_id": "alerts",
            "name": "Critical Alerts",
            "description": "Urgent notifications requiring immediate attention"
        }
    ]

    for channel in channels:
        try:
            result = await session.call_tool("create_channel", arguments=channel)
            print(f"✓ Created: {channel['name']}")
        except Exception as e:
            print(f"  Channel '{channel['name']}' already exists")


async def simulate_dev_subscribing(session):
    """Simulate a developer subscribing to relevant channels."""
    print("\n" + "=" * 60)
    print("Developer subscribing to channels...")
    print("=" * 60)

    # Subscribe to architecture decisions (high priority only)
    await session.call_tool(
        "subscribe_to_channel",
        arguments={
            "channel": "architecture",
            "priority_filter": ["high", "critical"]
        }
    )
    print("✓ Subscribed to 'architecture' (high/critical only)")

    # Subscribe to dev team (all notifications)
    await session.call_tool(
        "subscribe_to_channel",
        arguments={"channel": "dev-team"}
    )
    print("✓ Subscribed to 'dev-team' (all notifications)")

    # Subscribe to critical alerts
    await session.call_tool(
        "subscribe_to_channel",
        arguments={
            "channel": "alerts",
            "priority_filter": ["critical"]
        }
    )
    print("✓ Subscribed to 'alerts' (critical only)")

    # Subscribe to business with tag filter
    await session.call_tool(
        "subscribe_to_channel",
        arguments={
            "channel": "business",
            "tag_filter": ["requirements", "priorities"]
        }
    )
    print("✓ Subscribed to 'business' (requirements/priorities only)")


async def broadcast_architecture_decision(session):
    """Broadcast an important architecture decision."""
    print("\n" + "=" * 60)
    print("Broadcasting Architecture Decision...")
    print("=" * 60)

    result = await session.call_tool(
        "publish_notification",
        arguments={
            "channel": "architecture",
            "title": "Migration to Microservices Architecture",
            "body": """# Architecture Decision Record: Microservices Migration

## Context
Our monolithic application is becoming difficult to scale and maintain.
Different teams need to deploy independently.

## Decision
We will migrate to a microservices architecture using Docker and Kubernetes.

## Key Services
- User Service (authentication, profiles)
- Order Service (order processing, fulfillment)
- Payment Service (payment processing, billing)
- Notification Service (emails, push notifications)

## Timeline
- Phase 1 (Q1): User Service extraction
- Phase 2 (Q2): Order Service extraction
- Phase 3 (Q3): Payment Service extraction

## Impact
- All teams must adopt Docker for local development
- CI/CD pipeline updates required
- Service communication via REST APIs initially, gRPC later

## Next Steps
1. Review service boundaries
2. Define API contracts
3. Set up development environments
""",
            "priority": "high",
            "theme": "architecture-decision",
            "tags": ["architecture", "microservices", "infrastructure"]
        }
    )
    print(result.content[0].text)


async def send_critical_alert(session):
    """Send a critical system alert."""
    print("\n" + "=" * 60)
    print("Sending Critical Alert...")
    print("=" * 60)

    result = await session.call_tool(
        "publish_notification",
        arguments={
            "channel": "alerts",
            "title": "🚨 Production Database Connection Pool Exhausted",
            "body": """# CRITICAL ALERT

## Severity: CRITICAL
**Time:** 2024-01-15 14:32 UTC

## Issue
Production database connection pool has reached maximum capacity.
New requests are being rejected.

## Impact
- API response time degraded by 300%
- 15% of requests failing with 503 errors
- User login and checkout flows affected

## Immediate Actions Required
1. Scale database connection pool (temporary fix)
2. Investigate connection leaks in Order Service
3. Review slow queries consuming connections

## Current Status
- Incident Response Team has been notified
- Monitoring dashboards: https://grafana.example.com/incidents/db-pool
- War room: #incident-response (Slack)

## Updates
Will provide updates every 15 minutes in this channel.
""",
            "priority": "critical",
            "theme": "alert",
            "tags": ["incident", "database", "production", "critical"]
        }
    )
    print(result.content[0].text)


async def share_status_update(session):
    """Share a project status update."""
    print("\n" + "=" * 60)
    print("Sharing Status Update...")
    print("=" * 60)

    result = await session.call_tool(
        "publish_notification",
        arguments={
            "channel": "dev-team",
            "title": "Sprint 23 Completed - API v2.0 Released",
            "body": """# Sprint 23 Completion Report

## What We Shipped ✅
- **API v2.0**: GraphQL support, improved rate limiting
- **User Dashboard**: New analytics widgets
- **Mobile App**: Push notification improvements
- **Infrastructure**: Database replication setup

## Metrics
- Velocity: 34 story points (target: 30)
- Bug count: 12 resolved, 3 new
- Code coverage: 78% (up from 72%)
- API response time: Improved by 25%

## Blockers Resolved
- Database performance issue fixed
- Third-party API integration completed

## Next Sprint Focus
- Payment gateway integration
- Admin panel redesign
- Performance optimization

## Kudos 🎉
Great work team! Special thanks to Sarah for resolving the database issue.
""",
            "priority": "medium",
            "theme": "state-update",
            "tags": ["sprint", "release", "status"]
        }
    )
    print(result.content[0].text)


async def business_requirement_update(session):
    """Share a business requirements change."""
    print("\n" + "=" * 60)
    print("Sharing Business Requirement Update...")
    print("=" * 60)

    result = await session.call_tool(
        "publish_notification",
        arguments={
            "channel": "business",
            "title": "Priority Shift: Mobile App Features",
            "body": """# Updated Priorities - Q1 2024

## Context
Based on customer feedback and market analysis, we're adjusting our Q1 priorities.

## New Top Priorities
1. **Mobile App Push Notifications** (moved up from P2 to P1)
   - Customer retention impact: High
   - Requested by 78% of surveyed users
   - Competitive differentiation

2. **Social Media Integration** (moved up from P3 to P2)
   - Marketing team requirement
   - Viral growth potential

3. **Advanced Reporting** (moved down from P1 to P3)
   - Deferred to Q2 based on sales pipeline

## Impact on Development
- Mobile team: Shift focus to push notifications
- Backend team: API changes needed for social integration
- Frontend team: UI updates for social sharing

## Timeline
- Push notifications: 3 weeks (critical path)
- Social integration: 4 weeks
- Requirements workshop: Next Monday 10am

## Questions?
Reach out to Product team for clarification.
""",
            "priority": "high",
            "theme": "decision",
            "tags": ["requirements", "priorities", "product"]
        }
    )
    print(result.content[0].text)


async def consulting_update(session):
    """Share a consulting project update."""
    print("\n" + "=" * 60)
    print("Sharing Consulting Project Update...")
    print("=" * 60)

    result = await session.call_tool(
        "publish_notification",
        arguments={
            "channel": "consulting",
            "title": "Client Alpha: Technical Assessment Complete",
            "body": """# Client Alpha - Assessment Summary

## Project Overview
Technical assessment for Client Alpha's modernization project.

## Key Findings
1. **Legacy System Analysis**
   - 15-year-old monolithic PHP application
   - No automated tests
   - Manual deployment process
   - Database performance issues

2. **Recommended Approach**
   - Strangler pattern for gradual migration
   - Extract user authentication service first (highest ROI)
   - Implement CI/CD pipeline
   - Modernize frontend with React

3. **Estimated Effort**
   - Phase 1 (6 months): Authentication service + CI/CD
   - Phase 2 (8 months): Core business logic extraction
   - Phase 3 (4 months): Frontend modernization

## Budget Impact
- Original estimate: $450K
- Revised estimate: $520K (scope expansion)
- Client approved budget increase

## Next Steps
- Present architecture proposal to client CTO (Friday)
- Finalize statement of work
- Team allocation planning

## Team Requirements
- 2 Senior Backend Developers
- 1 DevOps Engineer
- 1 Frontend Developer (starting Phase 3)
""",
            "priority": "medium",
            "theme": "info",
            "tags": ["consulting", "client", "assessment"]
        }
    )
    print(result.content[0].text)


async def review_notifications(session):
    """Review notifications from different channels."""
    print("\n" + "=" * 60)
    print("Reviewing Notifications Across Channels...")
    print("=" * 60)

    channels = ["architecture", "dev-team", "alerts", "business", "consulting"]

    for channel in channels:
        try:
            notifications = await session.read_resource(
                uri=f"notification://{channel}/recent"
            )

            import json
            notifs = json.loads(notifications.contents[0].text)

            print(f"\n📬 {channel.upper()} ({len(notifs)} notifications)")

            if notifs:
                for notif in notifs[:3]:  # Show first 3
                    print(f"  • {notif['information']['title']}")
                    print(f"    Priority: {notif['context']['priority']}, "
                          f"Theme: {notif['context']['theme']}")

                if len(notifs) > 3:
                    print(f"  ... and {len(notifs) - 3} more")
        except Exception as e:
            print(f"\n📭 {channel.upper()} (no notifications)")


async def main():
    """Run the team workflow example."""

    # Connect to notify-mcp server
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "notify_mcp"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize
            await session.initialize()

            print("\n" + "=" * 60)
            print("NOTIFY-MCP TEAM COLLABORATION WORKFLOW")
            print("=" * 60)
            print("\nThis example simulates a realistic team using notify-mcp")
            print("to coordinate work across different AI assistants.")

            # Run the workflow
            await setup_channels(session)
            await simulate_dev_subscribing(session)
            await broadcast_architecture_decision(session)
            await send_critical_alert(session)
            await share_status_update(session)
            await business_requirement_update(session)
            await consulting_update(session)
            await review_notifications(session)

            print("\n" + "=" * 60)
            print("Workflow completed successfully!")
            print("=" * 60)
            print("\nKey Takeaways:")
            print("• Multiple teams can coordinate through shared channels")
            print("• Filters ensure relevant notifications reach the right people")
            print("• Different notification themes (alerts, decisions, updates)")
            print("• Cross-team visibility improves collaboration")
            print("• Works seamlessly across Claude, ChatGPT, and Gemini")


if __name__ == "__main__":
    asyncio.run(main())
