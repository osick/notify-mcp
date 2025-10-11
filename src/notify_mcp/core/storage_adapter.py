"""Abstract storage adapter interface."""

from abc import ABC, abstractmethod

from ..models import Channel, Notification, Subscription


class StorageAdapter(ABC):
    """Abstract base class for storage implementations."""

    # Channel operations
    @abstractmethod
    async def save_channel(self, channel: Channel) -> None:
        """Save a channel."""
        pass

    @abstractmethod
    async def get_channel(self, channel_id: str) -> Channel | None:
        """Get a channel by ID."""
        pass

    @abstractmethod
    async def delete_channel(self, channel_id: str) -> None:
        """Delete a channel."""
        pass

    @abstractmethod
    async def list_channels(self) -> list[Channel]:
        """List all channels."""
        pass

    # Subscription operations
    @abstractmethod
    async def save_subscription(self, subscription: Subscription) -> None:
        """Save a subscription."""
        pass

    @abstractmethod
    async def delete_subscription(self, subscription_id: str) -> None:
        """Delete a subscription."""
        pass

    @abstractmethod
    async def get_subscriptions_by_channel(self, channel: str) -> list[Subscription]:
        """Get all subscriptions for a channel."""
        pass

    @abstractmethod
    async def get_subscriptions_by_client(self, client_id: str) -> list[Subscription]:
        """Get all subscriptions for a client."""
        pass

    # Notification operations
    @abstractmethod
    async def save_notification(self, notification: Notification) -> None:
        """Save a notification."""
        pass

    @abstractmethod
    async def get_notifications(
        self, channel: str, limit: int = 50
    ) -> list[Notification]:
        """Get recent notifications from a channel."""
        pass

    @abstractmethod
    async def get_notification_count(self, channel: str) -> int:
        """Get total notification count for a channel."""
        pass
