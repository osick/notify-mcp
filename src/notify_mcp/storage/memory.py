"""In-memory storage implementation."""

from collections import defaultdict

from ..core.storage_adapter import StorageAdapter
from ..models import Channel, Notification, Subscription


class InMemoryStorage(StorageAdapter):
    """In-memory storage implementation using Python dictionaries."""

    def __init__(self, max_history_per_channel: int = 1000):
        """Initialize in-memory storage.

        Args:
            max_history_per_channel: Maximum notifications to keep per channel
        """
        self.max_history = max_history_per_channel

        # Storage dictionaries
        self._channels: dict[str, Channel] = {}
        self._subscriptions: dict[str, Subscription] = {}
        self._notifications: dict[str, list[Notification]] = defaultdict(list)

        # Indexes for faster lookups
        self._subscriptions_by_channel: dict[str, list[str]] = defaultdict(list)
        self._subscriptions_by_client: dict[str, list[str]] = defaultdict(list)

    # Channel operations
    async def save_channel(self, channel: Channel) -> None:
        """Save a channel."""
        self._channels[channel.id] = channel

    async def get_channel(self, channel_id: str) -> Channel | None:
        """Get a channel by ID."""
        return self._channels.get(channel_id)

    async def delete_channel(self, channel_id: str) -> None:
        """Delete a channel."""
        if channel_id in self._channels:
            del self._channels[channel_id]

        # Clean up related subscriptions
        if channel_id in self._subscriptions_by_channel:
            sub_ids = self._subscriptions_by_channel[channel_id].copy()
            for sub_id in sub_ids:
                await self.delete_subscription(sub_id)
            del self._subscriptions_by_channel[channel_id]

        # Clean up notifications
        if channel_id in self._notifications:
            del self._notifications[channel_id]

    async def list_channels(self) -> list[Channel]:
        """List all channels."""
        return list(self._channels.values())

    # Subscription operations
    async def save_subscription(self, subscription: Subscription) -> None:
        """Save a subscription."""
        self._subscriptions[subscription.id] = subscription

        # Update indexes
        if subscription.id not in self._subscriptions_by_channel[subscription.channel]:
            self._subscriptions_by_channel[subscription.channel].append(subscription.id)

        if subscription.id not in self._subscriptions_by_client[subscription.clientId]:
            self._subscriptions_by_client[subscription.clientId].append(subscription.id)

    async def delete_subscription(self, subscription_id: str) -> None:
        """Delete a subscription."""
        if subscription_id not in self._subscriptions:
            return

        subscription = self._subscriptions[subscription_id]

        # Remove from indexes
        if subscription.channel in self._subscriptions_by_channel:
            if subscription_id in self._subscriptions_by_channel[subscription.channel]:
                self._subscriptions_by_channel[subscription.channel].remove(subscription_id)

        if subscription.clientId in self._subscriptions_by_client:
            if subscription_id in self._subscriptions_by_client[subscription.clientId]:
                self._subscriptions_by_client[subscription.clientId].remove(subscription_id)

        # Delete subscription
        del self._subscriptions[subscription_id]

    async def get_subscriptions_by_channel(self, channel: str) -> list[Subscription]:
        """Get all subscriptions for a channel."""
        sub_ids = self._subscriptions_by_channel.get(channel, [])
        return [self._subscriptions[sub_id] for sub_id in sub_ids if sub_id in self._subscriptions]

    async def get_subscriptions_by_client(self, client_id: str) -> list[Subscription]:
        """Get all subscriptions for a client."""
        sub_ids = self._subscriptions_by_client.get(client_id, [])
        return [self._subscriptions[sub_id] for sub_id in sub_ids if sub_id in self._subscriptions]

    # Notification operations
    async def save_notification(self, notification: Notification) -> None:
        """Save a notification."""
        channel = notification.metadata.channel
        if channel:
            self._notifications[channel].append(notification)

            # Trim to max history (LRU - keep most recent)
            if len(self._notifications[channel]) > self.max_history:
                self._notifications[channel] = self._notifications[channel][-self.max_history:]

    async def get_notifications(
        self, channel: str, limit: int = 50
    ) -> list[Notification]:
        """Get recent notifications from a channel."""
        notifications = self._notifications.get(channel, [])
        return notifications[-limit:] if len(notifications) > limit else notifications

    async def get_notification_count(self, channel: str) -> int:
        """Get total notification count for a channel."""
        return len(self._notifications.get(channel, []))
