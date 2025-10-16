"""Main MCP server implementation."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)

from .config.storage_config import StorageSettings
from .config.transport_config import TransportSettings
from .core.channel_manager import ChannelManager
from .core.notification_router import NotificationRouter
from .core.notification_validator import NotificationValidator
from .core.subscription_manager import SubscriptionManager
from .models import (
    Context,
    Information,
    Metadata,
    Notification,
    Sender,
    SubscriptionFilter,
)
from .storage.factory import close_storage, create_storage

logger = logging.getLogger(__name__)


class NotifyMCPServer:
    """Notify-MCP server implementation."""

    def __init__(self):
        """Initialize the server."""
        # Storage will be initialized asynchronously in run()
        self.storage = None  # type: ignore
        self.validator = NotificationValidator()
        self.subscription_manager = None  # type: ignore
        self.channel_manager = None  # type: ignore
        self.router = None  # type: ignore

        # Create MCP server
        self.server = Server("notify-mcp")

        # Multi-client support
        self.active_clients: dict[str, dict] = {}  # client_id -> session info
        self._client_context: Optional[str] = None  # Current request context

        # Sequence counters per channel
        self.sequences: dict[str, int] = {}

        # Register handlers
        self._register_tool_handlers()
        self._register_resource_handlers()
        self._register_prompt_handlers()

    @property
    def current_client_id(self) -> str:
        """Get current client ID from context.

        For stdio: Returns fixed "stdio-client"
        For HTTP: Returns session-specific client ID from context
        """
        if self._client_context:
            return self._client_context
        return "stdio-client"  # Fallback for stdio mode

    def _get_next_sequence(self, channel: str) -> int:
        """Get next sequence number for a channel."""
        if channel not in self.sequences:
            self.sequences[channel] = 0
        self.sequences[channel] += 1
        return self.sequences[channel]

    def _register_tool_handlers(self) -> None:
        """Register MCP tool handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="publish_notification",
                    description="Publish a notification to a channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {"type": "string", "description": "Channel name"},
                            "title": {"type": "string", "description": "Notification title"},
                            "body": {"type": "string", "description": "Notification body"},
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "default": "medium",
                            },
                            "theme": {
                                "type": "string",
                                "enum": [
                                    "architecture-decision",
                                    "state-update",
                                    "memory-sync",
                                    "question",
                                    "decision",
                                    "alert",
                                    "info",
                                    "discussion",
                                ],
                                "default": "info",
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": [],
                            },
                        },
                        "required": ["channel", "title", "body"],
                    },
                ),
                Tool(
                    name="subscribe_to_channel",
                    description="Subscribe to notifications from a channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {"type": "string", "description": "Channel name"},
                            "priority_filter": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by priority levels",
                            },
                            "tag_filter": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by tags",
                            },
                        },
                        "required": ["channel"],
                    },
                ),
                Tool(
                    name="unsubscribe_from_channel",
                    description="Unsubscribe from a channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {"type": "string", "description": "Channel name"},
                        },
                        "required": ["channel"],
                    },
                ),
                Tool(
                    name="list_channels",
                    description="List all available channels",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="create_channel",
                    description="Create a new notification channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel_id": {
                                "type": "string",
                                "description": "Unique channel ID",
                            },
                            "name": {"type": "string", "description": "Channel name"},
                            "description": {
                                "type": "string",
                                "description": "Channel description",
                            },
                        },
                        "required": ["channel_id", "name"],
                    },
                ),
                Tool(
                    name="get_my_subscriptions",
                    description="Get current user's subscriptions",
                    inputSchema={"type": "object", "properties": {}},
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Call a tool."""
            if name == "publish_notification":
                return await self._publish_notification(arguments)
            elif name == "subscribe_to_channel":
                return await self._subscribe_to_channel(arguments)
            elif name == "unsubscribe_from_channel":
                return await self._unsubscribe_from_channel(arguments)
            elif name == "list_channels":
                return await self._list_channels()
            elif name == "create_channel":
                return await self._create_channel(arguments)
            elif name == "get_my_subscriptions":
                return await self._get_my_subscriptions()
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _publish_notification(self, args: dict) -> list[TextContent]:
        """Publish notification tool handler."""
        channel = args["channel"]

        # Create notification
        notification = Notification(
            schemaVersion="1.0.0",
            sender=Sender(
                id=self.current_client_id,
                name="MCP Client",
                role="dev",
            ),
            context=Context(
                theme=args.get("theme", "info"),
                priority=args.get("priority", "medium"),
                tags=args.get("tags", []),
            ),
            information=Information(
                title=args["title"],
                body=args["body"],
                format="text",
            ),
            metadata=Metadata(
                id="",  # Will be generated
                timestamp=datetime.now(),
            ),
        )

        # Validate and enrich
        sequence = self._get_next_sequence(channel)
        notification = self.validator.validate_and_enrich(notification, channel, sequence)

        # Save notification
        await self.storage.save_notification(notification)

        # Route to subscribers (in stdio mode, notifications are stored, not pushed)
        stats = await self.router.route_notification(notification)

        # Update channel stats
        count = await self.storage.get_notification_count(channel)
        await self.channel_manager.update_channel_stats(channel, count)

        # Get subscriber count for this channel
        subscriptions = await self.subscription_manager.get_subscribers(channel)
        subscriber_count = len(subscriptions)

        return [
            TextContent(
                type="text",
                text=f"✅ Notification published to {channel}\n"
                f"ID: {notification.metadata.id}\n"
                f"Stored for {subscriber_count} subscriber(s)\n"
                f"Filtered out: {stats['filtered']} subscriber(s)\n\n"
                f"💡 Retrieve via resource: notification://{channel}/recent",
            )
        ]

    async def _subscribe_to_channel(self, args: dict) -> list[TextContent]:
        """Subscribe to channel tool handler."""
        channel = args["channel"]

        # Build filter
        filters = SubscriptionFilter(
            priority=args.get("priority_filter"),
            tags=args.get("tag_filter"),
        )

        # Subscribe
        subscription = await self.subscription_manager.subscribe(
            self.current_client_id, channel, filters
        )

        return [
            TextContent(
                type="text",
                text=f"✅ Subscribed to channel: {channel}\n"
                f"Subscription ID: {subscription.id}\n"
                f"Filters: {filters.model_dump(exclude_none=True)}",
            )
        ]

    async def _unsubscribe_from_channel(self, args: dict) -> list[TextContent]:
        """Unsubscribe from channel tool handler."""
        channel = args["channel"]

        success = await self.subscription_manager.unsubscribe(self.current_client_id, channel)

        if success:
            return [TextContent(type="text", text=f"✅ Unsubscribed from channel: {channel}")]
        else:
            return [TextContent(type="text", text=f"❌ Not subscribed to channel: {channel}")]

    async def _list_channels(self) -> list[TextContent]:
        """List channels tool handler."""
        channels = await self.channel_manager.list_channels()

        if not channels:
            return [TextContent(type="text", text="No channels available")]

        lines = ["📢 Available Channels:\n"]
        for ch in channels:
            lines.append(f"• {ch.name} ({ch.id})")
            lines.append(f"  {ch.description or 'No description'}")
            lines.append(f"  Subscribers: {ch.subscriberCount}, Notifications: {ch.notificationCount}\n")

        return [TextContent(type="text", text="\n".join(lines))]

    async def _create_channel(self, args: dict) -> list[TextContent]:
        """Create channel tool handler."""
        try:
            channel = await self.channel_manager.create_channel(
                channel_id=args["channel_id"],
                name=args["name"],
                description=args.get("description"),
                created_by=self.current_client_id,
            )

            return [
                TextContent(
                    type="text",
                    text=f"✅ Channel created: {channel.name} ({channel.id})",
                )
            ]
        except ValueError as e:
            return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

    async def _get_my_subscriptions(self) -> list[TextContent]:
        """Get subscriptions tool handler."""
        subscriptions = await self.subscription_manager.get_client_subscriptions(
            self.current_client_id
        )

        if not subscriptions:
            return [TextContent(type="text", text="No active subscriptions")]

        lines = ["📬 Your Subscriptions:\n"]
        for sub in subscriptions:
            lines.append(f"• Channel: {sub.channel}")
            lines.append(f"  Subscribed: {sub.subscribedAt.isoformat()}")
            if sub.filters.priority or sub.filters.tags:
                lines.append(f"  Filters: {sub.filters.model_dump(exclude_none=True)}\n")

        return [TextContent(type="text", text="\n".join(lines))]

    def _register_resource_handlers(self) -> None:
        """Register MCP resource handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            resources = []

            # Add notification schema resource
            resources.append(
                Resource(
                    uri="schema://notification",
                    name="Notification Schema",
                    description="JSON Schema for notification structure",
                    mimeType="application/json",
                )
            )

            # Add resource for each channel
            channels = await self.channel_manager.list_channels()
            for channel in channels:
                resources.append(
                    Resource(
                        uri=f"notification://{channel.id}/recent",
                        name=f"Recent Notifications - {channel.name}",
                        description=f"Last 50 notifications from {channel.name}",
                        mimeType="application/json",
                    )
                )
                resources.append(
                    Resource(
                        uri=f"channel://{channel.id}/info",
                        name=f"{channel.name} Info",
                        description=f"Channel information for {channel.name}",
                        mimeType="application/json",
                    )
                )

            return resources

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource."""
            # Convert AnyUrl to string if needed
            uri_str = str(uri)
            parts = uri_str.split("://")
            if len(parts) != 2:
                raise ValueError(f"Invalid URI: {uri}")

            scheme, path = parts

            if scheme == "schema":
                # schema://notification
                if path == "notification":
                    # Find schema file relative to package
                    schema_path = Path(__file__).parent.parent.parent / "schemas" / "notification-schema.json"

                    if not schema_path.exists():
                        raise ValueError(f"Schema file not found: {schema_path}")

                    return schema_path.read_text()
                else:
                    raise ValueError(f"Unknown schema: {path}")

            elif scheme == "notification":
                # notification://<channel>/recent
                channel_path = path.split("/")
                if len(channel_path) < 2:
                    raise ValueError(f"Invalid notification URI: {uri}")

                channel = channel_path[0]
                notifications = await self.storage.get_notifications(channel, limit=50)

                return json.dumps(
                    [n.model_dump(mode="json", exclude_none=True) for n in notifications],
                    indent=2,
                )

            elif scheme == "channel":
                # channel://<channel>/info
                channel_id = path.split("/")[0]
                channel = await self.channel_manager.get_channel(channel_id)

                if not channel:
                    raise ValueError(f"Channel not found: {channel_id}")

                return json.dumps(channel.model_dump(mode="json", exclude_none=True), indent=2)

            else:
                raise ValueError(f"Unknown resource scheme: {scheme}")

    def _register_prompt_handlers(self) -> None:
        """Register MCP prompt handlers."""

        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List available prompts."""
            return [
                Prompt(
                    name="create_decision_notification",
                    description="Template for architecture decision notifications",
                    arguments=[
                        {"name": "decision_title", "description": "Title of decision", "required": True},
                        {"name": "context", "description": "Background context", "required": True},
                        {"name": "decision", "description": "What was decided", "required": True},
                    ],
                ),
                Prompt(
                    name="send_alert",
                    description="Template for critical alerts",
                    arguments=[
                        {"name": "alert_title", "description": "Alert title", "required": True},
                        {"name": "severity", "description": "Severity level", "required": True},
                        {"name": "impact", "description": "Impact description", "required": True},
                    ],
                ),
            ]

        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
            """Get a prompt."""
            if name == "create_decision_notification":
                return GetPromptResult(
                    description="Architecture decision notification template",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"""Create an architecture decision notification with:

Title: {arguments.get('decision_title', 'N/A')}
Context: {arguments.get('context', 'N/A')}
Decision: {arguments.get('decision', 'N/A')}

Format as a professional team notification in markdown.""",
                            ),
                        )
                    ],
                )
            elif name == "send_alert":
                return GetPromptResult(
                    description="Critical alert notification template",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"""Create a critical alert notification:

Title: {arguments.get('alert_title', 'N/A')}
Severity: {arguments.get('severity', 'N/A')}
Impact: {arguments.get('impact', 'N/A')}

Format as an urgent team alert.""",
                            ),
                        )
                    ],
                )
            else:
                raise ValueError(f"Unknown prompt: {name}")

    async def _initialize_server(self) -> None:
        """Initialize server components (storage, managers, default channel)."""
        # Initialize storage from configuration
        settings = StorageSettings()
        logger.info(f"Storage configuration: type={settings.storage_type}")
        self.storage = await create_storage(settings)

        # Initialize managers that depend on storage
        self.subscription_manager = SubscriptionManager(self.storage)
        self.channel_manager = ChannelManager(self.storage)
        self.router = NotificationRouter(self.storage, self.subscription_manager)

        # Create default channel
        try:
            await self.channel_manager.create_channel(
                channel_id="general",
                name="General",
                description="General team notifications",
                created_by="system",
            )
            logger.info("Created default 'general' channel")
        except ValueError:
            pass  # Channel already exists

    async def _shutdown_server(self) -> None:
        """Cleanup server resources."""
        logger.info("Shutting down server...")
        await close_storage(self.storage)

    async def run_stdio(self) -> None:
        """Run server with stdio transport (single client)."""
        logger.info("Starting Notify-MCP server with stdio transport...")

        await self._initialize_server()

        try:
            self._client_context = "stdio-client"
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options(),
                )
        finally:
            await self._shutdown_server()

    async def run_http(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Run server with HTTP transport (multi-client).

        Args:
            host: Host address to bind to
            port: Port to listen on
        """
        logger.info(f"Starting Notify-MCP server with HTTP transport on {host}:{port}...")

        await self._initialize_server()

        try:
            # Create session manager for multi-client support
            session_manager = StreamableHTTPSessionManager(self.server)

            # Run HTTP server context
            async with session_manager.run():
                # Import uvicorn for HTTP server
                import uvicorn

                # Create ASGI app that uses session_manager.handle_request
                async def app(scope, receive, send):
                    """ASGI app that delegates to session manager."""
                    await session_manager.handle_request(scope, receive, send)

                # Run HTTP server
                config = uvicorn.Config(app, host=host, port=port, log_level="info")
                server = uvicorn.Server(config)
                await server.serve()

        finally:
            await self._shutdown_server()

    async def run(self, transport: Optional[str] = None) -> None:
        """Run server with configured transport.

        Args:
            transport: Transport type ("stdio" or "http"). If None, reads from config.
        """
        # Get transport settings
        settings = TransportSettings()
        transport_type = transport or settings.transport_type

        logger.info(f"Transport: {transport_type}")

        if transport_type == "stdio":
            await self.run_stdio()
        elif transport_type == "http":
            await self.run_http(
                host=settings.http_host,
                port=settings.http_port,
            )
        else:
            raise ValueError(f"Unknown transport type: {transport_type}")
