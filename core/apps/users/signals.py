from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from core.apps.users.models import User as UserModel


def user_cache_key(vk_id: int) -> str:
    return f'user:vk_id:{vk_id}'


@receiver(post_save, sender=UserModel)
def invalidate_user_cache_on_save(sender, instance, **kwargs):
    cache.delete(user_cache_key(instance.vk_id))


@receiver(post_delete, sender=UserModel)
def invalidate_user_cache_on_delete(sender, instance, **kwargs):
    cache.delete(user_cache_key(instance.vk_id))
