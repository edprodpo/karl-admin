import enum
from dataclasses import (
    dataclass,
    field,
)

from core.apps.common.entities import BaseEntity


class TypeChat(enum.Enum):
    GROUP = 'GROUP'
    PRIVATE = 'PRIVATE'


@dataclass
class Chat(BaseEntity):
    id: int | None = field( # noqa
        default=None,
        kw_only=True,
    )
    chat_id: int
    title: str | None = field(
        default=None,
        kw_only=True,
    )
    is_active: bool = field(
        default=False,
        kw_only=True,
    )
    type_chat: TypeChat

    @classmethod
    def from_dict(cls, data: dict) -> 'Chat':
        type_chat_value = data.get('type_chat')
        type_chat_enum = TypeChat(type_chat_value) if type_chat_value else TypeChat.GROUP

        return cls(
            id=data.get('id'),
            chat_id=data['chat_id'],
            title=data.get('title'),
            is_active=data.get('is_active', False),
            type_chat=type_chat_enum,
        )
