Use the notify-mcp `publish_notification` tool to create an architecture decision notification.

Ask the user for:
1. **Decision title**: Brief description of what was decided
2. **Context**: Background information and why this decision was needed
3. **Decision**: The actual decision and rationale

Then publish the notification with:
- Channel: "engineering" (or ask user which channel)
- Theme: "architecture-decision"
- Priority: "high"
- Tags: ["architecture", "decision"]

Format the body as a clear, professional notification in markdown with sections for Context and Decision.
