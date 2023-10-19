import random
import string
import uuid
from django.db import models
from django.db.models import F, Min, Max
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from pytils.translit import slugify

from core.models import Country
from users.models import Country, User


def title_slugify(model, title):
    slug = slugify(title)
    if model.objects.filter(slug=slug).exists():
        letters = string.ascii_lowercase
        slug = slug + '-' + ''.join(random.choice(letters) for _ in range(3))
    return slug[:50]


class PublishModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BaseModel(models.Model):
    """Базовая модель"""
    title = models.CharField(max_length=255, unique=True, verbose_name=_('title'))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Url/Slug'))
    is_published = models.BooleanField(default=True, verbose_name=_('Publish'))
    created = models.DateTimeField(auto_now=False, auto_now_add=True,
                                   verbose_name=_('Date of created'))
    updated = models.DateTimeField(auto_now=True, auto_now_add=False,
                                   verbose_name=_('Date of updated'))

    objects = models.Manager()
    published_objects = PublishModelManager()

    class Meta:
        abstract = True
        ordering = ('title', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        self.slug = title_slugify(self.__class__, self.title)
        super().save(*args, **kwargs)


class Category(BaseModel):
    """Модель категории"""
    AUDIO = 'audio'
    VIDEO = 'video'
    CATEGORY_TYPE = ((AUDIO, _('Audio')), (VIDEO, _('Video')),)
    type = models.CharField(max_length=5, choices=CATEGORY_TYPE, default=AUDIO)
    image = models.ImageField(upload_to='category', blank=True)
    logo = models.ImageField(upload_to='category_logo', blank=True)
    description = models.TextField(blank=True)
    brands = models.ManyToManyField('CassetteBrand', related_name='categories', blank=True, verbose_name=_('Brands'))
    is_published_to_home = models.BooleanField(default=False, verbose_name=_('Publish to home page'))
    display_order = models.IntegerField(blank=True, null=True, verbose_name=_('display order'))

    def cassettes_count(self):
        """Считаем количество кассет в категории"""
        return Cassette.objects.filter(brand__categories__slug=self.slug).count()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('display_order', 'type', 'title')



class CassetteBrand(BaseModel):
    """Модель бренда"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('country'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    image = models.ImageField(upload_to='brands', blank=True, verbose_name=_('image'))

    def cassette_year(self):
        """Вычисляем минимальный и максимальный год кассет в данном бренде"""
        year_period = Cassette.objects.filter(brand=self).aggregate(min=Min('year_release'), max=Max('year_release'))
        return year_period

    def admin_preview(self):
        return mark_safe(
            f'<img src = "{self.image.url}" width = "200"/>')
    admin_preview.short_description = _('image preview')

    def admin_list_preview(self):
        if self.image:
            return mark_safe(
                f'<img src = "{self.image.url}" width = "50"/>')

    admin_list_preview.short_description = _('image')

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')
        ordering = ('title',)




class CassetteModel(BaseModel):
    """Модель модели кассеты"""
    title = models.CharField(max_length=255, unique=False, verbose_name=_('title'))
    brand = models.ForeignKey(CassetteBrand, on_delete=models.PROTECT, verbose_name=_('brand'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} ({self.brand})'


class CassetteType(BaseModel):
    """Модель типа кассеты"""
    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')
        ordering = ('title',)



class CassetteTechnology(BaseModel):
    """Модель технологии кассеты"""
    class Meta:
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')
        ordering = ('title',)


class CassetteManufacturer(BaseModel):
    """Модель производителя кассеты"""
    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')
        ordering = ('title',)


class CassetteSeries(BaseModel):
    """Модель серии кассеты"""
    class Meta:
        verbose_name = _('Series')
        verbose_name_plural = _('Series')
        ordering = ('title',)


class CassetteSort(BaseModel):
    """Модель серии кассеты"""
    class Meta:
        verbose_name = _('sort')
        verbose_name_plural = _('sorts')
        ordering = ('title',)


class CassetteCollection(BaseModel):
    """Модель коллекции"""
    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')
        ordering = ('title',)


class CassetteTapeLength(models.Model):
    """Модель длины ленты"""
    tape_length = models.CharField(max_length=32,
                                   verbose_name=_('tape length'))

    class Meta:
        verbose_name = _('tape length')
        verbose_name_plural = _('tape lengtes')
        ordering = ('tape_length',)

    def __str__(self):
        return self.tape_length


class CassettePrice(models.Model):
    """Различные варианты цены в зависимости от состояния"""
    poor = models.IntegerField(null=True, blank=True, verbose_name=_('Poor price'))
    good = models.IntegerField(null=True, blank=True, verbose_name=_('Good price'))
    very_good = models.IntegerField(null=True, blank=True, verbose_name=_('Very good price'))
    excellent = models.IntegerField(null=True, blank=True, verbose_name=_('Excellent price'))
    near_mint = models.IntegerField(null=True, blank=True, verbose_name=_('Near mint price'))
    mint = models.IntegerField(null=True, blank=True, verbose_name=_('Mint price'))
    cassette = models.OneToOneField('Cassette', on_delete=models.CASCADE,
                                    related_name='prices',
                                    verbose_name=_('cassette'))

    class Meta:
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return f'{self.cassette} prices'


class Cassette(models.Model):
    """Модель кассеты"""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name=_('uuid'))
    # user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('User'))
    coil = models.BooleanField(verbose_name=_('Coil'), null=True, blank=True)
    slim_case = models.BooleanField(verbose_name=_('Slim case'), null=True, blank=True)
    comment = models.TextField(verbose_name=_('Comments'), null=True, blank=True,)
    category = models.ForeignKey(Category, default=1, related_name='cassettes', on_delete=models.PROTECT, verbose_name=_('Category'))
    brand = models.ForeignKey(CassetteBrand, on_delete=models.PROTECT, related_name='cassettes', verbose_name=_('Brand'))
    tape_type = models.ForeignKey(CassetteType, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('tape type'))
    model = models.ForeignKey(CassetteModel, null=True, blank=True,on_delete=models.PROTECT, verbose_name=_('Model'))
    technology = models.ForeignKey(CassetteTechnology, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('technology'))
    manufacturer = models.ForeignKey(CassetteManufacturer, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('manufacturer'))
    series = models.ForeignKey(CassetteSeries, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('series'))
    sort = models.ForeignKey(CassetteSort, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('sort'))
    # collection = models.ForeignKey(CassetteCollection, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('Collection'))
    tape_length = models.ForeignKey(CassetteTapeLength, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('tape Length'))
    year_release = models.IntegerField(null=True, blank=True, verbose_name=_('year Release'))
    country = models.ForeignKey(Country, related_name='country_cassettes', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_('country'))
    markets = models.ManyToManyField(Country,
                                     blank=True,
                                     related_name='markets_cassettes',
                                     verbose_name=_('markets'))
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('date of comment created'))
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('date of comment updated'))
    upload_row = models.IntegerField(null=True, blank=True) # temp field to match data at upload process

    class Meta:
        default_related_name = 'cassettes'
        verbose_name = _('cassette')
        verbose_name_plural = _('cassettes')


    def get_absolute_url(self):
        return reverse('catalog:cassette', kwargs={'id': self.pk})

    def __str__(self):
        if self.brand:
            brand = f' {self.brand.title}'
        else:
            brand = ''
        if self.model:
            model = f' {self.model.title}'
        else:
            model = ''
        if self.tape_type:
            tape_type = f' {self.tape_type.title}'
        else:
            tape_type = ''
        if self.tape_length:
            tape_length = f' {self.tape_length.tape_length}'
        else:
            tape_length = ''
        return f'{brand}{model}{tape_type}{tape_length}'


class Image(models.Model):
    """Модель изображений кассеты"""
    class View(models.IntegerChoices):
        PACKAGE_FRONT_SIDE = '1', _('Front side of the package'),
        PACKAGE_BACK_SIDE = '2', _('Back side of the package'),
        PACKAGE_END_SIDE = '3', _('End side'),
        BOX_FRONT_SIDE = '4', _('Front side of the box'),
        BOX_BACK_SIDE = '5', _('Back side of the box'),
        DESCRIPTION_ONE = '6', _('Description 1'),
        DESCRIPTION_TWO = '7', _('Description 2'),
        ITEM_SIDE_A = '8', _('Item (Side A)'),
        ITEM_SIDE_B = '9', _('Item (Side B)'),
        BOX_GENERAL_VIEW = '10', _('General view (Box)'),
        ITEM_GENERAL_VIEW = '11', _('General view (Item)'),
        GENERAL_VIEW = '12', _('General view'),
        BARCODE = '13', _('Barcode'),
        FREQUENCY_RESPONSE = '14', _('Frequency response'),


    def image_path(self, filename):
        return f'cassettes/{self.cassette.uuid}/{filename}'

    cassette = models.ForeignKey(Cassette,
                                 on_delete=models.CASCADE,
                                 related_name='images',
                                 verbose_name=_('cassette'))
    image = models.ImageField(upload_to=image_path,
                              verbose_name=_('image file'))
    view = models.PositiveSmallIntegerField(choices=View.choices, blank=True,
                                            null=True, verbose_name=_('view'))
    is_cover = models.BooleanField(default=False, verbose_name=_('cover'))
    is_publish = models.BooleanField(default=True, verbose_name=_('publish'))

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ('cassette', 'view')
        constraints = [
            models.UniqueConstraint(
                fields=['cassette', 'view'],
                condition=models.Q(is_publish=True),
                name='unique_cassette_view',
                violation_error_message=_('Only one unique view per '
                                          'cassette can be published')
            ),
            models.UniqueConstraint(
                fields=['cassette'],
                condition=models.Q(is_cover=True),
                name='unique_cassette_cover',
                violation_error_message=_('Only one view per cassette per '
                                          'cassette can be set as cover'),
            ),
        ]

    def admin_preview(self):
        return mark_safe(
            f'<img src = "{self.image.url}" width = "200"/>')
    admin_preview.short_description = _('image preview')

    def admin_list_preview(self):
        return mark_safe(
            f'<img src = "{self.image.url}" width = "100"/>')
    admin_list_preview.short_description = _('image')


class CassetteSeller(models.Model):
    """Продавец кассет"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Seller'))
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name=_('Cassette'))

    class Meta:
        verbose_name = _('Seller')
        verbose_name_plural = _('Sellers')

    def __str__(self):
        return f'{self.cassette} + {self.user}'


