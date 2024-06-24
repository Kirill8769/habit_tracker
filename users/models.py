from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите почту')
    tg_chat_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name='ID телеграм',
        help_text='Укажите ID телеграм'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
