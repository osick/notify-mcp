"""Tests for notification filtering logic."""

import pytest
from datetime import datetime

from notify_mcp.utils.filters import matches_filter
from notify_mcp.models import (
    Notification,
    Sender,
    Context,
    Information,
    Metadata,
    SubscriptionFilter,
)


def create_notification(
    priority: str = "medium",
    tags: list[str] = None,
    theme: str = "info",
    role: str = "dev",
) -> Notification:
    """Helper to create a test notification."""
    return Notification(
        schema_version="1.0.0",
        sender=Sender(id="user", name="User", role=role),
        context=Context(theme=theme, priority=priority, tags=tags or []),
        information=Information(title="Test", body="Test body", format="text"),
        metadata=Metadata(id="test", timestamp=datetime.now()),
    )


class TestFilters:
    """Test notification filtering logic."""

    def test_no_filter_matches_all(self):
        """Test that empty filter matches all notifications."""
        notification = create_notification()
        filter = SubscriptionFilter()

        assert matches_filter(notification, filter) is True

    def test_priority_filter_match(self):
        """Test priority filter matching."""
        notification = create_notification(priority="high")
        filter = SubscriptionFilter(priority=["high", "critical"])

        assert matches_filter(notification, filter) is True

    def test_priority_filter_no_match(self):
        """Test priority filter not matching."""
        notification = create_notification(priority="low")
        filter = SubscriptionFilter(priority=["high", "critical"])

        assert matches_filter(notification, filter) is False

    def test_tag_filter_match(self):
        """Test tag filter with intersection."""
        notification = create_notification(tags=["backend", "api", "python"])
        filter = SubscriptionFilter(tags=["backend", "database"])

        # Should match because "backend" is in both
        assert matches_filter(notification, filter) is True

    def test_tag_filter_no_match(self):
        """Test tag filter with no intersection."""
        notification = create_notification(tags=["frontend", "ui"])
        filter = SubscriptionFilter(tags=["backend", "database"])

        assert matches_filter(notification, filter) is False

    def test_tag_filter_empty_notification_tags(self):
        """Test tag filter when notification has no tags."""
        notification = create_notification(tags=[])
        filter = SubscriptionFilter(tags=["backend"])

        assert matches_filter(notification, filter) is False

    def test_theme_filter_match(self):
        """Test theme filter matching."""
        notification = create_notification(theme="architecture-decision")
        filter = SubscriptionFilter(themes=["architecture-decision", "state-update"])

        assert matches_filter(notification, filter) is True

    def test_theme_filter_no_match(self):
        """Test theme filter not matching."""
        notification = create_notification(theme="info")
        filter = SubscriptionFilter(themes=["architecture-decision", "alert"])

        assert matches_filter(notification, filter) is False

    def test_role_filter_match(self):
        """Test role filter matching."""
        notification = create_notification(role="dev")
        filter = SubscriptionFilter(roles=["dev", "consulting"])

        assert matches_filter(notification, filter) is True

    def test_role_filter_no_match(self):
        """Test role filter not matching."""
        notification = create_notification(role="business")
        filter = SubscriptionFilter(roles=["dev", "consulting"])

        assert matches_filter(notification, filter) is False

    def test_multiple_filters_all_match(self):
        """Test multiple filters when all match."""
        notification = create_notification(
            priority="high",
            tags=["backend", "api"],
            theme="alert",
            role="dev",
        )
        filter = SubscriptionFilter(
            priority=["high", "critical"],
            tags=["backend"],
            themes=["alert", "architecture-decision"],
            roles=["dev", "consulting"],
        )

        assert matches_filter(notification, filter) is True

    def test_multiple_filters_one_fails(self):
        """Test multiple filters when one doesn't match."""
        notification = create_notification(
            priority="low",  # Doesn't match filter
            tags=["backend"],
            theme="alert",
            role="dev",
        )
        filter = SubscriptionFilter(
            priority=["high", "critical"],  # Won't match
            tags=["backend"],
            themes=["alert"],
            roles=["dev"],
        )

        assert matches_filter(notification, filter) is False

    def test_sender_filter_match(self):
        """Test sender ID filter matching."""
        notification = create_notification()
        notification.sender.id = "alice"
        filter = SubscriptionFilter(senders=["alice", "bob"])

        assert matches_filter(notification, filter) is True

    def test_sender_filter_no_match(self):
        """Test sender ID filter not matching."""
        notification = create_notification()
        notification.sender.id = "charlie"
        filter = SubscriptionFilter(senders=["alice", "bob"])

        assert matches_filter(notification, filter) is False

    def test_empty_filter_list_matches_all(self):
        """Test that empty filter lists match all (treated as no filter)."""
        notification = create_notification(priority="high")
        filter = SubscriptionFilter(priority=[])

        # Empty priority list is falsy in Python, treated as "no filter"
        assert matches_filter(notification, filter) is True
