"""SQLAlchemy ORM models for persistent storage.

These models map Pydantic domain models to database tables,
storing nested objects as JSON columns.
"""


from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

# Create declarative base
Base = declarative_base()


class ChannelModel(Base):
    """SQLAlchemy model for channels table.

    Maps to: notify_mcp.models.channel.Channel
    """

    __tablename__ = "channels"

    # Primary key
    id = Column(String(255), primary_key=True)

    # Core fields
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(String(255), nullable=False)

    # JSON columns (nested Pydantic models)
    permissions = Column(JSON, nullable=True)  # ChannelPermissions
    channel_metadata = Column("metadata", JSON, nullable=True)  # dict

    # Cached counts
    subscriber_count = Column(Integer, default=0, nullable=False)
    notification_count = Column(Integer, default=0, nullable=False)

    # Last activity
    last_notification_at = Column(DateTime, nullable=True)

    # Relationships (for cascade delete)
    subscriptions = relationship(
        "SubscriptionModel",
        back_populates="channel_rel",
        cascade="all, delete-orphan",
    )
    notifications = relationship(
        "NotificationModel",
        back_populates="channel_rel",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<ChannelModel(id='{self.id}', name='{self.name}')>"


class SubscriptionModel(Base):
    """SQLAlchemy model for subscriptions table.

    Maps to: notify_mcp.models.subscription.Subscription
    """

    __tablename__ = "subscriptions"

    # Primary key
    id = Column(String(255), primary_key=True)

    # Core fields
    client_id = Column(String(255), nullable=False)
    channel = Column(
        String(255),
        ForeignKey("channels.id", ondelete="CASCADE"),
        nullable=False,
    )
    subscribed_at = Column(DateTime, nullable=False)

    # JSON columns (nested Pydantic models)
    filters = Column(JSON, nullable=True)  # SubscriptionFilter

    # Relationship
    channel_rel = relationship("ChannelModel", back_populates="subscriptions")

    def __repr__(self) -> str:
        return f"<SubscriptionModel(id='{self.id}', client_id='{self.client_id}', channel='{self.channel}')>"


# Indexes for subscriptions
Index("ix_subscriptions_channel", SubscriptionModel.channel)
Index("ix_subscriptions_client_id", SubscriptionModel.client_id)
Index("ix_subscriptions_channel_client", SubscriptionModel.channel, SubscriptionModel.client_id)


class NotificationModel(Base):
    """SQLAlchemy model for notifications table.

    Maps to: notify_mcp.models.notification.Notification
    """

    __tablename__ = "notifications"

    # Primary key
    id = Column(String(255), primary_key=True)

    # Core fields
    channel = Column(
        String(255),
        ForeignKey("channels.id", ondelete="CASCADE"),
        nullable=False,
    )
    sequence = Column(Integer, nullable=False)
    priority = Column(String(20), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # Schema version
    schema_version = Column(String(20), nullable=False, default="1.0.0")

    # JSON columns (nested Pydantic models)
    sender_data = Column(JSON, nullable=False)  # Sender
    context_data = Column(JSON, nullable=False)  # Context
    information = Column(JSON, nullable=False)  # Information
    actions = Column(JSON, nullable=True)  # list[Action]
    visibility = Column(JSON, nullable=False)  # Visibility
    metadata_data = Column(JSON, nullable=False)  # Metadata

    # Relationship
    channel_rel = relationship("ChannelModel", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<NotificationModel(id='{self.id}', channel='{self.channel}', sequence={self.sequence})>"


# Indexes for notifications
Index("ix_notifications_channel", NotificationModel.channel)
Index("ix_notifications_channel_timestamp", NotificationModel.channel, NotificationModel.timestamp.desc())
Index("ix_notifications_channel_sequence", NotificationModel.channel, NotificationModel.sequence)
