from dataclasses import dataclass

from core.apps.common.exceptions.service import ServiceException


@dataclass(eq=False)
class TypeChatException(ServiceException):
    type_chat: str

    @property
    def message(self) -> str:
        return f'Неверный тип чата: "{self.type_chat}". Допустимые: "GROUP", "PRIVATE".'
