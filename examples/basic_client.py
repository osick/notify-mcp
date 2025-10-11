#!/usr/bin/env python3
"""Basic notify-mcp client example.

This example demonstrates:
1. Creating a channel
2. Subscribing to a channel
3. Publishing a notification
4. Retrieving recent notifications

Prerequisites:
- notify-mcp server running
- MCP client library installed: pip install mcp
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Run the basic client example."""

    # Connect to notify-mcp server via stdio
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "notify_mcp"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize the connection
            await session.initialize()

            print("=" * 60)
            print("Notify-MCP Basic Client Example")
            print("=" * 60)

            # 1. Create a new channel
            print("\n1. Creating a new channel...")
            try:
                result = await session.call_tool(
                    "create_channel",
                    arguments={
                        "channel_id": "dev-updates",
                        "name": "Development Updates",
                        "description": "Technical updates and status changes"
                    }
                )
                print(f"✓ {result.content[0].text}")
            except Exception as e:
                print(f"✗ Channel creation failed (may already exist): {e}")

            # 2. List all channels
            print("\n2. Listing all channels...")
            result = await session.call_tool("list_channels", arguments={})
            print(result.content[0].text)

            # 3. Subscribe to the channel
            print("\n3. Subscribing to dev-updates channel...")
            result = await session.call_tool(
                "subscribe_to_channel",
                arguments={
                    "channel": "dev-updates",
                    "priority_filter": ["high", "critical"]  # Only high-priority
                }
            )
            print(f"✓ {result.content[0].text}")

            # 4. Publish a notification
            print("\n4. Publishing a notification...")
            result = await session.call_tool(
                "publish_notification",
                arguments={
                    "channel": "dev-updates",
                    "title": "API Version 2.0 Released",
                    "body": "The new API v2.0 is now live in production. "
                            "Key changes: GraphQL support, rate limiting improvements, "
                            "and better error messages.",
                    "priority": "high",
                    "theme": "state-update",
                    "tags": ["api", "release", "backend"]
                }
            )
            print(result.content[0].text)

            # 5. Publish a lower priority notification (will be filtered)
            print("\n5. Publishing a low-priority notification (will be filtered)...")
            result = await session.call_tool(
                "publish_notification",
                arguments={
                    "channel": "dev-updates",
                    "title": "Code Review Guidelines Updated",
                    "body": "Minor updates to our code review checklist.",
                    "priority": "low",  # This will be filtered out
                    "theme": "info",
                    "tags": ["process"]
                }
            )
            print(result.content[0].text)

            # 6. Retrieve recent notifications
            print("\n6. Retrieving recent notifications...")
            notifications = await session.read_resource(
                uri="notification://dev-updates/recent"
            )

            import json
            notifs = json.loads(notifications.contents[0].text)

            print(f"\nFound {len(notifs)} notification(s):")
            for notif in notifs:
                print(f"\n  📬 {notif['information']['title']}")
                print(f"     Priority: {notif['context']['priority']}")
                print(f"     Theme: {notif['context']['theme']}")
                print(f"     Tags: {', '.join(notif['context']['tags'])}")
                print(f"     ID: {notif['metadata']['id']}")

            # 7. Get my subscriptions
            print("\n7. Checking my subscriptions...")
            result = await session.call_tool("get_my_subscriptions", arguments={})
            print(result.content[0].text)

            # 8. Unsubscribe from the channel
            print("\n8. Unsubscribing from dev-updates...")
            result = await session.call_tool(
                "unsubscribe_from_channel",
                arguments={"channel": "dev-updates"}
            )
            print(f"✓ {result.content[0].text}")

            print("\n" + "=" * 60)
            print("Example completed successfully!")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
