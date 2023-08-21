from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import Condition, Cassette
from users.models import User


class CollectionBaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name=_('cassette'))
    condition = models.ForeignKey(Condition,  on_delete=models.PROTECT, verbose_name=_('condition'))
    price = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('price'))

    class Meta:
        abstract = True


class Collection(CollectionBaseModel):

    class Meta:
        default_related_name = 'collections'


class Wishlist(CollectionBaseModel):

    class Meta:
        default_related_name = 'whishlists'


class Exchange(CollectionBaseModel):

    class Meta:
        default_related_name = 'exchanges'


class Sale(CollectionBaseModel):

    class Meta:
        default_related_name = 'sales'
