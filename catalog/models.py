from django.db import models
from django.db.models import Min, Max
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.models import Country, User
from pytils.translit import slugify


class BaseModel(models.Model):
    """Базовая модель"""
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Url/Slug'))
    is_published = models.BooleanField(default=False, verbose_name=_('Publish'))
    created = models.DateTimeField(auto_now=False, auto_now_add=True,
                                   verbose_name=_('Date of created'))
    updated = models.DateTimeField(auto_now=True, auto_now_add=False,
                                   verbose_name=_('Date of updated'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class CassetteCategory(BaseModel):
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

    def cassettes_count(self):
        """Считаем количество кассет в категории"""
        return Cassette.objects.filter(brand__categories__slug=self.slug).count()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class CassetteBrand(BaseModel):
    """Модель бренда"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('country'))
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='brands', blank=True, verbose_name=_('image'))

    def cassette_year(self):
        """Вычисляем минимальный и максимальный год кассет в данном бренде"""
        year_period = Cassette.objects.filter(brand=self).aggregate(min=Min('year_release'), max=Max('year_release'))
        return year_period

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')


class CassetteModel(BaseModel):
    """Модель модели кассеты"""
    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')


class CassetteType(BaseModel):
    """Модель типа кассеты"""
    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')


class CassetteTechnology(BaseModel):
    """Модель технологии кассеты"""
    class Meta:
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')


class CassetteManufacturer(BaseModel):
    """Модель производителя кассеты"""
    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')


class CassetteSeries(BaseModel):
    """Модель серии кассеты"""
    class Meta:
        verbose_name = _('Series')
        verbose_name_plural = _('Series')


class CassetteCollection(BaseModel):
    """Модель коллекции"""
    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')


class CassetteTapeLength(models.Model):
    """Модель длины ленты"""
    tape_length = models.IntegerField(verbose_name=_('Tape length'))

    class Meta:
        verbose_name = _('Tape length')
        verbose_name_plural = _('Tape lengtes')

    def __str__(self):
        return f'{self.tape_length}'


class CassettePrice(models.Model):
    """Различные варианты цены в зависимости от состояния"""
    poor = models.IntegerField(null=True, blank=True, verbose_name=_('Poor price'))
    good = models.IntegerField(null=True, blank=True, verbose_name=_('Good price'))
    very_good = models.IntegerField(null=True, blank=True, verbose_name=_('Very good price'))
    excellent = models.IntegerField(null=True, blank=True, verbose_name=_('Excellent price'))
    near_mint = models.IntegerField(null=True, blank=True, verbose_name=_('Near mint price'))
    mint = models.IntegerField(null=True, blank=True, verbose_name=_('Mint price'))
    cassette = models.ForeignKey('Cassette', on_delete=models.CASCADE, related_name='prices', verbose_name=_('cassette'))

    class Meta:
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return f'{self.cassette} prices'


class Cassette(models.Model):
    """Модель кассеты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    coil = models.BooleanField(verbose_name=_('Coil'), null=True, blank=True)
    slim_case = models.BooleanField(verbose_name=_('Slim case'), null=True, blank=True)
    comment = models.TextField(verbose_name=_('Comments'), null=True, blank=True,)
    category = models.ForeignKey(CassetteCategory, default=1, related_name='cassettes', on_delete=models.CASCADE, verbose_name=_('Category'))
    brand = models.ForeignKey(CassetteBrand, on_delete=models.CASCADE, related_name='cassettes', verbose_name=_('Brand'))
    type = models.ForeignKey(CassetteType, on_delete=models.CASCADE, verbose_name=_('Type'))
    model = models.ForeignKey(CassetteModel, null=True, blank=True,on_delete=models.CASCADE, verbose_name=_('Model'))
    technology = models.ForeignKey(CassetteTechnology, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Technology'))
    manufacturer = models.ForeignKey(CassetteManufacturer, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Manufacturer'))
    series = models.ForeignKey(CassetteSeries, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Series'))
    collection = models.ForeignKey(CassetteCollection, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Collection'))
    tape_length = models.ForeignKey(CassetteTapeLength, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Tape Length'))
    year_release = models.IntegerField(null=True, blank=True, verbose_name=_('Year Release'))
    created = models.DateTimeField(auto_now=False, auto_now_add=True,
                                   verbose_name=_('Date of comment created'))
    updated = models.DateTimeField(auto_now=True, auto_now_add=False,
                                   verbose_name=_('Date of comment updated'))

    class Meta:
        verbose_name = _('Cassette')
        verbose_name_plural = _('Cassettes')


    def get_absolute_url(self):
        return reverse('catalog:cassette', kwargs={'id': self.pk})

    def __str__(self):
        return f'{self.model} - {self.user}'


class CassettesImage(models.Model):
    """Модель изображений кассеты"""
    package_front_side = models.ImageField(upload_to='cassettes', verbose_name=_('Front side of the package'), null=True, blank=True)
    package_back_side = models.ImageField(upload_to='cassettes', verbose_name=_('Back side of the package'), null=True, blank=True)
    package_end_side = models.ImageField(upload_to='cassettes', verbose_name=_('End side'), null=True, blank=True)
    box_front_side = models.ImageField(upload_to='cassettes', verbose_name=_('Front side of the box'), null=True, blank=True)
    box_back_side = models.ImageField(upload_to='cassettes', verbose_name=_('Back side of the box'), null=True, blank=True)
    description_one = models.ImageField(upload_to='cassettes', verbose_name=_('Description 1'), null=True, blank=True)
    description_two = models.ImageField(upload_to='cassettes', verbose_name=_('Description 2'), null=True, blank=True)
    item_side_a = models.ImageField(upload_to='cassettes', verbose_name=_('Item (Side A)'), null=True, blank=True)
    item_side_b = models.ImageField(upload_to='cassettes', verbose_name=_('Item (Side B)'), null=True, blank=True)
    box_general_view = models.ImageField(upload_to='cassettes', verbose_name=_('General view (Box)'), null=True, blank=True)
    item_general_view = models.ImageField(upload_to='cassettes', verbose_name=_('General view (Item)'), null=True, blank=True)
    general_view = models.ImageField(upload_to='cassettes', verbose_name=_('General view'), null=True, blank=True)
    barcode = models.ImageField(upload_to='cassettes', verbose_name=_('General view'), null=True, blank=True)
    frequency_response = models.ImageField(upload_to='cassettes', verbose_name=_('General view'), null=True, blank=True)
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name=_('Cassette'), null=True, blank=True)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


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

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'{self.cassette} + {self.user}'
