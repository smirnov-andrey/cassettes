from django.db import models
from django.db.models import Min, Max, Avg

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
    ('mint', 'Mint'),
    ('excellent', 'Excellent'),
    ('very_good', 'Very good'),
    ('good', 'Good'),
    ('poor', 'Poor')
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
    coil = models.BooleanField(verbose_name='Coil')
    slim_case = models.BooleanField(verbose_name='Slim case')
    price = models.CharField(verbose_name='Price', max_length=100)
    comment = models.TextField(verbose_name='Comments')
    category = models.ForeignKey(CassetteCategory, default=1, related_name='cassettes', on_delete=models.CASCADE, verbose_name='Category')
    brand = models.ForeignKey(CassetteBrand, on_delete=models.CASCADE, related_name='cassettes', verbose_name='Brand')
    type = models.ForeignKey(CassetteType, on_delete=models.CASCADE, verbose_name='Type')
    model = models.ForeignKey(CassetteModel, on_delete=models.CASCADE, verbose_name='Model')
    technology = models.ForeignKey(CassetteTechnology, on_delete=models.CASCADE, verbose_name='Technology')
    manufacturer = models.ForeignKey(CassetteManufacturer, on_delete=models.CASCADE, verbose_name='Manufacturer')
    series = models.ForeignKey(CassetteSeries, on_delete=models.CASCADE, verbose_name='Series')
    collection = models.ForeignKey(CassetteCollection, on_delete=models.CASCADE, verbose_name='Collection')
    tape_length = models.ForeignKey(CassetteTapeLength, on_delete=models.CASCADE, verbose_name='Tape Length')
    year_release = models.IntegerField(verbose_name='Year Release')

    class Meta:
        verbose_name = 'Add cassettes'
        verbose_name_plural = 'Cassettes'

    def __str__(self):
        return f'{self.brand} + {self.model} + {self.type} + {self.series}'


class CassettesImage(models.Model):
    """Модель изображений кассеты"""
    image = models.ImageField(upload_to='cassettes', verbose_name='Image')
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name='Cassette')

    class Meta:
        verbose_name = 'Add image for cassette'
        verbose_name_plural = 'Cassette images'


class CassetteBarcode(models.Model):
    """Модель штрихкода кассеты"""
    file = models.FileField(upload_to='barcode')
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name='Cassette')

    class Meta:
        verbose_name = 'Add barcode for cassette'
        verbose_name_plural = 'Cassette barcodes'


class CassetteFrequencyResponse(models.Model):
    """Модель частотной характеристики кассеты"""
    file = models.FileField(upload_to='frequeryresponse')
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, verbose_name='Cassette')

    class Meta:
        verbose_name = 'Add frequency response for cassette'
        verbose_name_plural = 'Cassette frequency responses'


