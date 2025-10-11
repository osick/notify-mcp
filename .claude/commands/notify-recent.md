Retrieve recent notifications from a notify-mcp channel using MCP resources.

Ask the user which channel to check (default "engineering"), then:

1. Use the `readMcpResource` tool to read the resource:
   - URI: `notification://<channel-name>/recent`
   - Server: "notify-mcp"

2. Parse and display the notifications in a clear, readable format showing:
   - Title
   - Priority and theme
   - Timestamp
   - Body (summarized if long)
   - Tags

If there are no notifications, let the user know the channel is empty.
