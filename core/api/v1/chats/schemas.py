from datetime import datetime

from ninja import (
    Field,
    Schema,
)

from core.apps.chats.entities.chats import (
    Chat,
    TypeChat,
)
from core.apps.chats.exceptions.messages import TypeChatException


class ChatInSchema(Schema):
    chat_id: int
    title: str | None = Field(default=None)
    type_chat: str = Field(default='GROUP', examples=['GROUP', 'PRIVATE'])
    is_active: bool = Field(default=False)

    def to_entity(self) -> Chat:
        try:
            type_chat_enum = TypeChat(self.type_chat)
        except ValueError:
            raise TypeChatException(type_chat=self.type_chat)

        return Chat(
            chat_id=self.chat_id,
            title=self.title,
            type_chat=type_chat_enum,
            is_active=self.is_active,
        )


class ChatOutSchema(Schema):
    id: int | None # noqa
    chat_id: int
    title: str | None
    type_chat: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: Chat) -> 'ChatOutSchema':
        return ChatOutSchema(
            id=entity.id,
            chat_id=entity.chat_id,
            title=entity.title,
            type_chat=entity.type_chat.value,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
