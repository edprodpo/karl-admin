from dataclasses import dataclass

from core.apps.common.exceptions.service import ServiceException


@dataclass(eq=False)
class UserExistException(ServiceException):
    vk_id: int

    @property
    def message(self) -> str:
        return f'Пользователь с таким VK ID {self.vk_id} уже существует.'


@dataclass(eq=False)
class UserNotFoundByVKIDException(ServiceException):
    vk_id: int

    @property
    def message(self) -> str:
        return f'Пользователь с VK ID {self.vk_id} не найден.'
