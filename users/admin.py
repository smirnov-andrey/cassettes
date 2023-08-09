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


class CollectorFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'collector', 'rating_score', 'is_published')
    list_display_links = ('id', 'user', 'collector', 'rating_score')
    list_editable = ('is_published',)
    list_filter = ('rating_score', 'is_published', 'created', 'updated',)
    search_fields = ('id', 'user__username', 'user__first_name',
                     'user__last_name', 'user__email', 'collector__username',
                     'collector__first_name', 'collector__last_name',
                     'collector__email', 'rating_score', 'feedback')
    search_help_text = _('Search for feedback')
    actions_selection_counter = True
    show_full_result_count = True
    readonly_fields = ('id', 'created', 'updated')


admin.site.register(User)
admin.site.register(Country, CountryAdmin)
admin.site.register(CollectorFeedback, CollectorFeedbackAdmin)
