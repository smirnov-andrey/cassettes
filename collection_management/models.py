from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import Condition, Cassette
from users.models import User


class CollectionBaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name=_('cassette'))

    class Meta:
        abstract = True


class Collection(CollectionBaseModel):
    condition = models.ForeignKey(Condition, null=True, on_delete=models.PROTECT, verbose_name=_('condition'))
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('price'))

    class Meta:
        default_related_name = 'collections'
        constraints = [
            models.UniqueConstraint(fields=['user', 'cassette', 'condition'],
                                    name='unique_cassette_in_collection')
        ]


class Wishlist(CollectionBaseModel):

    class Meta:
        default_related_name = 'wishlists'
        constraints = [
            models.UniqueConstraint(fields=['user', 'cassette'],
                                    name='unique_cassette_in_wishlist')
        ]


class Exchange(CollectionBaseModel):

    class Meta:
        default_related_name = 'exchanges'
        constraints = [
            models.UniqueConstraint(fields=['user', 'cassette'],
                                    name='unique_cassette_in_exchange')
        ]


class Sale(CollectionBaseModel):

    class Meta:
        default_related_name = 'sales'
        constraints = [
            models.UniqueConstraint(fields=['user', 'cassette'],
                                    name='unique_cassette_in_sale')
        ]