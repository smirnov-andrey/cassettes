from django.db import models
from django.db.models import Min, Max
from django.urls import reverse

from users.models import Country, User
from pytils.translit import slugify


class BaseModel(models.Model):
    """Базовая модель"""
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class CassetteCategory(BaseModel):
    """Модель категории"""
    image = models.ImageField(upload_to='category', blank=True)
    logo = models.ImageField(upload_to='category_logo', blank=True)
    description = models.TextField(blank=True)
    brands = models.ManyToManyField('CassetteBrand', related_name='categories', blank=True, verbose_name='Brands')

    def cassettes_count(self):
        """Считаем количество кассет в категории"""
        return Cassette.objects.filter(brand__categories__slug=self.slug).count()


class CassetteBrand(BaseModel):
    """Модель бренда"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Country')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='brands', blank=True, verbose_name='image')

    def cassette_year(self):
        """Вычисляем минимальный и максимальный год кассет в данном бренде"""
        year_period = Cassette.objects.filter(brand=self).aggregate(min=Min('year_release'), max=Max('year_release'))
        return year_period


class CassetteModel(BaseModel):
    """Модель модели кассеты"""
    pass


class CassetteType(BaseModel):
    """Модель типа кассеты"""
    pass


class CassetteTechnology(BaseModel):
    """Модель технологии кассеты"""
    pass


class CassetteManufacturer(BaseModel):
    """Модель производителя кассеты"""
    pass


class CassetteSeries(BaseModel):
    """Модель серии кассеты"""
    pass


class CassetteCollection(BaseModel):
    """Модель коллекции"""
    pass


class CassetteTapeLength(models.Model):
    """Модель длины ленты"""
    tape_length = models.IntegerField(verbose_name='Tape length')

    def __str__(self):
        return f'{self.tape_length}'


CASSETTECONDITION = (
    ('poor', 'Poor'),
    ('good', 'Good'),
    ('very_good', 'Very good'),
    ('excellent', 'Excellent'),
    ('nearmint', 'Near mint'),
    ('mint', 'Mint'),
)


class CassettePrice(models.Model):
    """Различные варианты цены в зависимости от состояния"""
    price = models.IntegerField(verbose_name='price')
    condition = models.CharField(max_length=100, choices=CASSETTECONDITION, verbose_name='condition')
    cassette = models.ForeignKey('Cassette', on_delete=models.CASCADE, related_name='prices', verbose_name='cassette')

    class Meta:
        verbose_name = 'Add cassette price'
        verbose_name_plural = 'Cassettes prices'

    def __str__(self):
        return f'{self.cassette} - {self.price}'


class Cassette(models.Model):
    """Модель кассеты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    coil = models.BooleanField(verbose_name='Coil', null=True, blank=True)
    slim_case = models.BooleanField(verbose_name='Slim case', null=True, blank=True)
    comment = models.TextField(verbose_name='Comments', null=True, blank=True,)
    category = models.ForeignKey(CassetteCategory, default=1, related_name='cassettes', on_delete=models.CASCADE, verbose_name='Category')
    brand = models.ForeignKey(CassetteBrand, on_delete=models.CASCADE, related_name='cassettes', verbose_name='Brand')
    type = models.ForeignKey(CassetteType, on_delete=models.CASCADE, verbose_name='Type')
    model = models.ForeignKey(CassetteModel, null=True, blank=True,on_delete=models.CASCADE, verbose_name='Model')
    technology = models.ForeignKey(CassetteTechnology, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Technology')
    manufacturer = models.ForeignKey(CassetteManufacturer, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Manufacturer')
    series = models.ForeignKey(CassetteSeries, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Series')
    collection = models.ForeignKey(CassetteCollection, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Collection')
    tape_length = models.ForeignKey(CassetteTapeLength, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Tape Length')
    year_release = models.IntegerField(null=True, blank=True, verbose_name='Year Release')

    class Meta:
        verbose_name = 'Add cassettes'
        verbose_name_plural = 'Cassettes'


    def get_absolute_url(self):
        return reverse('catalog:cassette', kwargs={'id': self.pk})

    def __str__(self):
        return f'{self.model} - {self.user}'


class CassettesImage(models.Model):
    """Модель изображений кассеты"""
    package_front_side = models.ImageField(upload_to='cassettes', verbose_name='Front side of the package', null=True, blank=True)
    package_back_side = models.ImageField(upload_to='cassettes', verbose_name='Back side of the package', null=True, blank=True)
    package_end_side = models.ImageField(upload_to='cassettes', verbose_name='End side', null=True, blank=True)
    box_front_side = models.ImageField(upload_to='cassettes', verbose_name='Front side of the box', null=True, blank=True)
    box_back_side = models.ImageField(upload_to='cassettes', verbose_name='Back side of the box', null=True, blank=True)
    description_one = models.ImageField(upload_to='cassettes', verbose_name='Description 1', null=True, blank=True)
    description_two = models.ImageField(upload_to='cassettes', verbose_name='Description 2', null=True, blank=True)
    item_side_a = models.ImageField(upload_to='cassettes', verbose_name='Item (Side A)', null=True, blank=True)
    item_side_b = models.ImageField(upload_to='cassettes', verbose_name='Item (Side B)', null=True, blank=True)
    box_general_view = models.ImageField(upload_to='cassettes', verbose_name='General view (Box)', null=True, blank=True)
    item_general_view = models.ImageField(upload_to='cassettes', verbose_name='General view (Item)', null=True, blank=True)
    general_view = models.ImageField(upload_to='cassettes', verbose_name='General view', null=True, blank=True)
    barcode = models.ImageField(upload_to='cassettes', verbose_name='General view', null=True, blank=True)
    frequency_response = models.ImageField(upload_to='cassettes', verbose_name='General view', null=True, blank=True)
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name='Cassette', null=True, blank=True)

    class Meta:
        verbose_name = 'Add image for cassette'
        verbose_name_plural = 'Cassette images'


class CassetteSeller(models.Model):
    """Продавец кассет"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Seller')
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name='Cassette')

    class Meta:
        verbose_name = 'Cassette sellers'
        verbose_name_plural = 'Cassette seller'

    def __str__(self):
        return f'{self.cassette} + {self.user}'


class CassetteChanger(models.Model):
    """Меняла"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Changer')
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name='Cassette')

    class Meta:
        verbose_name = 'Cassette changers'
        verbose_name_plural = 'Cassette changer'

    def __str__(self):
        return f'{self.cassette} + {self.user}'