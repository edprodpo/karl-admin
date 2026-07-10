from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.users.entities.users import User as UserEntity


class User(TimedBaseModel):
    vk_id = models.BigIntegerField(
        verbose_name='VK ID',
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=256,
        unique=False,
        null=True,
        blank=True,
    )
    thread_id = models.CharField(
        verbose_name='THREAD ID',
        max_length=256,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name if self.name else f'Пользователь {self.vk_id}'

    @classmethod
    def from_entity(cls, user: UserEntity) -> 'User':
        return cls(
            vk_id=user.vk_id,
            email=user.email,
            name=user.name,
            thread_id=user.thread_id,
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        model_fields = {f.name for f in cls._meta.get_fields() if isinstance(f, models.Field)}
        filtered_data = {k: v for k, v in data.items() if k in model_fields}
        return cls(**filtered_data)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.pk,
            vk_id=self.vk_id,
            email=self.email,
            name=self.name,
            thread_id=self.thread_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.pk,
            'vk_id': self.vk_id,
            'email': self.email,
            'name': self.name,
            'thread_id': self.thread_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['vk_id'],
                condition=models.Q(vk_id__isnull=False),
                name='unique_vk_id_not_null',
            ),
            models.UniqueConstraint(
                fields=['email'],
                condition=models.Q(email__isnull=False),
                name='unique_email_not_null',
            ),
            models.UniqueConstraint(
                fields=['thread_id'],
                condition=models.Q(thread_id__isnull=False),
                name='unique_thread_id_not_null',
            ),
        ]
