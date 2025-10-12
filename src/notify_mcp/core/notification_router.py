"""Notification routing logic."""

import logging
from collections.abc import Awaitable, Callable

from ..models import Notification
from ..utils.filters import matches_filter
from .storage_adapter import StorageAdapter
from .subscription_manager import SubscriptionManager

logger = logging.getLogger(__name__)


class NotificationRouter:
    """Routes notifications to subscribed clients."""

    def __init__(
        self,
        storage: StorageAdapter,
        subscription_manager: SubscriptionManager,
    ):
        """Initialize notification router.

        Args:
            storage: Storage adapter
            subscription_manager: Subscription manager
        """
        self.storage = storage
        self.subscription_manager = subscription_manager

        # Callback for delivering notifications to clients
        # Will be set by MCP server
        self.notification_callback: Callable[[str, Notification], Awaitable[None]] | None = None

    def set_notification_callback(
        self, callback: Callable[[str, Notification], Awaitable[None]]
    ) -> None:
        """Set the callback function for notification delivery.

        Args:
            callback: Async function(client_id, notification) to deliver notifications
        """
        self.notification_callback = callback

    async def route_notification(self, notification: Notification) -> dict[str, int]:
        """Route notification to subscribers.

        Args:
            notification: Notification to route

        Returns:
            Dictionary with delivery stats: {'delivered': count, 'filtered': count}
        """
        channel = notification.metadata.channel
        if not channel:
            logger.warning("Notification has no channel, cannot route")
            return {"delivered": 0, "filtered": 0}

        # Get all subscribers for this channel
        subscriptions = await self.subscription_manager.get_subscribers(channel)

        delivered = 0
        filtered = 0

        for subscription in subscriptions:
            # Apply filters
            if matches_filter(notification, subscription.filters):
                # Deliver to client
                if self.notification_callback:
                    try:
                        await self.notification_callback(
                            subscription.clientId, notification
                        )
                        delivered += 1
                    except Exception as e:
                        logger.error(
                            f"Failed to deliver notification to {subscription.clientId}: {e}"
                        )
                else:
                    logger.warning("No notification callback set, cannot deliver")
            else:
                filtered += 1

        logger.info(
            f"Routed notification to channel {channel}: "
            f"{delivered} delivered, {filtered} filtered out"
        )

        return {"delivered": delivered, "filtered": filtered}
