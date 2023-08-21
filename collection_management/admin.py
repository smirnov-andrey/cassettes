from django.contrib import admin

from .models import *


class BaseCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cassette', 'condition', 'price')
    list_display_links = ('id', 'user', 'cassette', 'condition', 'price')
    list_filter = ('condition', 'price')
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'user__username', 'user__first_name', 'user__last_name', 'user__email',
                     'cassette__brand__title', 'cassette__brand__title_en', 'cassette__brand__title_ru',
                     'cassette__model__title', 'cassette__model__title_en', 'cassette__model__title_ru',
                     'condition__name', 'price')


admin.site.register(Collection, BaseCollectionAdmin)
admin.site.register(Wishlist, BaseCollectionAdmin)
admin.site.register(Exchange, BaseCollectionAdmin)
admin.site.register(Sale, BaseCollectionAdmin)