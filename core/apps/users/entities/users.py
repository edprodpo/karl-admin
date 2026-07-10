from dataclasses import (
    dataclass,
    field,
)

from core.apps.common.entities import BaseEntity


@dataclass
class User(BaseEntity):
    id: int | None = field( # noqa
        default=None,
        kw_only=True,
    )
    vk_id: int | None = field(
        default=None,
        kw_only=True,
    )
    email: str | None = field(
        default=None,
        kw_only=True,
    )
    name: str | None = field(
        default=None,
        kw_only=True,
    )
    thread_id: str | None = field(
        default=None,
        kw_only=True,
    )

    @classmethod
    def from_dict(cls, user: dict) -> 'User':
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in user.items() if k in valid_keys}
        return cls(**filtered_data)
