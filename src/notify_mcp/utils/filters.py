"""Filter matching utilities."""

from ..models import Notification, SubscriptionFilter


def matches_filter(notification: Notification, filter: SubscriptionFilter) -> bool:
    """Check if notification matches subscription filter.

    Args:
        notification: Notification to check
        filter: Subscription filter criteria

    Returns:
        True if notification matches all filter criteria
    """
    # Priority filter
    if filter.priority and notification.context.priority not in filter.priority:
        return False

    # Tags filter (any tag match)
    if filter.tags:
        notification_tags = set(notification.context.tags)
        filter_tags = set(filter.tags)
        if not notification_tags.intersection(filter_tags):
            return False

    # Themes filter
    if filter.themes and notification.context.theme not in filter.themes:
        return False

    # Roles filter (sender role)
    if filter.roles and notification.sender.role not in filter.roles:
        return False

    # Senders filter (sender ID)
    if filter.senders and notification.sender.id not in filter.senders:
        return False

    return True
