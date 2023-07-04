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

class CassetteCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'type', 'is_published', 'is_published_to_home', )
    list_display_links = ('id','title', 'slug', 'type', )
    list_editable = ('is_published','is_published_to_home',)
    list_filter = ('type', 'is_published', 'is_published_to_home', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated',)
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = (
    'id', 'title', 'slug', 'type', 'description', 'brands__title', 'brands__description')
    search_help_text = 'Search for comment by id, title, slug, description or brands'
    fields =  ('id', 'type', 'title', 'slug', 'logo', 'image', 'description', 'is_published', 'is_published_to_home', 'brands', 'created', 'updated', )
    filter_horizontal = ('brands', )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title"]}


admin.site.register(CassetteBrand)
admin.site.register(CassetteType)
admin.site.register(CassetteSeries)
admin.site.register(CassetteManufacturer)
admin.site.register(CassetteCollection)
admin.site.register(CassetteTapeLength)
admin.site.register(CassetteTechnology)
admin.site.register(CassetteModel)
admin.site.register(Cassette, CassetteAdmin)
admin.site.register(CassetteCategory, CassetteCategoryAdmin)
admin.site.register(CassetteSeller)
admin.site.register(CassetteChanger)
admin.site.register(CassettesImage)
admin.site.register(CassetteComment, CassetteCommentAdmin)
