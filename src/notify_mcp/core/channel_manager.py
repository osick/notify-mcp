"""Channel management."""

from datetime import datetime

from ..models import Channel, ChannelPermissions
from .storage_adapter import StorageAdapter


class ChannelManager:
    """Manages notification channels."""

    def __init__(self, storage: StorageAdapter):
        """Initialize channel manager.

        Args:
            storage: Storage adapter
        """
        self.storage = storage

    async def create_channel(
        self,
        channel_id: str,
        name: str,
        created_by: str,
        description: str | None = None,
        permissions: ChannelPermissions | None = None,
        metadata: dict | None = None,
    ) -> Channel:
        """Create a new channel.

        Args:
            channel_id: Unique channel identifier
            name: Channel display name
            created_by: User who created the channel
            description: Optional description
            permissions: Optional permissions (defaults to public)
            metadata: Optional metadata

        Returns:
            Created channel

        Raises:
            ValueError: If channel already exists
        """
        existing = await self.storage.get_channel(channel_id)
        if existing:
            raise ValueError(f"Channel {channel_id} already exists")

        channel = Channel(
            id=channel_id,
            name=name,
            description=description,
            createdAt=datetime.now(),
            createdBy=created_by,
            permissions=permissions or ChannelPermissions(),
            metadata=metadata or {},
        )

        await self.storage.save_channel(channel)
        return channel

    async def get_channel(self, channel_id: str) -> Channel | None:
        """Get a channel by ID.

        Args:
            channel_id: Channel identifier

        Returns:
            Channel or None if not found
        """
        return await self.storage.get_channel(channel_id)

    async def delete_channel(self, channel_id: str) -> None:
        """Delete a channel.

        Args:
            channel_id: Channel identifier
        """
        await self.storage.delete_channel(channel_id)

    async def list_channels(self) -> list[Channel]:
        """List all channels.

        Returns:
            List of all channels
        """
        return await self.storage.list_channels()

    async def update_channel_stats(
        self, channel_id: str, notification_count: int | None = None
    ) -> None:
        """Update channel statistics.

        Args:
            channel_id: Channel identifier
            notification_count: New notification count
        """
        channel = await self.storage.get_channel(channel_id)
        if not channel:
            return

        if notification_count is not None:
            channel.notificationCount = notification_count
            channel.lastNotificationAt = datetime.now()

        await self.storage.save_channel(channel)
