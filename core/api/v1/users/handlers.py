import logging

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

import orjson
from punq import Container

from core.api.schemas import ApiResponse
from core.api.v1.auth import SecretKeyAuth
from core.api.v1.users.schemas import (
    UserInSchema,
    UserOutSchema,
    UserUpdateSchema,
)
from core.apps.users.entities.users import User
from core.apps.users.exceptions.users import (
    UserExistException,
    UserNotFoundByVKIDException,
)
from core.apps.users.services.users import BaseUserService
from core.project.containers import get_container


router = Router(
    tags=['Пользователи'],
    auth=SecretKeyAuth(),
)
logger = logging.getLogger('django.request')


@router.post(path='', response=ApiResponse[UserOutSchema])
def create_user_handler(
    request: HttpRequest,
    schema: UserInSchema,
) -> ApiResponse[UserOutSchema]:
    container: Container = get_container()
    user_service: BaseUserService = container.resolve(BaseUserService)

    try:
        user: User = user_service.create(user=schema.to_entity())

        return ApiResponse(data=UserOutSchema.from_entity(entity=user))

    except UserExistException as error:
        logger.error(
            msg='Пользователь уже существует.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=400,
            message=error.message,
        )


@router.get('{vk_id}/', response=ApiResponse[UserOutSchema])
def get_user_by_vk_id_handler(
    request: HttpRequest,
    vk_id: int,
) -> ApiResponse[UserOutSchema]:
    container: Container = get_container()
    user_service: BaseUserService = container.resolve(BaseUserService)

    try:
        user: User = user_service.get_by_vk_id(vk_id=vk_id)

        return ApiResponse(data=UserOutSchema.from_entity(entity=user))

    except UserNotFoundByVKIDException as error:
        logger.error(
            msg='Пользователь не найден.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=404,
            message=error.message,
        )


@router.patch('{vk_id}/', response=ApiResponse[UserOutSchema])
def update_user_by_vk_id_handler(
    request: HttpRequest,
    vk_id: int,
    schema: UserUpdateSchema,
) -> ApiResponse[UserOutSchema]:
    container: Container = get_container()
    user_service: BaseUserService = container.resolve(BaseUserService)

    try:
        update_data: dict = schema.dict(exclude_unset=True)
        updated_user: User = user_service.update_by_vk_id(
            vk_id=vk_id,
            data=update_data,
        )

        return ApiResponse(data=UserOutSchema.from_entity(entity=updated_user))

    except UserNotFoundByVKIDException as error:
        logger.error(
            msg='Пользователь не найден.',
            extra={'error_meta': orjson.dumps(error).decode()},
        )
        raise HttpError(
            status_code=404,
            message=error.message,
        )
