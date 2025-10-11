Use the notify-mcp `publish_notification` tool to create a status update notification.

Ask the user for:
1. **Title**: Brief status update summary
2. **Details**: What changed or what's the current state
3. **Channel**: Which channel to publish to (default "general")

Then publish the notification with:
- Theme: "state-update"
- Priority: "medium"
- Tags: ["status", "update"]

Format the body as a clear, concise update that teams can quickly understand.
