from dataclasses import dataclass

from core.apps.common.exceptions.base import ApplicationException


@dataclass(eq=False)
class ServiceException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Сервисная ошибка.'
