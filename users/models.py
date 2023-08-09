from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('country'))

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.title


class UserManager(DjangoUserManager):
    def get_queryset(self):
        return super().get_queryset().annotate(rating=models.Avg('feedback_collectors__rating_score'))


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, _('User')),
        (MODERATOR, _('Moderator')),
        (ADMIN, _('Admin')),
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

    objects = UserManager()

    class Meta:
        ordering = ('username',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

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


class PublishModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class CollectorFeedback(models.Model):
    """Отзывы о коллекционерах с оценкой для пользовательского рейтинга."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name="feedback_users",
    )
    collector = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('collector'),
        related_name="feedback_collectors",
    )
    rating_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('rating score'),
    )
    feedback = models.TextField(verbose_name=_('feedback'))
    is_published = models.BooleanField(default=True,
                                       verbose_name=_('publish'))
    created = models.DateTimeField(auto_now=False, auto_now_add=True,
                                   verbose_name=_('Date of created'))
    updated = models.DateTimeField(auto_now=True, auto_now_add=False,
                                   verbose_name=_('Date of updated'))

    objects = models.Manager()
    published_objects = PublishModelManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'collector'],
                name='unique_feedback_relationships',
                violation_error_message=_('Feedback with this User and Collector already exists')
            ),
            models.CheckConstraint(
                check=~Q(user=F('collector')),
                name='prevent_self_feedback',
                violation_error_message=_('Feedback with matching User and Collector is not allowed')
            )
        ]
        ordering = ('-created',)
        verbose_name = _('feedback')
        verbose_name_plural = _('feedbacks')

    def __str__(self):
        return f'{self.collector} -> {self.user}'
