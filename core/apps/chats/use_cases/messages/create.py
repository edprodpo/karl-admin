from dataclasses import dataclass

from core.apps.chats.entities.chats import Chat as ChatEntity
from core.apps.chats.entities.messages import Message as MessageEntity
from core.apps.chats.services.chats import BaseChatService
from core.apps.chats.services.messages import BaseMessageService
from core.apps.users.entities.users import User as UserEntity
from core.apps.users.services.users import BaseUserService


@dataclass
class CreateMessageUseCase:
    message_service: BaseMessageService
    user_service: BaseUserService
    chat_service: BaseChatService

    def execute(
        self,
        message: MessageEntity,
        vk_id: int,
        chat_id: int,
    ) -> MessageEntity:
        user: UserEntity = self.user_service.get_by_vk_id(vk_id=vk_id)
        chat: ChatEntity = self.chat_service.get_by_chat_id(chat_id=chat_id)

        message: MessageEntity = self.message_service.create(
            message=message,
            user=user,
            chat=chat,
        )

        return message
