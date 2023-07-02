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
admin.site.register(CassetteComment)