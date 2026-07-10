from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class BaseEntity(ABC):
    created_at: datetime = field(
        default_factory=lambda: datetime.now(tz=ZoneInfo('Europe/Moscow')),
        kw_only=True,
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(tz=ZoneInfo('Europe/Moscow')),
        kw_only=True,
    )
