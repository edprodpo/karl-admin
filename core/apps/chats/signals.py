from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from core.apps.chats.models.chats import Chat as ChatModel


def chat_cache_key(chat_id: int) -> str:
    return f'chat:chat_id:{chat_id}'


@receiver(post_save, sender=ChatModel)
def invalidate_chat_cache_on_save(sender, instance, **kwargs):
    cache.delete(chat_cache_key(instance.chat_id))


@receiver(post_delete, sender=ChatModel)
def invalidate_chat_cache_on_delete(sender, instance, **kwargs):
    cache.delete(chat_cache_key(instance.chat_id))
