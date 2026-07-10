import random

import pytest
from faker import Faker
from tests.factories.chats import ChatModelFactory
from tests.factories.messages import MessageModelFactory
from tests.factories.users import UserModelFactory

from core.apps.chats.entities.messages import (
    Message as MessageEntity,
    MessageStat,
)
from core.apps.chats.models.chats import Chat as ChatModel
from core.apps.chats.models.messages import Message as MessageModel
from core.apps.chats.services.messages import BaseMessageService
from core.apps.users.models.users import User as UserModel


@pytest.mark.django_db
def test_message_service_create(
    message_service: BaseMessageService,
):
    user_dto: UserModel = UserModelFactory.create()
    chat_dto: ChatModel = ChatModelFactory.create()
    message_dto: MessageModel = MessageModelFactory.build(
        user=user_dto,
        chat=chat_dto,
    )

    created_message: MessageEntity = message_service.create(
        message=message_dto.to_entity(),
        user=user_dto.to_entity(),
        chat=chat_dto.to_entity(),
    )

    assert created_message.request == message_dto.request, f'{created_message=}'
    assert created_message.response == message_dto.response, f'{created_message=}'


@pytest.mark.django_db
def test_message_service_create_multiple(
    message_service: BaseMessageService,
):
    expected_count = 5

    user_dto: UserModel = UserModelFactory.create()
    chat_dto: ChatModel = ChatModelFactory.create()
    messages: list[MessageModel] = MessageModelFactory.build_batch(
        size=expected_count,
        user=user_dto,
        chat=chat_dto,
    )

    created_messages: list[MessageEntity] = [
        message_service.create(
            message=message.to_entity(),
            user=user_dto.to_entity(),
            chat=chat_dto.to_entity(),
        ) for message in messages
    ]

    assert len(created_messages) == expected_count, f'{len(created_messages)=}, {expected_count=}'

    for message_dto, created_message in zip(messages, created_messages):
        assert created_message.request == message_dto.request, f'{created_message.request=} != {message_dto.request=}' # noqa
        assert created_message.response == message_dto.response, f'{created_message.response=} != {message_dto.response=}' # noqa


@pytest.mark.django_db
def test_message_service_get_message_stat(
    message_service: BaseMessageService,
    faker: Faker,
):
    user_count = faker.random_int(min=10, max=100)
    message_count = faker.random_int(min=10, max=100)

    users: list[UserModel] = UserModelFactory.create_batch(size=user_count)
    chat_dto: ChatModel = ChatModelFactory.create()
    messages: list[MessageModel] = [
        MessageModelFactory.create(
            user=random.choice(users), # noqa
            chat=chat_dto,
        ) for _ in range(message_count)
    ]

    message_stats: list[MessageStat] = message_service.get_message_stat(chat_dto.type_chat)

    assert all(isinstance(s, MessageStat) for s in message_stats)

    total_messages_count = sum(s.total_messages for s in message_stats)
    assert total_messages_count == len(messages), f"{total_messages_count=} != {len(messages)=}"

    unique_users_count = sum(s.unique_users for s in message_stats)
    assert unique_users_count <= len(users), f"{unique_users_count=} > {len(users)=}"
