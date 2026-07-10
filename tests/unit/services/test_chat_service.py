import pytest
from faker import Faker
from tests.factories.chats import ChatModelFactory

from core.apps.chats.entities.chats import Chat as ChatEntity
from core.apps.chats.exceptions.chats import (
    ChatExistException,
    ChatNotFoundException,
)
from core.apps.chats.models.chats import Chat as ChatModel
from core.apps.chats.services.chats import BaseChatService


@pytest.mark.django_db
def test_chat_service_create(
    chat_service: BaseChatService,
):
    chat_dto: ChatModel = ChatModelFactory.build()

    created_chat: ChatEntity = chat_service.create(chat=chat_dto.to_entity())

    assert created_chat.chat_id == chat_dto.chat_id, f'{created_chat=}'
    assert created_chat.title == chat_dto.title, f'{created_chat=}'


@pytest.mark.django_db
def test_chat_service_create_exist_exception(
    chat_service: BaseChatService,
):
    chat_dto: ChatModel = ChatModelFactory.create()

    with pytest.raises(ChatExistException):
        chat_service.create(chat=chat_dto.to_entity())


@pytest.mark.django_db
def test_chat_service_get_by_chat_id(
    chat_service: BaseChatService,
):
    chat_dto: ChatModel = ChatModelFactory.create()

    fetched_chat: ChatEntity = chat_service.get_by_chat_id(chat_id=chat_dto.chat_id)

    assert fetched_chat.chat_id == chat_dto.chat_id, f'{fetched_chat=}'
    assert fetched_chat.title == chat_dto.title, f'{fetched_chat=}'


@pytest.mark.django_db
def test_chat_service_get_by_chat_id_not_found_exception(
    chat_service: BaseChatService,
    faker: Faker,
):
    with pytest.raises(ChatNotFoundException):
        chat_service.get_by_chat_id(chat_id=faker.random_int())
