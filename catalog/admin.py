from django.contrib import admin
from .models import *


class CassetteImageInline(admin.TabularInline):
    model = CassettesImage
    extra = 3


class CassetteFrequencyResponseInline(admin.TabularInline):
    model = CassetteFrequencyResponse
    extra = 3


class CassettePriceInline(admin.TabularInline):
    model = CassettePrice
    extra = 3


class CassetteAdmin(admin.ModelAdmin):
    inlines = [CassetteImageInline, CassetteFrequencyResponseInline, CassettePriceInline]


admin.site.register(CassetteBrand)
admin.site.register(CassetteType)
admin.site.register(CassetteSeries)
admin.site.register(CassetteManufacturer)
admin.site.register(CassetteCollection)
admin.site.register(CassetteBarcode)
admin.site.register(CassetteFrequencyResponse)
admin.site.register(CassetteTapeLength)
admin.site.register(CassetteTechnology)
admin.site.register(CassetteModel)
admin.site.register(Cassette, CassetteAdmin)
admin.site.register(CassetteCategory)



