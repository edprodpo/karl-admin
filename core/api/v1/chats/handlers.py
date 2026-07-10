import logging

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

import orjson
from punq import Container

from core.api.schemas import ApiResponse
from core.api.v1.auth import SecretKeyAuth
from core.api.v1.chats.schemas import (
    ChatInSchema,
    ChatOutSchema,
)
from core.apps.chats.entities.chats import Chat
from core.apps.chats.exceptions.chats import (
    ChatExistException,
    ChatNotFoundException,
)
from core.apps.chats.exceptions.messages import TypeChatException
from core.apps.chats.services.chats import BaseChatService
from core.project.containers import get_container


router = Router(
    tags=['Чаты'],
    auth=SecretKeyAuth(),
)
logger = logging.getLogger('django.request')


@router.post(path='', response=ApiResponse[ChatOutSchema])
def create_group_chat_handler(
    request: HttpRequest,
    schema: ChatInSchema,
) -> ApiResponse[ChatOutSchema]:
    container: Container = get_container()
    chat_service: BaseChatService = container.resolve(BaseChatService)

    try:
        chat: Chat = chat_service.create(chat=schema.to_entity())

        return ApiResponse(data=ChatOutSchema.from_entity(entity=chat))

    except ChatExistException as error:
        logger.error(
            msg='Чат уже существует.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=400,
            message=error.message,
        )

    except TypeChatException as error:
        logger.error(
            msg='Неправильный тип чата.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=400,
            message=error.message,
        )


@router.get('{chat_id}/', response=ApiResponse[ChatOutSchema])
def get_group_chat_by_chat_id_handler(
    request: HttpRequest,
    chat_id: int,
) -> ApiResponse[ChatOutSchema]:
    container: Container = get_container()
    chat_service: BaseChatService = container.resolve(BaseChatService)

    try:
        chat: Chat = chat_service.get_by_chat_id(chat_id=chat_id)

        return ApiResponse(data=ChatOutSchema.from_entity(entity=chat))

    except ChatNotFoundException as error:
        logger.error(
            msg='Чат не найден.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=404,
            message=error.message,
        )
