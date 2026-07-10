from dataclasses import dataclass

from core.apps.common.exceptions.service import ServiceException


@dataclass(eq=False)
class ChatExistException(ServiceException):
    chat_id: int

    @property
    def message(self) -> str:
        return f'Чат с таким ID {self.chat_id} уже существует.'


@dataclass(eq=False)
class ChatNotFoundException(ServiceException):
    chat_id: int

    @property
    def message(self) -> str:
        return f'Чат с ID {self.chat_id} не найден.'
