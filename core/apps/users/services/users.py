from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db import IntegrityError

from core.apps.common.services.cache.base import BaseCacheService
from core.apps.users.entities.users import User as UserEntity
from core.apps.users.exceptions.users import (
    UserExistException,
    UserNotFoundByVKIDException,
)
from core.apps.users.models.users import User as UserModel


@dataclass
class BaseUserService(ABC):
    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def get_by_vk_id(self, vk_id: int) -> UserEntity:
        ...

    @abstractmethod
    def update_by_vk_id(self, vk_id: int, data: dict) -> UserEntity:
        ...


@dataclass
class ORMUserService(BaseUserService):
    cache_service: BaseCacheService
    CACHE_TIMEOUT: int = 60 * 10

    def _cache_key(self, vk_id: int) -> str:
        return f'user:vk_id:{vk_id}'

    def create(self, user: UserEntity) -> UserEntity:
        try:
            user_dto = UserModel.from_entity(user=user)
            user_dto.save()

            self.cache_service.set_cache(
                key=self._cache_key(user.vk_id),
                value=user_dto.to_dict(),
                timeout=self.CACHE_TIMEOUT,
            )

            return user_dto.to_entity()

        except IntegrityError:
            raise UserExistException(vk_id=user.vk_id)

    def get_by_vk_id(self, vk_id: int) -> UserEntity:
        cache_key = self._cache_key(vk_id)
        cached_user = self.cache_service.get_cache(key=cache_key)

        if cached_user:
            return UserEntity.from_dict(cached_user)

        try:
            user_dto = UserModel.objects.get(vk_id=vk_id)

            self.cache_service.set_cache(
                key=self._cache_key(vk_id),
                value=user_dto.to_dict(),
                timeout=self.CACHE_TIMEOUT,
            )

            return user_dto

        except UserModel.DoesNotExist:
            raise UserNotFoundByVKIDException(vk_id=vk_id)

    def update_by_vk_id(self, vk_id: int, data: dict) -> UserEntity:
        allowed_fields = {'name', 'email', 'thread_id'}
        cache_key = self._cache_key(vk_id)
        cached_user = self.cache_service.get_cache(cache_key)

        try:
            if cached_user:
                user_dto = UserModel.from_dict(cached_user)
            else:
                user_dto = UserModel.objects.get(vk_id=vk_id)

            update_fields = []
            for field in allowed_fields:
                if field in data and data[field] is not None:
                    setattr(user_dto, field, data[field])
                    update_fields.append(field)

            if update_fields:
                user_dto.save(update_fields=update_fields)
                self.cache_service.set_cache(
                    key=self._cache_key(vk_id),
                    value=user_dto.to_dict(),
                    timeout=self.CACHE_TIMEOUT,
                )

            return user_dto.to_entity()

        except UserModel.DoesNotExist:
            raise UserNotFoundByVKIDException(vk_id=vk_id)
