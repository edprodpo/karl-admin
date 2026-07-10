from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'core.apps.chats'
    verbose_name = 'Чат'
    label = 'chats'

    def ready(self) -> None:
        from core.apps.chats import signals  # noqa
