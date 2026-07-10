import factory
from factory.django import DjangoModelFactory
from tests.factories.chats import ChatModelFactory
from tests.factories.users import UserModelFactory

from core.apps.chats.models.messages import Message as MessageModel


class MessageModelFactory(DjangoModelFactory):
    request = factory.Faker('sentence')
    response = factory.Faker('sentence')
    created_at = factory.Faker('date_time')
    user = factory.SubFactory(UserModelFactory)
    chat = factory.SubFactory(ChatModelFactory)

    class Meta:
        model = MessageModel
