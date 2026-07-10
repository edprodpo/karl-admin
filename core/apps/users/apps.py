from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'core.apps.users'
    verbose_name = 'Пользователи'
    label = 'users'

    def ready(self) -> None:
        from core.apps.users import signals  # noqa
