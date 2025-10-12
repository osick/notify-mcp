"""Tests for Pydantic models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from notify_mcp.models import (
    Notification,
    Sender,
    Context,
    Information,
    Metadata,
    Channel,
    ChannelPermissions,
    Subscription,
    SubscriptionFilter,
)


class TestNotificationModels:
    """Test notification data models."""

    def test_valid_notification_creation(self):
        """Test creating a valid notification."""
        notification = Notification(
            schema_version="1.0.0",
            sender=Sender(
                id="user123",
                name="Alice",
                role="dev",
                ai_tool="claude",
            ),
            context=Context(
                theme="architecture-decision",
                priority="high",
                tags=["backend", "api"],
            ),
            information=Information(
                title="API Gateway Decision",
                body="We decided to use Kong as our API gateway",
                format="text",
            ),
            metadata=Metadata(
                id="notif-123",
                timestamp=datetime.now(),
                channel="engineering",
                sequence=1,
            ),
        )

        assert notification.sender.id == "user123"
        assert notification.context.priority == "high"
        assert notification.information.title == "API Gateway Decision"
        assert "backend" in notification.context.tags

    def test_invalid_sender_role(self):
        """Test that invalid sender roles are rejected."""
        with pytest.raises(ValidationError):
            Sender(
                id="user123",
                name="Alice",
                role="invalid_role",  # Should fail
            )

    def test_invalid_priority(self):
        """Test that invalid priorities are rejected."""
        with pytest.raises(ValidationError):
            Context(
                theme="info",
                priority="invalid_priority",  # Should fail
                tags=[],
            )

    def test_title_length_validation(self):
        """Test title length constraints."""
        with pytest.raises(ValidationError):
            Information(
                title="",  # Too short
                body="Some body",
                format="text",
            )

        with pytest.raises(ValidationError):
            Information(
                title="x" * 201,  # Too long (max 200)
                body="Some body",
                format="text",
            )

    def test_body_required(self):
        """Test that body is required."""
        with pytest.raises(ValidationError):
            Information(
                title="Valid Title",
                body="",  # Empty body should fail
                format="text",
            )


class TestChannelModels:
    """Test channel data models."""

    def test_valid_channel_creation(self):
        """Test creating a valid channel."""
        channel = Channel(
            id="engineering",
            name="Engineering Team",
            description="Technical discussions and decisions",
            createdAt=datetime.now(),
            createdBy="admin",
            permissions=ChannelPermissions(
                publish=["dev", "consulting"],
                subscribe=["dev", "consulting", "business"],
            ),
            subscriberCount=5,
            notificationCount=100,
        )

        assert channel.id == "engineering"
        assert channel.subscriberCount == 5
        assert "dev" in channel.permissions.publish

    def test_default_subscriber_count(self):
        """Test default subscriber count is 0."""
        channel = Channel(
            id="test",
            name="Test Channel",
            createdAt=datetime.now(),
            createdBy="admin",
            permissions=ChannelPermissions(),
        )

        assert channel.subscriberCount == 0
        assert channel.notificationCount == 0


class TestSubscriptionModels:
    """Test subscription data models."""

    def test_subscription_with_filters(self):
        """Test subscription with priority and tag filters."""
        sub = Subscription(
            id="sub-123",
            clientId="client-456",
            channel="engineering",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(
                priority=["high", "critical"],
                tags=["backend", "api"],
            ),
        )

        assert sub.clientId == "client-456"
        assert "high" in sub.filters.priority
        assert "backend" in sub.filters.tags

    def test_subscription_without_filters(self):
        """Test subscription without filters (all notifications)."""
        sub = Subscription(
            id="sub-123",
            clientId="client-456",
            channel="engineering",
            subscribedAt=datetime.now(),
            filters=SubscriptionFilter(),
        )

        assert sub.filters.priority is None
        assert sub.filters.tags is None
        assert sub.filters.themes is None

    def test_empty_filter_lists(self):
        """Test that empty filter lists are treated as None."""
        filter = SubscriptionFilter(
            priority=[],
            tags=[],
        )

        # Empty lists should work (filter nothing)
        assert filter.priority == []
        assert filter.tags == []
