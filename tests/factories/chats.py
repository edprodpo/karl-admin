import factory
from factory.django import DjangoModelFactory

from core.apps.chats.models.chats import (
    Chat as ChatModel,
    TypeChat,
)


class ChatModelFactory(DjangoModelFactory):
    chat_id = factory.Faker('random_int')
    title = factory.Faker('text')
    type_chat = TypeChat.GROUP
    is_active = True

    class Meta:
        model = ChatModel
