from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.chats.entities.chats import Chat
from core.apps.common.entities import BaseEntity
from core.apps.common.enums import EntityStatus
from core.apps.users.models.users import User


@dataclass
class MessageStat:
    month: str
    total_messages: int
    unique_users: int

    @classmethod
    def from_qs(
        cls,
        month: datetime,
        total_messages: int,
        unique_users: int,
    ) -> 'MessageStat':
        month_str = month.strftime('%Y-%m')
        return cls(
            month=month_str,
            total_messages=total_messages,
            unique_users=unique_users,
        )


@dataclass
class Message(BaseEntity):
    id: int | None = field( # noqa
        default=None,
        kw_only=True,
    )
    user: User | EntityStatus | None = field(
        default=EntityStatus.NOT_LOADED,
        kw_only=True,
    )
    chat: Chat | EntityStatus | None = field(
        default=EntityStatus.NOT_LOADED,
        kw_only=True,
    )
    request: str | None = field(
        default=None,
        kw_only=True,
    )
    response: str | None = field(
        default=None,
        kw_only=True,
    )
