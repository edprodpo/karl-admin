from dataclasses import dataclass
from typing import Any

from core.apps.common.services.cache.base import BaseCacheService


@dataclass
class FakeCacheService(BaseCacheService):
    def set_cache(self, key: str, value: Any, timeout: int | None = None) -> None:
        ...

    def get_cache(self, key: str) -> Any:
        ...
