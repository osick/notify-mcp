"""Subscription management."""

import uuid
from datetime import datetime

from ..models import Subscription, SubscriptionFilter
from .storage_adapter import StorageAdapter


class SubscriptionManager:
    """Manages client subscriptions to channels."""

    def __init__(self, storage: StorageAdapter):
        """Initialize subscription manager.

        Args:
            storage: Storage adapter
        """
        self.storage = storage

    async def subscribe(
        self, client_id: str, channel: str, filters: SubscriptionFilter | None = None
    ) -> Subscription:
        """Subscribe client to a channel.

        Args:
            client_id: Client identifier
            channel: Channel to subscribe to
            filters: Optional filter criteria

        Returns:
            Created subscription
        """
        subscription = Subscription(
            id=f"sub-{uuid.uuid4().hex[:12]}",
            clientId=client_id,
            channel=channel,
            subscribedAt=datetime.now(),
            filters=filters or SubscriptionFilter(),
        )

        await self.storage.save_subscription(subscription)
        return subscription

    async def unsubscribe(self, client_id: str, channel: str) -> bool:
        """Unsubscribe client from a channel.

        Args:
            client_id: Client identifier
            channel: Channel to unsubscribe from

        Returns:
            True if unsubscribed, False if not subscribed
        """
        subscriptions = await self.storage.get_subscriptions_by_client(client_id)

        for sub in subscriptions:
            if sub.channel == channel:
                await self.storage.delete_subscription(sub.id)
                return True

        return False

    async def get_subscribers(self, channel: str) -> list[Subscription]:
        """Get all subscribers for a channel.

        Args:
            channel: Channel name

        Returns:
            List of subscriptions
        """
        return await self.storage.get_subscriptions_by_channel(channel)

    async def get_client_subscriptions(self, client_id: str) -> list[Subscription]:
        """Get all subscriptions for a client.

        Args:
            client_id: Client identifier

        Returns:
            List of subscriptions
        """
        return await self.storage.get_subscriptions_by_client(client_id)
