from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(BaseModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(CassetteCategory)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(CassetteBrand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(CassetteModel)
class ModelTranslationOptions(TranslationOptions):
    pass


@register(CassetteType)
class TypeTranslationOptions(TranslationOptions):
    pass


@register(CassetteTechnology)
class TechnologyTranslationOptions(TranslationOptions):
    pass


@register(CassetteManufacturer)
class ManufacturerTranslationOptions(TranslationOptions):
    pass


@register(CassetteSeries)
class SeriesTranslationOptions(TranslationOptions):
    pass


@register(CassetteCollection)
class CollectionTranslationOptions(TranslationOptions):
    pass


@register(Cassette)
class CassetteTranslationOptions(TranslationOptions):
    fields = ('comment', )





