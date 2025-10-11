"""Tests for storage implementations."""

import pytest
from datetime import datetime

from notify_mcp.storage.memory import InMemoryStorage
from notify_mcp.models import (
    Channel,
    ChannelPermissions,
    Notification,
    Sender,
    Context,
    Information,
    Metadata,
    Subscription,
    SubscriptionFilter,
)


@pytest.fixture
def storage():
    """Create a fresh in-memory storage instance."""
    return InMemoryStorage(max_history_per_channel=100)


@pytest.fixture
def sample_channel():
    """Create a sample channel."""
    return Channel(
        id="test-channel",
        name="Test Channel",
        description="A test channel",
        createdAt=datetime.now(),
        createdBy="test-user",
        permissions=ChannelPermissions(),
    )


@pytest.fixture
def sample_notification():
    """Create a sample notification."""
    return Notification(
        schema_version="1.0.0",
        sender=Sender(id="user123", name="Alice", role="dev"),
        context=Context(theme="info", priority="medium", tags=["test"]),
        information=Information(title="Test", body="Test notification", format="text"),
        metadata=Metadata(
            id="notif-123",
            timestamp=datetime.now(),
            channel="test-channel",
            sequence=1,
        ),
    )


@pytest.fixture
def sample_subscription():
    """Create a sample subscription."""
    return Subscription(
        id="sub-123",
        clientId="client-456",
        channel="test-channel",
        subscribedAt=datetime.now(),
        filters=SubscriptionFilter(),
    )


class TestInMemoryStorage:
    """Test in-memory storage implementation."""

    @pytest.mark.asyncio
    async def test_save_and_get_channel(self, storage, sample_channel):
        """Test saving and retrieving a channel."""
        await storage.save_channel(sample_channel)

        retrieved = await storage.get_channel("test-channel")
        assert retrieved is not None
        assert retrieved.id == "test-channel"
        assert retrieved.name == "Test Channel"

    @pytest.mark.asyncio
    async def test_get_nonexistent_channel(self, storage):
        """Test getting a channel that doesn't exist."""
        result = await storage.get_channel("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_list_channels(self, storage):
        """Test listing all channels."""
        channel1 = Channel(
            id="channel1",
            name="Channel 1",
            createdAt=datetime.now(),
            createdBy="user",
            permissions=ChannelPermissions(),
        )
        channel2 = Channel(
            id="channel2",
            name="Channel 2",
            createdAt=datetime.now(),
            createdBy="user",
            permissions=ChannelPermissions(),
        )

        await storage.save_channel(channel1)
        await storage.save_channel(channel2)

        channels = await storage.list_channels()
        assert len(channels) == 2
        assert any(ch.id == "channel1" for ch in channels)
        assert any(ch.id == "channel2" for ch in channels)

    @pytest.mark.asyncio
    async def test_save_and_get_notification(self, storage, sample_notification):
        """Test saving and retrieving notifications."""
        await storage.save_notification(sample_notification)

        notifications = await storage.get_notifications("test-channel", limit=10)
        assert len(notifications) == 1
        assert notifications[0].metadata.id == "notif-123"

    @pytest.mark.asyncio
    async def test_notification_history_limit(self, storage):
        """Test that notification history respects max limit."""
        storage = InMemoryStorage(max_history_per_channel=5)

        # Add 10 notifications
        for i in range(10):
            notification = Notification(
                schema_version="1.0.0",
                sender=Sender(id="user", name="User", role="dev"),
                context=Context(theme="info", priority="medium", tags=[]),
                information=Information(title=f"Test {i}", body=f"Body {i}", format="text"),
                metadata=Metadata(
                    id=f"notif-{i}",
                    timestamp=datetime.now(),
                    channel="test",
                    sequence=i,
                ),
            )
            await storage.save_notification(notification)

        # Should only keep last 5
        notifications = await storage.get_notifications("test", limit=100)
        assert len(notifications) == 5

        # Should be the last 5 (5-9)
        ids = [n.metadata.id for n in notifications]
        assert "notif-9" in ids
        assert "notif-5" in ids
        assert "notif-0" not in ids

    @pytest.mark.asyncio
    async def test_get_notification_count(self, storage, sample_notification):
        """Test getting notification count for a channel."""
        await storage.save_notification(sample_notification)

        count = await storage.get_notification_count("test-channel")
        assert count == 1

        # Add another
        notification2 = Notification(
            schema_version="1.0.0",
            sender=Sender(id="user", name="User", role="dev"),
            context=Context(theme="info", priority="medium", tags=[]),
            information=Information(title="Test 2", body="Body 2", format="text"),
            metadata=Metadata(
                id="notif-124",
                timestamp=datetime.now(),
                channel="test-channel",
                sequence=2,
            ),
        )
        await storage.save_notification(notification2)

        count = await storage.get_notification_count("test-channel")
        assert count == 2

    @pytest.mark.asyncio
    async def test_save_and_get_subscription(self, storage, sample_subscription):
        """Test saving and retrieving subscriptions."""
        await storage.save_subscription(sample_subscription)

        # Get via channel lookup
        subscriptions = await storage.get_subscriptions_by_channel("test-channel")
        assert len(subscriptions) == 1
        assert subscriptions[0].clientId == "client-456"
        assert subscriptions[0].channel == "test-channel"

    @pytest.mark.asyncio
    async def test_get_subscriptions_by_channel(self, storage):
        """Test getting all subscriptions for a channel."""
        sub1 = Subscription(
            id="sub-1",
            clientId="client-1",
            channel="test-channel",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(),
        )
        sub2 = Subscription(
            id="sub-2",
            clientId="client-2",
            channel="test-channel",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(),
        )
        sub3 = Subscription(
            id="sub-3",
            clientId="client-3",
            channel="other-channel",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(),
        )

        await storage.save_subscription(sub1)
        await storage.save_subscription(sub2)
        await storage.save_subscription(sub3)

        subscriptions = await storage.get_subscriptions_by_channel("test-channel")
        assert len(subscriptions) == 2
        assert all(sub.channel == "test-channel" for sub in subscriptions)

    @pytest.mark.asyncio
    async def test_get_subscriptions_by_client(self, storage):
        """Test getting all subscriptions for a client."""
        sub1 = Subscription(
            id="sub-1",
            clientId="client-1",
            channel="channel-1",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(),
        )
        sub2 = Subscription(
            id="sub-2",
            clientId="client-1",
            channel="channel-2",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(),
        )
        sub3 = Subscription(
            id="sub-3",
            clientId="client-2",
            channel="channel-1",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(),
        )

        await storage.save_subscription(sub1)
        await storage.save_subscription(sub2)
        await storage.save_subscription(sub3)

        subscriptions = await storage.get_subscriptions_by_client("client-1")
        assert len(subscriptions) == 2
        assert all(sub.clientId == "client-1" for sub in subscriptions)

    @pytest.mark.asyncio
    async def test_delete_subscription(self, storage, sample_subscription):
        """Test deleting a subscription."""
        await storage.save_subscription(sample_subscription)

        # Verify it exists
        subscriptions = await storage.get_subscriptions_by_channel("test-channel")
        assert len(subscriptions) == 1

        # Delete it
        await storage.delete_subscription(sample_subscription.id)

        # Verify it's gone
        by_channel = await storage.get_subscriptions_by_channel("test-channel")
        assert len(by_channel) == 0

        by_client = await storage.get_subscriptions_by_client("client-456")
        assert len(by_client) == 0
