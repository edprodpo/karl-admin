import factory
from factory.django import DjangoModelFactory

from core.apps.users.models.users import User as UserModel


class UserModelFactory(DjangoModelFactory):
    vk_id = factory.Faker('random_int')
    email = factory.Faker('email')
    name = factory.Faker('name')
    thread_id = factory.Faker('text')

    class Meta:
        model = UserModel
