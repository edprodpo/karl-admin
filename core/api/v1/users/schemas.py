from datetime import datetime

from ninja import (
    Field,
    Schema,
)

from core.apps.users.entities.users import User


class UserInSchema(Schema):
    vk_id: int | None = Field(default=None)
    email: str | None = Field(default=None)
    name: str | None = Field(default=None)
    thread_id: str | None = Field(default=None)

    def to_entity(self) -> User:
        return User(
            vk_id=self.vk_id,
            email=self.email,
            name=self.name,
            thread_id=self.thread_id,
        )


class UserOutSchema(Schema):
    id: int | None # noqa
    vk_id: int | None
    email: str | None
    name: str | None
    thread_id: str | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: User) -> 'UserOutSchema':
        return UserOutSchema(
            id=entity.id,
            vk_id=entity.vk_id,
            email=entity.email,
            name=entity.name,
            thread_id=entity.thread_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class UserUpdateSchema(Schema):
    email: str | None = None
    name: str | None = None
    thread_id: str | None = None
