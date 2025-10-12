"""SQLite storage adapter implementation.

This module provides persistent storage using SQLite with async support.
Implements LRU cache for notification history to limit database size.
"""

import logging
from pathlib import Path

from sqlalchemy import delete, desc, func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..core.storage_adapter import StorageAdapter
from ..models.channel import Channel, ChannelPermissions
from ..models.notification import (
    Action,
    Context,
    Information,
    Metadata,
    Notification,
    Sender,
    Visibility,
)
from ..models.subscription import Subscription, SubscriptionFilter
from .models import Base, ChannelModel, NotificationModel, SubscriptionModel

logger = logging.getLogger(__name__)


class SQLiteStorage(StorageAdapter):
    """SQLite-based persistent storage adapter.

    Features:
    - Async SQLite operations using aiosqlite
    - LRU cache for notifications (configurable max per channel)
    - JSON serialization of nested Pydantic models
    - WAL mode for better concurrency
    """

    def __init__(self, db_path: str, max_history_per_channel: int = 1000):
        """Initialize SQLite storage.

        Args:
            db_path: Path to SQLite database file
            max_history_per_channel: Maximum notifications to keep per channel (LRU)
        """
        self.db_path = Path(db_path).expanduser()
        self.max_history = max_history_per_channel

        # Create async engine with SQLite-specific options
        db_url = f"sqlite+aiosqlite:///{self.db_path}"
        self.engine = create_async_engine(
            db_url,
            echo=False,  # Set to True for SQL debug logging
            future=True,
        )

        # Create session factory
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        logger.info(f"SQLite storage configured: path={self.db_path}")

    async def initialize(self) -> None:
        """Initialize database schema.

        Creates all tables and enables WAL mode for better concurrency.
        """
        async with self.engine.begin() as conn:
            # Enable foreign key constraints (required for cascade deletes)
            await conn.execute(text("PRAGMA foreign_keys=ON"))

            # Create all tables
            await conn.run_sync(Base.metadata.create_all)

            # Enable WAL mode for better concurrency
            await conn.execute(text("PRAGMA journal_mode=WAL"))

        logger.info("Database schema initialized")

    async def close(self) -> None:
        """Close database connections and cleanup resources."""
        await self.engine.dispose()
        logger.info("Database connections closed")

    # ========== Channel Operations ==========

    async def save_channel(self, channel: Channel) -> None:
        """Save or update a channel."""
        async with self.session_factory() as session:
            # Check if channel exists
            stmt = select(ChannelModel).where(ChannelModel.id == channel.id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Update existing
                existing.name = channel.name
                existing.description = channel.description
                existing.created_at = channel.createdAt
                existing.created_by = channel.createdBy
                existing.permissions = channel.permissions.model_dump(mode="json") if channel.permissions else None
                existing.channel_metadata = channel.metadata
                existing.subscriber_count = channel.subscriberCount
                existing.notification_count = channel.notificationCount
                existing.last_notification_at = channel.lastNotificationAt
            else:
                # Create new
                channel_model = ChannelModel(
                    id=channel.id,
                    name=channel.name,
                    description=channel.description,
                    created_at=channel.createdAt,
                    created_by=channel.createdBy,
                    permissions=channel.permissions.model_dump(mode="json") if channel.permissions else None,
                    channel_metadata=channel.metadata,
                    subscriber_count=channel.subscriberCount,
                    notification_count=channel.notificationCount,
                    last_notification_at=channel.lastNotificationAt,
                )
                session.add(channel_model)

            await session.commit()

    async def get_channel(self, channel_id: str) -> Channel | None:
        """Get a channel by ID."""
        async with self.session_factory() as session:
            stmt = select(ChannelModel).where(ChannelModel.id == channel_id)
            result = await session.execute(stmt)
            channel_model = result.scalar_one_or_none()

            if not channel_model:
                return None

            return self._channel_model_to_pydantic(channel_model)

    async def delete_channel(self, channel_id: str) -> None:
        """Delete a channel (cascade deletes subscriptions and notifications)."""
        async with self.session_factory() as session:
            stmt = delete(ChannelModel).where(ChannelModel.id == channel_id)
            await session.execute(stmt)
            await session.commit()

    async def list_channels(self) -> list[Channel]:
        """List all channels."""
        async with self.session_factory() as session:
            stmt = select(ChannelModel)
            result = await session.execute(stmt)
            channel_models = result.scalars().all()

            return [self._channel_model_to_pydantic(cm) for cm in channel_models]

    # ========== Subscription Operations ==========

    async def save_subscription(self, subscription: Subscription) -> None:
        """Save a new subscription."""
        async with self.session_factory() as session:
            sub_model = SubscriptionModel(
                id=subscription.id,
                client_id=subscription.clientId,
                channel=subscription.channel,
                subscribed_at=subscription.subscribedAt,
                filters=subscription.filters.model_dump(mode="json") if subscription.filters else None,
            )
            session.add(sub_model)

            try:
                await session.commit()
            except IntegrityError:
                # Subscription already exists or channel doesn't exist
                await session.rollback()
                raise

    async def delete_subscription(self, subscription_id: str) -> None:
        """Delete a subscription by ID."""
        async with self.session_factory() as session:
            stmt = delete(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
            await session.execute(stmt)
            await session.commit()

    async def get_subscriptions_by_channel(self, channel_id: str) -> list[Subscription]:
        """Get all subscriptions for a channel."""
        async with self.session_factory() as session:
            stmt = select(SubscriptionModel).where(SubscriptionModel.channel == channel_id)
            result = await session.execute(stmt)
            sub_models = result.scalars().all()

            return [self._subscription_model_to_pydantic(sm) for sm in sub_models]

    async def get_subscriptions_by_client(self, client_id: str) -> list[Subscription]:
        """Get all subscriptions for a client."""
        async with self.session_factory() as session:
            stmt = select(SubscriptionModel).where(SubscriptionModel.client_id == client_id)
            result = await session.execute(stmt)
            sub_models = result.scalars().all()

            return [self._subscription_model_to_pydantic(sm) for sm in sub_models]

    # ========== Notification Operations ==========

    async def save_notification(self, notification: Notification) -> None:
        """Save a notification and enforce LRU cache limit."""
        async with self.session_factory() as session:
            # Extract channel from metadata
            channel_id = notification.metadata.channel
            if not channel_id:
                raise ValueError("Notification metadata must include channel")

            # Create notification model
            notif_model = NotificationModel(
                id=notification.metadata.id,
                channel=channel_id,
                sequence=notification.metadata.sequence or 0,
                priority=notification.context.priority,
                timestamp=notification.metadata.timestamp,
                schema_version=notification.schemaVersion,
                sender_data=notification.sender.model_dump(mode="json"),
                context_data=notification.context.model_dump(mode="json"),
                information=notification.information.model_dump(mode="json"),
                actions=[a.model_dump(mode="json") for a in notification.actions] if notification.actions else None,
                visibility=notification.visibility.model_dump(mode="json"),
                metadata_data=notification.metadata.model_dump(mode="json"),
            )
            session.add(notif_model)

            # Commit notification
            await session.commit()

            # Enforce LRU cache limit
            await self._enforce_lru_cache(session, channel_id)

    async def get_notifications(
        self, channel_id: str, limit: int = 50, offset: int = 0
    ) -> list[Notification]:
        """Get notifications for a channel (most recent first)."""
        async with self.session_factory() as session:
            stmt = (
                select(NotificationModel)
                .where(NotificationModel.channel == channel_id)
                .order_by(desc(NotificationModel.timestamp))
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(stmt)
            notif_models = result.scalars().all()

            return [self._notification_model_to_pydantic(nm) for nm in notif_models]

    async def get_notification_count(self, channel_id: str) -> int:
        """Get total notification count for a channel."""
        async with self.session_factory() as session:
            stmt = select(func.count()).select_from(NotificationModel).where(
                NotificationModel.channel == channel_id
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    # ========== Private Helper Methods ==========

    async def _enforce_lru_cache(self, session: AsyncSession, channel_id: str) -> None:
        """Enforce LRU cache limit for notifications.

        Deletes oldest notifications when limit is exceeded.
        """
        # Count notifications for this channel
        count_stmt = select(func.count()).select_from(NotificationModel).where(
            NotificationModel.channel == channel_id
        )
        result = await session.execute(count_stmt)
        count = result.scalar_one()

        if count > self.max_history:
            # Calculate how many to delete
            to_delete = count - self.max_history

            # Get IDs of oldest notifications
            oldest_stmt = (
                select(NotificationModel.id)
                .where(NotificationModel.channel == channel_id)
                .order_by(NotificationModel.timestamp)
                .limit(to_delete)
            )
            result = await session.execute(oldest_stmt)
            old_ids = [row[0] for row in result.all()]

            # Delete them
            if old_ids:
                delete_stmt = delete(NotificationModel).where(NotificationModel.id.in_(old_ids))
                await session.execute(delete_stmt)
                await session.commit()

                logger.info(
                    f"LRU cache: deleted {len(old_ids)} old notifications from channel {channel_id}"
                )

    def _channel_model_to_pydantic(self, model: ChannelModel) -> Channel:
        """Convert SQLAlchemy ChannelModel to Pydantic Channel."""
        return Channel(
            id=model.id,
            name=model.name,
            description=model.description,
            createdAt=model.created_at,
            createdBy=model.created_by,
            permissions=ChannelPermissions(**model.permissions) if model.permissions else ChannelPermissions(),
            metadata=model.channel_metadata or {},
            subscriberCount=model.subscriber_count,
            notificationCount=model.notification_count,
            lastNotificationAt=model.last_notification_at,
        )

    def _subscription_model_to_pydantic(self, model: SubscriptionModel) -> Subscription:
        """Convert SQLAlchemy SubscriptionModel to Pydantic Subscription."""
        return Subscription(
            id=model.id,
            clientId=model.client_id,
            channel=model.channel,
            subscribedAt=model.subscribed_at,
            filters=SubscriptionFilter(**model.filters) if model.filters else SubscriptionFilter(),
        )

    def _notification_model_to_pydantic(self, model: NotificationModel) -> Notification:
        """Convert SQLAlchemy NotificationModel to Pydantic Notification."""
        return Notification(
            schemaVersion=model.schema_version,
            sender=Sender(**model.sender_data),
            context=Context(**model.context_data),
            information=Information(**model.information),
            actions=[Action(**a) for a in model.actions] if model.actions else [],
            visibility=Visibility(**model.visibility),
            metadata=Metadata(**model.metadata_data),
        )
