Use the notify-mcp `publish_notification` tool to create a critical alert notification.

Ask the user for:
1. **Alert title**: Brief description of the alert
2. **Severity**: Critical, high, or urgent
3. **Impact**: What systems/teams are affected
4. **Action required**: What needs to be done (if any)

Then publish the notification with:
- Channel: Ask user which channel (default "general")
- Theme: "alert"
- Priority: "critical"
- Tags: ["alert", "urgent"]

Format the body clearly with sections for Impact and Action Required. Use urgent language.
