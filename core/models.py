from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('country'))

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ('title', )

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('language'))

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        ordering = ('title',)

    def __str__(self):
        return self.title
