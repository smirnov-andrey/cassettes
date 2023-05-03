from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    title = models.CharField(max_length=200, verbose_name='Country')

    def __str__(self):
        return self.title


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    USER_LANGUAGE = (
        ('English', 'Английский'),
        ('Russian', 'Русский'),
        ('Spanish', 'Испанский'),
    )
    role = models.CharField(
        # Можно лучше: Тут обычно задают 9, как в moderator.
        # Я бы закладывался сразу с запасом
        max_length=20,
        choices=USER_ROLES,
        default=USER
    )
    premium = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to='profile')
    bio = models.TextField(blank=True)
    born_date = models.DateField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=200, choices=USER_LANGUAGE)
    website = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('username',)

    # Можно лучше: можно добавить тут property для удобства
    @property
    def is_admin(self):
        # Надо исправить: Везде, где мы используем роли - не используем строки,
        # а используем константу
        return (
            self.role == User.ADMIN
            or self.is_superuser
            # Я тут не уверен, считается ли стафф "администратором Django"
            # по спеке, но будем считать, что да
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR