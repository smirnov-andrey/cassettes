from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User, Country

from modeltranslation.admin import TabbedTranslationAdmin


from .models import *


class CountryAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id','title',)
    readonly_fields = ('id', )
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'title','title_en', 'title_ru')
    search_help_text = _('Search for Country by country name or id')
    fields = ('id', 'title',)


admin.site.register(User)
admin.site.register(Country, CountryAdmin)
