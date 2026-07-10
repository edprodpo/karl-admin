from django.db import models

from core.apps.chats.entities.chats import Chat as ChatEntity
from core.apps.chats.entities.messages import Message as MessageEntity
from core.apps.common.models import TimedBaseModel
from core.apps.users.entities.users import User as UserEntity


class Message(TimedBaseModel):
    request = models.TextField(
        verbose_name='Запрос пользователя',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        to='users.User',
        verbose_name='Пользователь',
        related_name='user_message',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    chat = models.ForeignKey(
        to='chats.Chat',
        verbose_name='Чат',
        related_name='chat_message',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    response = models.TextField(
        verbose_name='Ответ нейрокуратора',
        null=True,
        blank=True,
    )

    @classmethod
    def from_entity(
        cls,
            message: MessageEntity,
            user: UserEntity,
            chat: ChatEntity,
    ) -> 'Message':
        return cls(
            user_id=user.id,
            chat_id=chat.id,
            request=message.request,
            response=message.response,
        )

    def to_entity(self) -> MessageEntity:
        return MessageEntity(
            id=self.pk,
            request=self.request,
            response=self.response,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
