from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db import IntegrityError

from core.apps.chats.entities.chats import Chat as ChatEntity
from core.apps.chats.exceptions.chats import (
    ChatExistException,
    ChatNotFoundException,
)
from core.apps.chats.models.chats import Chat as ChatModel
from core.apps.common.services.cache.base import BaseCacheService


@dataclass
class BaseChatService(ABC):
    @abstractmethod
    def create(self, chat: ChatEntity) -> ChatEntity:
        ...

    @abstractmethod
    def get_by_chat_id(self, chat_id: int) -> ChatEntity:
        ...


@dataclass
class ORMChatService(BaseChatService):
    cache_service: BaseCacheService
    CACHE_TIMEOUT: int = 60 * 30

    def _cache_key(self, chat_id: int) -> str:
        return f'chat:chat_id:{chat_id}'

    def create(self, chat: ChatEntity) -> ChatEntity:
        try:
            chat_dto = ChatModel.from_entity(chat=chat)
            chat_dto.save()

            self.cache_service.set_cache(
                key=self._cache_key(chat.chat_id),
                value=chat_dto.to_dict(),
                timeout=self.CACHE_TIMEOUT,
            )

            return chat_dto.to_entity()

        except IntegrityError:
            raise ChatExistException(chat_id=chat.chat_id)

    def get_by_chat_id(self, chat_id: int) -> ChatEntity:
        cache_key = self._cache_key(chat_id)
        cached_chat = self.cache_service.get_cache(cache_key)

        if cached_chat:
            return ChatEntity.from_dict(cached_chat)

        try:
            chat_dto = ChatModel.objects.get(chat_id=chat_id)

            self.cache_service.set_cache(
                key=self._cache_key(chat_id),
                value=chat_dto.to_dict(),
                timeout=self.CACHE_TIMEOUT,
            )

            return chat_dto.to_entity()

        except ChatModel.DoesNotExist:
            raise ChatNotFoundException(chat_id=chat_id)