class CassetteChanger(models.Model):
    """Меняла"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Changer'))
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name=_('Cassette'))

    class Meta:
        verbose_name = _('Changer')
        verbose_name_plural = _('Changers')

    def __str__(self):
        return f'{self.cassette} + {self.user}'


class CassetteComment(models.Model):
    """Комментарии пользотвателей к касете"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'), related_name='comments')
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name=_('Cassette'), related_name='comments')
    comment = models.TextField(verbose_name=_('Comments'))
    is_published = models.BooleanField(default=False, verbose_name=_('Publish'))
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Date of comment created'))
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Date of comment updated'))

    objects = models.Manager()
    published_objects = PublishModelManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'{self.cassette} + {self.user}'

#
# class CollectionBaseModel(models.Model):
#     POOR = 'poor'
#     GOOD = 'good'
#     VERY_GOOD = 'very_good'
#     EXCELLENT = 'excellent'
#     NEAR_MINT = 'near_mint'
#     MINT = 'mint'
#     CONDITIONS = (
#         (POOR, _('Poor')),
#         (GOOD, _('Good')),
#         (VERY_GOOD, _('Very good')),
#         (EXCELLENT, _('Excellent')),
#         (NEAR_MINT, _('Near mint')),
#         (MINT, _('Mint')),
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name=_('User'),
#         related_name="%(app_label)s_%(class)s_related",
#         related_query_name="%(app_label)s_%(class)ss"
#     )
#     cassette = models.ForeignKey(
#         Cassette,
#         on_delete=models.CASCADE,
#         verbose_name=_('Cassette'),
#         related_name="%(app_label)s_%(class)s_related",
#         related_query_name="%(app_label)s_%(class)ss"
#     )
#     type = models.CharField(max_length=9, choices=CONDITIONS)
#     created = models.DateTimeField(auto_now=False, auto_now_add=True,
#                                    verbose_name=_('Date of created'))
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False,
#                                    verbose_name=_('Date of updated'))
#
#     class Meta:
#         abstract = True
#
#
# class PersonalCollection(CollectionBaseModel):
#     class Meta(CollectionBaseModel.Meta):
#         verbose_name = _('personal collection')
#         verbose_name_plural = _('personal collections')
#
#
# class WishlistCollection(CollectionBaseModel):
#     class Meta(CollectionBaseModel.Meta):
#         verbose_name = _('wishlist collection')
#         verbose_name_plural = _('wishlist collections')
#
#
# class ExchangeCollection(CollectionBaseModel):
#     class Meta(CollectionBaseModel.Meta):
#         verbose_name = _('exchange collection')
#         verbose_name_plural = _('exchange collections')
#
#
# class SellCollection(CollectionBaseModel):
#     class Meta(CollectionBaseModel.Meta):
#         verbose_name = _('sell collection')
#         verbose_name_plural = _('sell collections')

class Condition(models.Model):
    """Tape conditions model."""
    name = models.CharField(
        verbose_name=_('name'),
        unique=True,
        max_length=10,
    )
    abbreviation = models.CharField(
        verbose_name=_('abbreviation'),
        blank=True, unique=True, max_length=5,)
    description = models.CharField(
        verbose_name=_('description'),
        blank=True, max_length=5000,)
    is_published = models.BooleanField(default=True,
                                       verbose_name=_('publish'))

    class Meta:
        verbose_name = _('condition')
        verbose_name_plural = _('conditions')

    def __str__(self):
        return f'{self.name} ({self.abbreviation})'



