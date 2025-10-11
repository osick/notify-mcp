"""Notification models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Sender(BaseModel):
    """Notification sender information."""

    id: str
    name: str
    role: Literal["dev", "consulting", "business", "other"]
    aiTool: Literal["claude", "chatgpt", "gemini", "other"] | None = None
    email: str | None = None


class Context(BaseModel):
    """Notification context metadata."""

    theme: Literal[
        "architecture-decision",
        "state-update",
        "memory-sync",
        "question",
        "decision",
        "alert",
        "info",
        "discussion",
    ]
    priority: Literal["low", "medium", "high", "critical"] = "medium"
    validity: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    relatedConversationId: str | None = None
    projectId: str | None = None


class Attachment(BaseModel):
    """Notification attachment."""

    type: str
    url: str
    name: str | None = None


class Information(BaseModel):
    """Notification content."""

    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    format: Literal["text", "markdown", "json", "html"] = "text"
    attachments: list[Attachment] = Field(default_factory=list)


class Action(BaseModel):
    """Suggested action for recipients."""

    type: Literal["acknowledge", "respond", "review", "approve", "reject", "custom"]
    label: str
    url: str | None = None
    data: dict | None = None


class Visibility(BaseModel):
    """Access control settings."""

    teams: list[Literal["dev", "consulting", "business", "all"]] = Field(
        default_factory=lambda: ["all"]
    )
    private: bool = False
    allowedUsers: list[str] = Field(default_factory=list)


class Metadata(BaseModel):
    """System-generated metadata."""

    id: str
    timestamp: datetime
    version: str | None = None
    channel: str | None = None
    replyTo: str | None = None
    sequence: int | None = None


class Notification(BaseModel):
    """Complete notification model."""

    schemaVersion: str = "1.0.0"
    sender: Sender
    context: Context
    information: Information
    metadata: Metadata
    actions: list[Action] = Field(default_factory=list)
    visibility: Visibility = Field(default_factory=Visibility)
