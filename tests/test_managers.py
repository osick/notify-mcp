"""Tests for core managers."""

import pytest
from datetime import datetime

from notify_mcp.core.channel_manager import ChannelManager
from notify_mcp.core.subscription_manager import SubscriptionManager
from notify_mcp.core.notification_validator import NotificationValidator
from notify_mcp.core.notification_router import NotificationRouter
from notify_mcp.storage.memory import InMemoryStorage
from notify_mcp.models import (
    Notification,
    Sender,
    Context,
    Information,
    Metadata,
    SubscriptionFilter,
)


@pytest.fixture
def storage():
    """Create a fresh storage instance."""
    return InMemoryStorage()


@pytest.fixture
def channel_manager(storage):
    """Create a channel manager."""
    return ChannelManager(storage)


@pytest.fixture
def subscription_manager(storage):
    """Create a subscription manager."""
    return SubscriptionManager(storage)


@pytest.fixture
def validator():
    """Create a notification validator."""
    return NotificationValidator()


@pytest.fixture
def router(storage, subscription_manager):
    """Create a notification router."""
    return NotificationRouter(storage, subscription_manager)


class TestChannelManager:
    """Test channel manager."""

    @pytest.mark.asyncio
    async def test_create_channel(self, channel_manager):
        """Test creating a new channel."""
        channel = await channel_manager.create_channel(
            channel_id="test",
            name="Test Channel",
            description="A test channel",
            created_by="user",
        )

        assert channel.id == "test"
        assert channel.name == "Test Channel"
        assert channel.subscriberCount == 0

    @pytest.mark.asyncio
    async def test_create_duplicate_channel(self, channel_manager):
        """Test that creating duplicate channel raises error."""
        await channel_manager.create_channel(
            channel_id="test",
            name="Test Channel",
            created_by="user",
        )

        with pytest.raises(ValueError, match="already exists"):
            await channel_manager.create_channel(
                channel_id="test",
                name="Test Channel 2",
                created_by="user",
            )

    @pytest.mark.asyncio
    async def test_get_channel(self, channel_manager):
        """Test getting a channel."""
        await channel_manager.create_channel(
            channel_id="test",
            name="Test Channel",
            created_by="user",
        )

        channel = await channel_manager.get_channel("test")
        assert channel is not None
        assert channel.id == "test"

    @pytest.mark.asyncio
    async def test_update_channel_stats(self, channel_manager):
        """Test updating channel statistics."""
        channel = await channel_manager.create_channel(
            channel_id="test",
            name="Test Channel",
            created_by="user",
        )

        assert channel.notificationCount == 0

        await channel_manager.update_channel_stats("test", notification_count=10)

        updated = await channel_manager.get_channel("test")
        assert updated.notificationCount == 10


class TestSubscriptionManager:
    """Test subscription manager."""

    @pytest.mark.asyncio
    async def test_subscribe(self, subscription_manager):
        """Test subscribing to a channel."""
        subscription = await subscription_manager.subscribe(
            client_id="client-1",
            channel="test",
            filters=SubscriptionFilter(priority=["high", "critical"]),
        )

        assert subscription.clientId == "client-1"
        assert subscription.channel == "test"
        assert "high" in subscription.filters.priority

    @pytest.mark.asyncio
    async def test_subscribe_twice_creates_multiple(self, subscription_manager):
        """Test that subscribing twice creates multiple subscriptions."""
        sub1 = await subscription_manager.subscribe(
            client_id="client-1",
            channel="test",
            filters=SubscriptionFilter(),
        )

        sub2 = await subscription_manager.subscribe(
            client_id="client-1",
            channel="test",
            filters=SubscriptionFilter(priority=["high"]),
        )

        # Creates separate subscriptions (not idempotent in current implementation)
        assert sub1.id != sub2.id

        # Both should exist
        subscriptions = await subscription_manager.get_client_subscriptions("client-1")
        assert len(subscriptions) == 2

    @pytest.mark.asyncio
    async def test_unsubscribe(self, subscription_manager):
        """Test unsubscribing from a channel."""
        await subscription_manager.subscribe(
            client_id="client-1",
            channel="test",
            filters=SubscriptionFilter(),
        )

        success = await subscription_manager.unsubscribe("client-1", "test")
        assert success is True

        # Verify it's gone
        subscriptions = await subscription_manager.get_client_subscriptions("client-1")
        assert len(subscriptions) == 0

    @pytest.mark.asyncio
    async def test_unsubscribe_nonexistent(self, subscription_manager):
        """Test unsubscribing from non-existent subscription."""
        success = await subscription_manager.unsubscribe("client-1", "test")
        assert success is False

    @pytest.mark.asyncio
    async def test_get_subscribers(self, subscription_manager):
        """Test getting all subscribers for a channel."""
        await subscription_manager.subscribe("client-1", "test", SubscriptionFilter())
        await subscription_manager.subscribe("client-2", "test", SubscriptionFilter())
        await subscription_manager.subscribe("client-3", "other", SubscriptionFilter())

        subscribers = await subscription_manager.get_subscribers("test")
        assert len(subscribers) == 2
        assert any(sub.clientId == "client-1" for sub in subscribers)
        assert any(sub.clientId == "client-2" for sub in subscribers)


