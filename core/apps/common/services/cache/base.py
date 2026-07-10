from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseCacheService(ABC):
    @abstractmethod
    def set_cache(
        self,
        key: str,
        value: Any,
        timeout: int | None = None,
    ) -> None:
        ...

    @abstractmethod
    def get_cache(self, key: str) -> Any:
        ...
