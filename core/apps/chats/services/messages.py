from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db.models import Count
from django.db.models.functions import TruncMonth

from core.apps.chats.entities.chats import (
    Chat as ChatEntity,
    TypeChat,
)
from core.apps.chats.entities.messages import (
    Message as MessageEntity,
    MessageStat,
)
from core.apps.chats.models.messages import Message as MessageModel
from core.apps.users.entities.users import User as UserEntity


@dataclass
class BaseMessageService(ABC):
    @abstractmethod
    def create(
        self,
        message: MessageEntity,
        user: UserEntity,
        chat: ChatEntity,
    ) -> MessageEntity:
        ...

    @abstractmethod
    def get_message_stat(
        self,
        type_chat: TypeChat = TypeChat.GROUP,
    ) -> list[MessageStat]:
        ...


@dataclass
class ORMMessageService(BaseMessageService):
    def create(
        self,
        message: MessageEntity,
        user: UserEntity,
        chat: ChatEntity,
    ) -> MessageEntity:
        message_dto = MessageModel.from_entity(
            message=message,
            user=user,
            chat=chat,
        )
        message_dto.save()

        return message_dto.to_entity()

    def get_message_stat(
        self,
        type_chat: TypeChat = TypeChat.GROUP,
    ) -> list[MessageStat]:
        qs = (
            MessageModel.objects
            .filter(chat__type_chat=type_chat.value)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(
                total_messages=Count('id'),
                unique_users=Count('user', distinct=True),
            )
            .order_by('-month')
        )

        result: list[MessageStat] = [
            MessageStat.from_qs(
                month=row['month'],
                total_messages=row['total_messages'],
                unique_users=row['unique_users'],
            ) for row in qs
        ]

        return result
