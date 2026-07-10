from dataclasses import dataclass
from typing import Any

from django.core.cache import cache

from core.apps.common.services.cache.base import BaseCacheService


@dataclass
class DjangoCacheService(BaseCacheService):
    def set_cache(
        self,
        key: str,
        value: Any,
        timeout: int | None = None,
    ) -> None:
        cache.set(
            key=key,
            value=value,
            timeout=timeout,
        )

    def get_cache(self, key: str) -> Any:
        return cache.get(key=key)
