from datetime import datetime

from ninja import (
    Field,
    Schema,
)

from core.apps.chats.entities.messages import Message


class MessageInSchema(Schema):
    vk_id: int
    request: str | None = Field(default=None)
    response: str | None = Field(default=None)

    def to_entity(self) -> Message:
        return Message(
            request=self.request,
            response=self.response,
        )


class MessageOutSchema(Schema):
    id: int | None # noqa
    request: str | None
    response: str | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: Message) -> 'MessageOutSchema':
        return MessageOutSchema(
            id=entity.id,
            request=entity.request,
            response=entity.response,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
