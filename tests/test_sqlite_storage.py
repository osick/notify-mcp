"""Tests for SQLite storage adapter."""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile

from notify_mcp.storage.sqlite_storage import SQLiteStorage
from notify_mcp.models.channel import Channel, ChannelPermissions
from notify_mcp.models.subscription import Subscription, SubscriptionFilter
from notify_mcp.models.notification import (
    Notification,
    Sender,
    Context,
    Information,
    Metadata,
)


@pytest.fixture
async def sqlite_storage():
    """Create a temporary SQLite storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        storage = SQLiteStorage(db_path=str(db_path), max_history_per_channel=10)
        await storage.initialize()
        yield storage
        await storage.close()


class TestSQLiteStorage:
    """Test SQLite storage adapter."""

    async def test_save_and_get_channel(self, sqlite_storage):
        """Test saving and retrieving a channel."""
        channel = Channel(
            id="test-channel",
            name="Test Channel",
            description="Test description",
            createdAt=datetime.now(),
            createdBy="test-user",
            subscriberCount=5,
            notificationCount=10,
        )

        await sqlite_storage.save_channel(channel)
        retrieved = await sqlite_storage.get_channel("test-channel")

        assert retrieved is not None
        assert retrieved.id == channel.id
        assert retrieved.name == channel.name
        assert retrieved.description == channel.description
        assert retrieved.subscriberCount == channel.subscriberCount
        assert retrieved.notificationCount == channel.notificationCount

    async def test_update_channel(self, sqlite_storage):
        """Test updating an existing channel."""
        channel = Channel(
            id="test-channel",
            name="Test Channel",
            createdAt=datetime.now(),
            createdBy="test-user",
            subscriberCount=5,
        )

        await sqlite_storage.save_channel(channel)

        # Update the channel
        channel.subscriberCount = 10
        channel.name = "Updated Channel"
        await sqlite_storage.save_channel(channel)

        retrieved = await sqlite_storage.get_channel("test-channel")
        assert retrieved is not None
        assert retrieved.subscriberCount == 10
        assert retrieved.name == "Updated Channel"

    async def test_get_nonexistent_channel(self, sqlite_storage):
        """Test getting a channel that doesn't exist."""
        result = await sqlite_storage.get_channel("nonexistent")
        assert result is None

    async def test_list_channels(self, sqlite_storage):
        """Test listing all channels."""
        channel1 = Channel(
            id="channel1", name="Channel 1", createdAt=datetime.now(), createdBy="user1"
        )
        channel2 = Channel(
            id="channel2", name="Channel 2", createdAt=datetime.now(), createdBy="user2"
        )

        await sqlite_storage.save_channel(channel1)
        await sqlite_storage.save_channel(channel2)

        channels = await sqlite_storage.list_channels()
        assert len(channels) == 2
        assert any(ch.id == "channel1" for ch in channels)
        assert any(ch.id == "channel2" for ch in channels)

    async def test_delete_channel(self, sqlite_storage):
        """Test deleting a channel."""
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        await sqlite_storage.delete_channel("test-channel")
        retrieved = await sqlite_storage.get_channel("test-channel")
        assert retrieved is None

    async def test_save_and_get_subscription(self, sqlite_storage):
        """Test saving and retrieving a subscription."""
        # Create channel first
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create subscription
        subscription = Subscription(
            id="sub1",
            clientId="client1",
            channel="test-channel",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(priority=["high", "critical"]),
        )

        await sqlite_storage.save_subscription(subscription)

        # Retrieve by channel
        subs = await sqlite_storage.get_subscriptions_by_channel("test-channel")
        assert len(subs) == 1
        assert subs[0].id == "sub1"
        assert subs[0].clientId == "client1"
        assert subs[0].filters.priority == ["high", "critical"]

    async def test_get_subscriptions_by_client(self, sqlite_storage):
        """Test getting subscriptions by client ID."""
        # Create channels
        channel1 = Channel(
            id="channel1", name="Channel 1", createdAt=datetime.now(), createdBy="user"
        )
        channel2 = Channel(
            id="channel2", name="Channel 2", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel1)
        await sqlite_storage.save_channel(channel2)

        # Create subscriptions for same client
        sub1 = Subscription(
            id="sub1",
            clientId="client1",
            channel="channel1",
            subscribedAt=datetime.now(),
        )
        sub2 = Subscription(
            id="sub2",
            clientId="client1",
            channel="channel2",
            subscribedAt=datetime.now(),
        )

        await sqlite_storage.save_subscription(sub1)
        await sqlite_storage.save_subscription(sub2)

        # Retrieve by client
        subs = await sqlite_storage.get_subscriptions_by_client("client1")
        assert len(subs) == 2
        assert any(sub.channel == "channel1" for sub in subs)
        assert any(sub.channel == "channel2" for sub in subs)

    async def test_delete_subscription(self, sqlite_storage):
        """Test deleting a subscription."""
        # Create channel
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create subscription
        subscription = Subscription(
            id="sub1",
            clientId="client1",
            channel="test-channel",
            subscribedAt=datetime.now(),
        )
        await sqlite_storage.save_subscription(subscription)

        # Delete subscription
        await sqlite_storage.delete_subscription("sub1")

        # Verify deletion
        subs = await sqlite_storage.get_subscriptions_by_channel("test-channel")
        assert len(subs) == 0

    async def test_cascade_delete_subscriptions(self, sqlite_storage):
        """Test that deleting a channel cascades to subscriptions."""
        # Create channel
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create subscription
        subscription = Subscription(
            id="sub1",
            clientId="client1",
            channel="test-channel",
            subscribedAt=datetime.now(),
        )
        await sqlite_storage.save_subscription(subscription)

        # Delete channel
        await sqlite_storage.delete_channel("test-channel")

        # Verify subscriptions are also deleted
        subs = await sqlite_storage.get_subscriptions_by_channel("test-channel")
        assert len(subs) == 0

    async def test_save_and_get_notification(self, sqlite_storage):
        """Test saving and retrieving notifications."""
        # Create channel
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create notification
        notification = Notification(
            schemaVersion="1.0.0",
            sender=Sender(id="user1", name="User 1", role="dev"),
            context=Context(theme="info", priority="medium", tags=["test"]),
            information=Information(title="Test Notification", body="Test body"),
            metadata=Metadata(
                id="notif1", timestamp=datetime.now(), channel="test-channel", sequence=1
            ),
        )

        await sqlite_storage.save_notification(notification)

        # Retrieve notifications
        notifs = await sqlite_storage.get_notifications("test-channel", limit=10)
        assert len(notifs) == 1
        assert notifs[0].metadata.id == "notif1"
        assert notifs[0].information.title == "Test Notification"
        assert notifs[0].context.priority == "medium"

    async def test_notification_lru_cache(self, sqlite_storage):
        """Test that LRU cache limits notification history."""
        # Create channel
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create 15 notifications (max is 10)
        for i in range(15):
            notification = Notification(
                schemaVersion="1.0.0",
                sender=Sender(id="user1", name="User 1", role="dev"),
                context=Context(theme="info", priority="medium"),
                information=Information(title=f"Notification {i}", body="Test body"),
                metadata=Metadata(
                    id=f"notif{i}",
                    timestamp=datetime.now(),
                    channel="test-channel",
                    sequence=i,
                ),
            )
            await sqlite_storage.save_notification(notification)

        # Should only have 10 most recent
        notifs = await sqlite_storage.get_notifications("test-channel", limit=20)
        assert len(notifs) == 10

        # Should have notifications 5-14 (oldest 0-4 deleted)
        titles = [n.information.title for n in notifs]
        assert "Notification 0" not in titles
        assert "Notification 4" not in titles
        assert "Notification 5" in titles
        assert "Notification 14" in titles

    async def test_get_notification_count(self, sqlite_storage):
        """Test getting notification count."""
        # Create channel
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create 5 notifications
        for i in range(5):
            notification = Notification(
                schemaVersion="1.0.0",
                sender=Sender(id="user1", name="User 1", role="dev"),
                context=Context(theme="info", priority="medium"),
                information=Information(title=f"Notification {i}", body="Test"),
                metadata=Metadata(
                    id=f"notif{i}",
                    timestamp=datetime.now(),
                    channel="test-channel",
                    sequence=i,
                ),
            )
            await sqlite_storage.save_notification(notification)

        count = await sqlite_storage.get_notification_count("test-channel")
        assert count == 5

    async def test_notification_ordering(self, sqlite_storage):
        """Test that notifications are returned in reverse chronological order."""
        # Create channel
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create notifications with different timestamps
        import time

        for i in range(3):
            notification = Notification(
                schemaVersion="1.0.0",
                sender=Sender(id="user1", name="User 1", role="dev"),
                context=Context(theme="info", priority="medium"),
                information=Information(title=f"Notification {i}", body="Test"),
                metadata=Metadata(
                    id=f"notif{i}",
                    timestamp=datetime.now(),
                    channel="test-channel",
                    sequence=i,
                ),
            )
            await sqlite_storage.save_notification(notification)
            time.sleep(0.01)  # Small delay to ensure different timestamps

        # Retrieve notifications
        notifs = await sqlite_storage.get_notifications("test-channel", limit=10)

        # Should be in reverse order (most recent first)
        assert notifs[0].information.title == "Notification 2"
        assert notifs[1].information.title == "Notification 1"
        assert notifs[2].information.title == "Notification 0"

    async def test_pagination(self, sqlite_storage):
        """Test notification pagination."""
        # Create channel
        channel = Channel(
            id="test-channel", name="Test", createdAt=datetime.now(), createdBy="user"
        )
        await sqlite_storage.save_channel(channel)

        # Create 10 notifications
        for i in range(10):
            notification = Notification(
                schemaVersion="1.0.0",
                sender=Sender(id="user1", name="User 1", role="dev"),
                context=Context(theme="info", priority="medium"),
                information=Information(title=f"Notification {i}", body="Test"),
                metadata=Metadata(
                    id=f"notif{i}",
                    timestamp=datetime.now(),
                    channel="test-channel",
                    sequence=i,
                ),
            )
            await sqlite_storage.save_notification(notification)

        # Get first page
        page1 = await sqlite_storage.get_notifications("test-channel", limit=5, offset=0)
        assert len(page1) == 5

        # Get second page
        page2 = await sqlite_storage.get_notifications("test-channel", limit=5, offset=5)
        assert len(page2) == 5

        # Verify no overlap
        page1_ids = {n.metadata.id for n in page1}
        page2_ids = {n.metadata.id for n in page2}
        assert len(page1_ids & page2_ids) == 0
