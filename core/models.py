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


class GlobalText(models.Model):
    system_name = models.CharField(max_length=200, verbose_name=_(
        'system name'))
    admin_name = models.CharField(max_length=200, verbose_name=_(
        'admin name'))
    title = models.CharField(blank=True, max_length=200, verbose_name=_(
        'title'))
    text = models.TextField(blank=True, verbose_name='text')

    class Meta:
        verbose_name = _('global text')
        verbose_name_plural = _('global texts')
        ordering = ('system_name',)

    def __str__(self):
        return self.admin_name