class TestNotificationValidator:
    """Test notification validator."""

    def test_enrich_notification(self):
        """Test enriching notification with metadata (without schema validation)."""
        # Skip schema validation tests since schema file may not exist
        # Focus on enrichment logic
        validator = NotificationValidator.__new__(NotificationValidator)
        validator.schema = {}  # Mock schema

        notification = Notification(
            schemaVersion="1.0.0",
            sender=Sender(id="user", name="User", role="dev"),
            context=Context(theme="info", priority="medium", tags=[]),
            information=Information(title="Test", body="Test body", format="text"),
            metadata=Metadata(id="", timestamp=datetime.now()),
        )

        enriched = validator.enrich_notification(notification, channel="test", sequence=42)

        # Should have generated ID
        assert enriched.metadata.id != ""
        assert enriched.metadata.id.startswith("notif-")

        # Should have channel and sequence
        assert enriched.metadata.channel == "test"
        assert enriched.metadata.sequence == 42


class TestNotificationRouter:
    """Test notification router."""

    @pytest.mark.asyncio
    async def test_route_to_subscribers(self, router, subscription_manager):
        """Test routing notification to subscribers."""
        # Subscribe two clients
        await subscription_manager.subscribe("client-1", "test", SubscriptionFilter())
        await subscription_manager.subscribe("client-2", "test", SubscriptionFilter())

        # Track deliveries
        deliveries = []

        async def callback(client_id: str, notification: Notification):
            deliveries.append(client_id)

        router.set_notification_callback(callback)

        # Route notification
        notification = Notification(
            schemaVersion="1.0.0",
            sender=Sender(id="user", name="User", role="dev"),
            context=Context(theme="info", priority="medium", tags=[]),
            information=Information(title="Test", body="Test body", format="text"),
            metadata=Metadata(
                id="test",
                timestamp=datetime.now(),
                channel="test",
                sequence=1,
            ),
        )

        stats = await router.route_notification(notification)

        assert stats["delivered"] == 2
        assert stats["filtered"] == 0
        assert "client-1" in deliveries
        assert "client-2" in deliveries

    @pytest.mark.asyncio
    async def test_route_with_priority_filter(self, router, subscription_manager):
        """Test routing with priority filtering."""
        # Subscribe with high priority filter
        await subscription_manager.subscribe(
            "client-1",
            "test",
            SubscriptionFilter(priority=["high", "critical"]),
        )

        deliveries = []

        async def callback(client_id: str, notification: Notification):
            deliveries.append(client_id)

        router.set_notification_callback(callback)

        # Send medium priority notification (should be filtered)
        notification_medium = Notification(
            schemaVersion="1.0.0",
            sender=Sender(id="user", name="User", role="dev"),
            context=Context(theme="info", priority="medium", tags=[]),
            information=Information(title="Test", body="Test body", format="text"),
            metadata=Metadata(
                id="test1",
                timestamp=datetime.now(),
                channel="test",
                sequence=1,
            ),
        )

        stats = await router.route_notification(notification_medium)
        assert stats["delivered"] == 0
        assert stats["filtered"] == 1

        # Send high priority notification (should be delivered)
        notification_high = Notification(
            schemaVersion="1.0.0",
            sender=Sender(id="user", name="User", role="dev"),
            context=Context(theme="alert", priority="high", tags=[]),
            information=Information(title="Test", body="Test body", format="text"),
            metadata=Metadata(
                id="test2",
                timestamp=datetime.now(),
                channel="test",
                sequence=2,
            ),
        )

        stats = await router.route_notification(notification_high)
        assert stats["delivered"] == 1
        assert stats["filtered"] == 0
        assert "client-1" in deliveries

    @pytest.mark.asyncio
    async def test_route_with_tag_filter(self, router, subscription_manager):
        """Test routing with tag filtering."""
        # Subscribe with tag filter
        await subscription_manager.subscribe(
            "client-1",
            "test",
            SubscriptionFilter(tags=["backend", "api"]),
        )

        deliveries = []

        async def callback(client_id: str, notification: Notification):
            deliveries.append(client_id)

        router.set_notification_callback(callback)

        # Send notification with matching tag
        notification = Notification(
            schemaVersion="1.0.0",
            sender=Sender(id="user", name="User", role="dev"),
            context=Context(theme="info", priority="medium", tags=["backend", "database"]),
            information=Information(title="Test", body="Test body", format="text"),
            metadata=Metadata(
                id="test",
                timestamp=datetime.now(),
                channel="test",
                sequence=1,
            ),
        )

        stats = await router.route_notification(notification)
        assert stats["delivered"] == 1
        assert "client-1" in deliveries
