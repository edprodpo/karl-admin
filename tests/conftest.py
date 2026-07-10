import pytest
from faker import Faker
from punq import Container
from tests.fixtures import init_dummy_container

from core.apps.chats.services.chats import BaseChatService
from core.apps.chats.services.messages import BaseMessageService
from core.apps.users.services.users import BaseUserService


@pytest.fixture()
def faker() -> Faker:
    return Faker()


@pytest.fixture(scope='function')
def container() -> Container:
    return init_dummy_container()


@pytest.fixture()
def user_service(container: Container) -> BaseUserService:
    return container.resolve(BaseUserService)


@pytest.fixture()
def chat_service(container: Container) -> BaseChatService:
    return container.resolve(BaseChatService)


@pytest.fixture()
def message_service(container: Container) -> BaseMessageService:
    return container.resolve(BaseMessageService)
