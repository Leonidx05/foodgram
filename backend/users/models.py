from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F

from foodgram.constants import EMAIL_MAX, USER_MAX


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    email = models.EmailField(
        max_length=EMAIL_MAX,
        unique=True,
        verbose_name='E-mail'
    )
    username = models.CharField(
        max_length=USER_MAX,
        unique=True,
        verbose_name='Юзернейм'
    )
    first_name = models.CharField(
        max_length=USER_MAX,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=USER_MAX,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=USER_MAX,
        verbose_name='Пароль'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscriptions_unique'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'
