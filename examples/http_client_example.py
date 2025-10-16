#!/usr/bin/env python
"""Example: Connect to notify-mcp HTTP server and interact with it.

This example demonstrates how to connect to a notify-mcp server running
with HTTP transport and perform basic operations.

Prerequisites:
    1. Start HTTP server:
       NOTIFY_MCP_TRANSPORT_TYPE=http uv run python -m notify_mcp

    2. Run this client:
       python examples/http_client_example.py

Note: This is a simplified example. For production use, implement proper
error handling, retries, and connection management.
"""

import asyncio
import json
from datetime import datetime

from mcp import ClientSession
from mcp.client.streamable_http import StreamableHTTPTransport


async def main():
    """Connect to HTTP server and demonstrate basic operations."""
    # Server configuration
    server_url = "http://localhost:8000/mcp"

    print(f"Connecting to notify-mcp HTTP server at {server_url}...")
    print()

    # Create HTTP transport
    transport = StreamableHTTPTransport(server_url)

    async with ClientSession(transport.read, transport.write) as session:
        # Initialize connection
        await session.initialize()
        print("✅ Connected to notify-mcp server!")
        print()

        # List available tools
        tools_result = await session.list_tools()
        print(f"📋 Available Tools ({len(tools_result.tools)}):")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")
        print()

        # Create a channel
        print("Creating 'demo' channel...")
        create_result = await session.call_tool(
            "create_channel",
            arguments={
                "channel_id": "demo",
                "name": "Demo Channel",
                "description": "Example channel for HTTP client demo",
            },
        )
        print(f"✅ {create_result.content[0].text}")
        print()

        # Subscribe to the channel
        print("Subscribing to 'demo' channel...")
        subscribe_result = await session.call_tool(
            "subscribe_to_channel",
            arguments={
                "channel": "demo",
                "priority_filter": ["high", "critical"],
            },
        )
        print(f"✅ {subscribe_result.content[0].text}")
        print()

        # Publish a notification
        print("Publishing notification to 'demo' channel...")
        publish_result = await session.call_tool(
            "publish_notification",
            arguments={
                "channel": "demo",
                "title": "HTTP Client Test",
                "body": f"Successfully connected via HTTP at {datetime.now().isoformat()}",
                "priority": "high",
                "theme": "info",
                "tags": ["http", "example", "test"],
            },
        )
        print(f"✅ {publish_result.content[0].text}")
        print()

        # List all channels
        print("Listing all channels...")
        channels_result = await session.call_tool("list_channels", arguments={})
        print(channels_result.content[0].text)
        print()

        # Read notifications from the channel
        print("Reading recent notifications from 'demo' channel...")
        notifications_uri = "notification://demo/recent"
        notifications_content = await session.read_resource(notifications_uri)
        notifications = json.loads(notifications_content)
        print(f"📬 Found {len(notifications)} notification(s):")
        for notif in notifications[:5]:  # Show first 5
            print(f"  - {notif['information']['title']} (Priority: {notif['context']['priority']})")
        print()

        # Get current subscriptions
        print("Getting current subscriptions...")
        subs_result = await session.call_tool("get_my_subscriptions", arguments={})
        print(subs_result.content[0].text)
        print()

        # Unsubscribe
        print("Unsubscribing from 'demo' channel...")
        unsub_result = await session.call_tool(
            "unsubscribe_from_channel",
            arguments={"channel": "demo"},
        )
        print(f"✅ {unsub_result.content[0].text}")
        print()

        print("✅ Demo complete!")
        print()
        print("💡 Tips:")
        print("  - Multiple clients can connect simultaneously to the HTTP server")
        print("  - Notifications are shared across all connected clients")
        print("  - Use SQLite storage for persistent notifications across restarts")
        print("  - For production use, upgrade to Enterprise Edition for authentication")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Disconnected")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure the HTTP server is running:")
        print("   NOTIFY_MCP_TRANSPORT_TYPE=http uv run python -m notify_mcp")
