from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from .models import *


# Register your models here.
@admin.register(GlobalText)
class GlobalTextAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'system_name', 'admin_name',)
    list_display_links = ('id', 'system_name', 'admin_name',)
    fields = ('id', 'system_name', 'admin_name', 'title', 'text')
    search_fields = ('id', 'system_name', 'admin_name', 'title', 'text')
    readonly_fields = ('id', 'system_name')


