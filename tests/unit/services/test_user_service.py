import pytest
from faker import Faker
from tests.factories.users import UserModelFactory

from core.apps.users.entities.users import User as UserEntity
from core.apps.users.exceptions.users import (
    UserExistException,
    UserNotFoundByVKIDException,
)
from core.apps.users.models.users import User as UserModel
from core.apps.users.services.users import BaseUserService


@pytest.mark.django_db
def test_user_service_create(
    user_service: BaseUserService,
):
    user_dto: UserModel = UserModelFactory.build()

    created_user: UserEntity = user_service.create(user=user_dto.to_entity())

    assert created_user.vk_id == user_dto.vk_id, f'{created_user=}'
    assert created_user.name == user_dto.name, f'{created_user=}'
    assert created_user.email == user_dto.email, f'{created_user=}'
    assert created_user.thread_id == user_dto.thread_id, f'{created_user=}'


@pytest.mark.django_db
def test_user_service_create_exist_exception(
    user_service: BaseUserService,
):
    user_dto: UserModel = UserModelFactory.build()
    user_service.create(user=user_dto.to_entity())

    with pytest.raises(UserExistException):
        user_service.create(user=user_dto.to_entity())


@pytest.mark.django_db
def test_user_service_get_by_vk_id(
    user_service: BaseUserService,
):
    user_dto: UserModel = UserModelFactory.create()
    fetched_user: UserEntity = user_service.get_by_vk_id(user_dto.vk_id)

    assert fetched_user.name == user_dto.name, f'{fetched_user=}'
    assert fetched_user.email == user_dto.email, f'{fetched_user=}'
    assert fetched_user.thread_id == user_dto.thread_id, f'{fetched_user=}'


@pytest.mark.django_db
def test_user_service_get_by_vk_id_not_found_exception(
    user_service: BaseUserService,
):
    user_dto: UserModel = UserModelFactory.build()

    with pytest.raises(UserNotFoundByVKIDException):
        user_service.get_by_vk_id(vk_id=user_dto.vk_id)


@pytest.mark.django_db
def test_user_service_update_by_vk_id(
    user_service: BaseUserService,
    faker: Faker,
):
    user_dto: UserModel = UserModelFactory.create()
    data: dict = {
        'email': faker.email(),
        'name': faker.name(),
        'thread_id': faker.text(max_nb_chars=128),
    }

    updated_user: UserEntity = user_service.update_by_vk_id(
        vk_id=user_dto.vk_id,
        data=data,
    )

    assert updated_user.email != user_dto.email, f'{updated_user=}'
    assert updated_user.name != user_dto.name, f'{updated_user=}'
    assert updated_user.thread_id != user_dto.thread_id, f'{updated_user=}'


@pytest.mark.django_db
def test_user_service_update_by_vk_id_not_found_exception(
    user_service: BaseUserService,
    faker: Faker,
):
    data: dict = {
        'email': faker.email(),
        'name': faker.name(),
        'thread_id': faker.text(max_nb_chars=128),
    }

    with pytest.raises(UserNotFoundByVKIDException):
        user_service.update_by_vk_id(
            vk_id=faker.random_int(),
            data=data,
        )
