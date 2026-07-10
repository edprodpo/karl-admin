from punq import (
    Container,
    Scope,
)

from core.apps.common.services.cache.base import BaseCacheService
from core.apps.common.services.cache.memory import FakeCacheService
from core.project.containers import _init_container


def init_dummy_container() -> Container:
    container = _init_container()

    # services
    container.register(
        service=BaseCacheService,
        factory=FakeCacheService,
        scope=Scope.singleton,
    )

    return container
