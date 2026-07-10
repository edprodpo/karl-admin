import logging

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

import orjson
from punq import Container

from core.api.schemas import ApiResponse
from core.api.v1.auth import SecretKeyAuth
from core.api.v1.messages.schemas import (
    MessageInSchema,
    MessageOutSchema,
)
from core.apps.chats.entities.messages import Message
from core.apps.chats.exceptions.chats import ChatNotFoundException
from core.apps.chats.exceptions.messages import TypeChatException
from core.apps.chats.use_cases.messages.create import CreateMessageUseCase
from core.apps.users.exceptions.users import UserNotFoundByVKIDException
from core.project.containers import get_container


router = Router(
    tags=['Сообщения'],
    auth=SecretKeyAuth(),
)
logger = logging.getLogger('django.request')


@router.post('{chat_id}/messages/', response=ApiResponse[MessageOutSchema])
def create_message_handler(
    request: HttpRequest,
    chat_id: int,
    schema: MessageInSchema,
) -> ApiResponse[MessageOutSchema]:
    container: Container = get_container()
    use_case: CreateMessageUseCase = container.resolve(CreateMessageUseCase)

    try:
        message: Message = use_case.execute(
            message=schema.to_entity(),
            vk_id=schema.vk_id,
            chat_id=chat_id,
        )

        return ApiResponse(data=MessageOutSchema.from_entity(entity=message))

    except UserNotFoundByVKIDException as error:
        logger.error(
            msg='Пользователь не найден.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=404,
            message=error.message,
        )

    except ChatNotFoundException as error:
        logger.error(
            msg='Чат не найден.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=404,
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
