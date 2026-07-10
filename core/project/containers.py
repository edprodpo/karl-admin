from functools import lru_cache

from punq import (
    Container,
    Scope,
)

from core.apps.chats.services.chats import (
    BaseChatService,
    ORMChatService,
)
from core.apps.chats.services.messages import (
    BaseMessageService,
    ORMMessageService,
)
from core.apps.chats.use_cases.messages.create import CreateMessageUseCase
from core.apps.common.services.cache.base import BaseCacheService
from core.apps.common.services.cache.django_cache import DjangoCacheService
from core.apps.users.services.users import (
    BaseUserService,
    ORMUserService,
)


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # services
    container.register(
        service=BaseCacheService,
        factory=DjangoCacheService,
        scope=Scope.singleton,
    )
    container.register(
        service=BaseUserService,
        factory=ORMUserService,
        scope=Scope.singleton,
    )
    container.register(
        service=BaseChatService,
        factory=ORMChatService,
        scope=Scope.singleton,
    )
    container.register(
        service=BaseMessageService,
        factory=ORMMessageService,
        scope=Scope.singleton,
    )

    # use cases
    container.register(CreateMessageUseCase)

    return container
