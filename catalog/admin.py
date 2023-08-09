from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from .models import *

class BasedAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', )
    list_display_links = ('id','title', 'slug', )
    list_editable = ('is_published',)
    list_filter = ('is_published', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated',)
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'title', 'title_en', 'title_ru', 'slug')
    search_help_text = _('Search by id, title or slug')
    fields = ('id', 'title', 'slug', 'is_published', 'created', 'updated', )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title_en"]}


class CassetteImageInline(admin.StackedInline):
    model = CassettesImage
    extra = 0


class CassettePriceInline(admin.TabularInline):
    model = CassettePrice
    extra = 0


class CassetteAdmin(TabbedTranslationAdmin):
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
    search_fields = ('id', 'user__username', 'user__first_name', 'user__last_name', 'cassette__brand__title', 'cassette__brand__title_en', 'cassette__brand__title_ru', 'cassette__model__title', 'cassette__model__title_en', 'cassette__model__title_ru','comment',)
    search_help_text = _('Search for comment by id, user, cassette or comment text')

class CassetteCategoryAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title', 'slug', 'type', 'is_published', 'is_published_to_home', )
    list_display_links = ('id','title', 'slug', 'type', )
    list_editable = ('is_published','is_published_to_home',)
    list_filter = ('type', 'is_published', 'is_published_to_home', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated',)
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'title', 'title_en', 'title_ru', 'slug', 'type', 'description', 'description_en', 'description_ru', 'brands__title', 'brands__description', 'brands__title_en', 'brands__description_en', 'brands__title_ru', 'brands__description_ru')
    search_help_text = _('Search for category by id, title, slug, description or brands')
    fields =  ('id', 'type', 'title', 'slug', 'logo', 'image', 'description', 'is_published', 'is_published_to_home', 'brands', 'created', 'updated', )
    filter_horizontal = ('brands', )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title_en"]}


class CassetteBrandAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title', 'slug', 'country', 'is_published', )
    list_display_links = ('id','title', 'slug', 'country', )
    list_editable = ('is_published',)
    list_filter = ('country', 'is_published', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated',)
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'title', 'title_en', 'title_ru', 'slug', 'country', 'description', 'description_en', 'description_ru', )
    search_help_text = _('Search for brand by id, title, slug, description')
    fields = ('id', 'title', 'slug', 'description', 'is_published', 'created', 'updated', )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title_en"]}


class CassetteModelAdmin(BasedAdmin):
    pass


class CassetteTypeAdmin(BasedAdmin):
    pass


class CassetteTechnologyAdmin(BasedAdmin):
    pass


class CassetteManufacturerAdmin(BasedAdmin):
    pass


class CassetteSeriesAdmin(BasedAdmin):
    pass


class CassetteCollectionAdmin(BasedAdmin):
    pass


admin.site.register(CassetteBrand, CassetteBrandAdmin)
admin.site.register(CassetteType, CassetteTypeAdmin)
admin.site.register(CassetteSeries, CassetteSeriesAdmin)
admin.site.register(CassetteManufacturer, CassetteManufacturerAdmin)
admin.site.register(CassetteCollection, CassetteCollectionAdmin)
admin.site.register(CassetteTapeLength)
admin.site.register(CassetteTechnology, CassetteTechnologyAdmin)
admin.site.register(CassetteModel, CassetteModelAdmin)
admin.site.register(Cassette, CassetteAdmin)
admin.site.register(CassetteCategory, CassetteCategoryAdmin)
admin.site.register(CassetteSeller)
admin.site.register(CassetteChanger)
admin.site.register(CassettesImage)
admin.site.register(CassetteComment, CassetteCommentAdmin)
# admin.site.register(PersonalCollection)
# admin.site.register(WishlistCollection)
# admin.site.register(ExchangeCollection)
# admin.site.register(SellCollection)


