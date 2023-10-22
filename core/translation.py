from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(GlobalText)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'text')






