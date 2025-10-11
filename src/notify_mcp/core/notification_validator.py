"""Notification validator using JSON Schema."""

import json
import uuid
from datetime import datetime
from pathlib import Path

from jsonschema import validate

from ..models import Notification


class NotificationValidator:
    """Validates notifications against JSON Schema."""

    def __init__(self):
        """Initialize validator with schema."""
        # Load JSON Schema
        schema_path = Path(__file__).parent.parent.parent.parent / "schemas" / "notification-schema.json"
        with open(schema_path) as f:
            self.schema = json.load(f)

    def validate(self, notification_data: dict) -> None:
        """Validate notification data against schema.

        Args:
            notification_data: Notification as dictionary

        Raises:
            ValidationError: If notification doesn't match schema
        """
        validate(instance=notification_data, schema=self.schema)

    def enrich_notification(
        self, notification: Notification, channel: str, sequence: int
    ) -> Notification:
        """Enrich notification with system metadata.

        Args:
            notification: Notification to enrich
            channel: Target channel
            sequence: Sequence number

        Returns:
            Enriched notification
        """
        # Generate ID if not present
        if not notification.metadata.id:
            notification.metadata.id = f"notif-{uuid.uuid4().hex[:12]}"

        # Set timestamp if not present
        if not notification.metadata.timestamp:
            notification.metadata.timestamp = datetime.now()

        # Set channel and sequence
        notification.metadata.channel = channel
        notification.metadata.sequence = sequence

        return notification

    def validate_and_enrich(
        self, notification: Notification, channel: str, sequence: int
    ) -> Notification:
        """Validate and enrich notification.

        Args:
            notification: Notification to validate and enrich
            channel: Target channel
            sequence: Sequence number

        Returns:
            Validated and enriched notification

        Raises:
            ValidationError: If validation fails
        """
        # Convert to dict for JSON Schema validation
        notification_dict = notification.model_dump(mode="json")

        # Validate against schema
        self.validate(notification_dict)

        # Enrich with metadata
        enriched = self.enrich_notification(notification, channel, sequence)

        return enriched
