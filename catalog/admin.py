from django.contrib import admin
from .models import *


class CassetteImageInline(admin.StackedInline):
    model = CassettesImage
    extra = 0


class CassettePriceInline(admin.TabularInline):
    model = CassettePrice
    extra = 0


class CassetteAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'year_release', 'user', )
    list_display_links = ('id', 'brand', 'model', 'year_release', 'user', )
    inlines = [CassetteImageInline, CassettePriceInline]


class CassetteCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cassette', 'created', 'is_published', )
    list_display_links = ('id', 'user', 'cassette', 'created', )
    list_editable = ('is_published', )
    ordering = ('-created',)
    list_filter = ('is_published', 'created', 'updated', )
    readonly_fields = ('id', 'created', 'updated',)
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'user__username', 'user__first_name', 'user__last_name', 'cassette__brand__title', 'cassette__model__title','comment',)
    search_help_text = 'Search for comment by id, user, cassette or comment text'


admin.site.register(CassetteBrand)
admin.site.register(CassetteType)
admin.site.register(CassetteSeries)
admin.site.register(CassetteManufacturer)
admin.site.register(CassetteCollection)
admin.site.register(CassetteTapeLength)
admin.site.register(CassetteTechnology)
admin.site.register(CassetteModel)
admin.site.register(Cassette, CassetteAdmin)
admin.site.register(CassetteCategory)
admin.site.register(CassetteSeller)
admin.site.register(CassetteChanger)
admin.site.register(CassettesImage)
admin.site.register(CassetteComment, CassetteCommentAdmin)
