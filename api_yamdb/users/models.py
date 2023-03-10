from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )

    role = models.CharField(
        verbose_name='Роль',
        choices=USER_ROLES,
        default=USER,
        max_length=20
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150,
        db_index=True
    )
    email = models.EmailField(
        verbose_name='Почта',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=10,
        null=True
    )

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
