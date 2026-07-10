from django.db import models

from core.apps.chats.entities.chats import Chat as ChatEntity
from core.apps.common.models import TimedBaseModel


class TypeChat(models.TextChoices):
    GROUP = 'GROUP', 'Групповой'
    PRIVATE = 'PRIVATE', 'Приватный'


class Chat(TimedBaseModel):
    chat_id = models.BigIntegerField(
        verbose_name='ID чата',
        unique=True,
        null=False,
        blank=False,
    )
    title = models.CharField(
        verbose_name='Название чата',
        max_length=256,
        null=True,
        blank=True,
    )
    type_chat = models.CharField(
        verbose_name='Тип чата',
        max_length=10,
        choices=TypeChat.choices,
    )
    is_active = models.BooleanField(
        verbose_name='Разрешение',
        null=False,
        default=False,
    )

    def __str__(self) -> str:
        return self.title if self.title else f'Чат {self.chat_id}'

    @classmethod
    def from_entity(cls, chat: ChatEntity) -> 'Chat':
        return cls(
            chat_id=chat.chat_id,
            title=chat.title,
            type_chat=chat.type_chat.value,
            is_active=chat.is_active,
        )

    def to_entity(self) -> ChatEntity:
        return ChatEntity(
            id=self.pk,
            chat_id=self.chat_id,
            title=self.title,
            type_chat=TypeChat(self.type_chat),
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.pk,
            'chat_id': self.chat_id,
            'title': self.title,
            'type_chat': self.type_chat,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
