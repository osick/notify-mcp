"""Channel models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChannelPermissions(BaseModel):
    """Channel access control permissions."""

    subscribe: list[Literal["dev", "consulting", "business", "viewer", "all"]] = Field(
        default_factory=lambda: ["all"]
    )
    publish: list[Literal["dev", "consulting", "business", "admin"]] = Field(
        default_factory=lambda: ["dev", "consulting", "business"]
    )
    admin: list[Literal["dev", "admin"]] = Field(default_factory=lambda: ["dev"])


class Channel(BaseModel):
    """Notification channel model."""

    id: str
    name: str
    description: str | None = None
    createdAt: datetime
    createdBy: str
    permissions: ChannelPermissions = Field(default_factory=ChannelPermissions)
    metadata: dict = Field(default_factory=dict)
    subscriberCount: int = 0
    notificationCount: int = 0
    lastNotificationAt: datetime | None = None
