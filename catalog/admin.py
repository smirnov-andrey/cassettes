from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import RadioSelect
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from .models import *


class BasedAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', )
    list_display_links = ('id', 'title', 'slug', )
    list_editable = ('is_published',)
    list_filter = ('is_published', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated',)
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'title', 'title_en', 'title_ru', 'slug')
    search_help_text = _('Search by id, title or slug')
    fields = ('id', 'title', 'slug', 'is_published', 'created', 'updated', )
    ordering = ('title', )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title_en"]}


class ImageInlineForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


    # def __init__(self, *args, **kwargs):
    #     super(ImageInlineForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['is_cover'].widget = forms.RadioSelect()

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     is_cover = cleaned_data.get('is_cover')
    #     cassette = cleaned_data.get('cassette')
    #     if is_cover and Image.objects.filter(
    #         cassette=cassette,
    #         is_cover=is_cover
    #     ).exists():
    #         raise forms.ValidationError(_('Only one view per cassette per '
    #                                       'cassette can be set as cover'))
    #     super(ImageInlineForm, self).clean()


class ImageInline(admin.TabularInline):
    model = Image
    fields = ('id', 'admin_list_preview', 'view', 'is_cover', 'is_publish', 'image', )
    readonly_fields = ('id', 'admin_list_preview')
    form = ImageInlineForm
    # formfield_overrides = {
    #     'is_cover': {'widget': RadioSelect},
    # }
    # autocomplete_fields = ('product',)
    show_change_link = True
    can_delete = True
    extra = 0


class CassettePriceInline(admin.TabularInline):
    model = CassettePrice
    extra = 0


class ImageAdmin(admin.ModelAdmin):
    list_display = ('admin_list_preview', 'id', 'cassette', 'view',
                    'is_cover', 'is_publish',)
    list_display_links = ('id', 'admin_list_preview')
    list_editable = ('cassette', 'view', 'is_cover', 'is_publish')
    list_filter = ('is_cover', 'is_publish',  'view')
    readonly_fields = ('id', 'admin_list_preview')
    search_fields = ('cassette', 'view')
    actions_selection_counter = True
    show_full_result_count = True
    autocomplete_fields = ('cassette', )


class CassetteAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'brand', 'manufacturer', 'model', 'tape_type',
                    'tape_length', 'year_release', 'country')
    list_display_links = ('id',)
    search_fields = ('brand__title', 'model__title', 'manufacturer__title',
                     'series__title')
    filter_horizontal = ('markets', )
    autocomplete_fields = ('brand', 'manufacturer', 'model',)
    inlines = [ImageInline, CassettePriceInline]


class CassetteCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cassette', 'created', 'is_published', )
    list_display_links = ('id', 'user', 'cassette', 'created', )
    list_editable = ('is_published', )
    ordering = ('-created',)
    list_filter = ('is_published', 'created', 'updated', )
    readonly_fields = ('id', 'created', 'updated')
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'user__username', 'user__first_name', 'user__last_name', 'cassette__brand__title', 'cassette__brand__title_en', 'cassette__brand__title_ru', 'cassette__model__title', 'cassette__model__title_en', 'cassette__model__title_ru','comment',)
    search_help_text = _('Search for comment by id, user, cassette or comment text')


class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title', 'slug', 'type',
                    'display_order', 'is_published', 'is_published_to_home', )
    list_display_links = ('id', 'title', 'slug', 'type', )
    list_editable = ('display_order', 'is_published', 'is_published_to_home',)
    list_filter = ('type', 'is_published', 'is_published_to_home', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated',)
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'title', 'title_en', 'title_ru', 'slug', 'type', 'description', 'description_en', 'description_ru', 'brands__title', 'brands__description', 'brands__title_en', 'brands__description_en', 'brands__title_ru', 'brands__description_ru')
    search_help_text = _('Search for category by id, title, slug, description or brands')
    fields = ('id', 'type', 'title', 'slug', 'logo', 'image', 'description', 'display_order', 'is_published', 'is_published_to_home', 'brands', 'created', 'updated', )
    filter_horizontal = ('brands', )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title_en"]}


class CassetteBrandAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'title', 'country', 'is_published', 'admin_list_preview')
    list_display_links = ('id', 'title', 'country', 'admin_list_preview')
    list_editable = ('is_published',)
    list_filter = ('country', 'is_published', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated', 'admin_preview', 'admin_list_preview')
    actions_selection_counter = True
    show_full_result_count = True
    search_fields = ('id', 'title', 'title_en', 'title_ru', 'slug', 'description', 'description_en', 'description_ru', )
    search_help_text = _('Search for brand by id, title, slug, description')
    fields = ('id', 'title', 'slug', 'description', 'image', 'admin_preview', 'is_published', 'created', 'updated', )
    ordering = ('title', )

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        else:
            return {"slug": ["title_en"]}


class CassetteModelAdmin(BasedAdmin):
    list_display = ('id', 'brand', 'title', 'slug', 'is_published', )
    fields = ('id', 'brand', 'title', 'slug', 'is_published', 'created',
              'updated',)
    autocomplete_fields = ('brand', )


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
admin.site.register(Category, CategoryAdmin)
# admin.site.register(CassetteSeller)
# admin.site.register(CassetteChanger)
admin.site.register(Image, ImageAdmin)
admin.site.register(CassetteComment, CassetteCommentAdmin)
admin.site.register(Condition)
