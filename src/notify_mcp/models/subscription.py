"""Subscription models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SubscriptionFilter(BaseModel):
    """Filter criteria for subscriptions."""

    priority: list[Literal["low", "medium", "high", "critical"]] | None = None
    tags: list[str] | None = None
    themes: list[
        Literal[
            "architecture-decision",
            "state-update",
            "memory-sync",
            "question",
            "decision",
            "alert",
            "info",
            "discussion",
        ]
    ] | None = None
    roles: list[Literal["dev", "consulting", "business", "other"]] | None = None
    senders: list[str] | None = None


class Subscription(BaseModel):
    """Subscription model."""

    id: str
    clientId: str
    channel: str
    subscribedAt: datetime
    filters: SubscriptionFilter = Field(default_factory=SubscriptionFilter)
