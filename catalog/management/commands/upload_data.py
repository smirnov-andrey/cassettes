import os
import pyexcel

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catalog.models import *


class Command(BaseCommand):
    help = 'Upload data to catalog'
    category = Category.objects.get(pk=1)

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'upload_data')
        book = pyexcel.get_book(file_name=os.path.join(data_dir, 'all_products.ods'))
        sheet = book['all_products']
        sheet['P1'] = 'cassette_id'
        sheet['Q1'] = 'cassette_uuid'
        sheet.name_columns_by_row(0)

        brands = dict()
        manufactures = dict()
        models = dict()
        sorts = dict()
        tape_types = dict()
        tape_lengths = dict()
        countrys = dict()
        for row in range(0, 15421):
            brand = sheet[row, 'brand'].strip()
            manufacture = sheet[row, 'manufacture'].strip()
            model = sheet[row, 'model'].strip()
            series = sheet[row, 'series'].strip()
            sort = sheet[row, 'sort'].strip()
            tape_type = sheet[row, 'tape_type'].strip()
            tape_length = str(sheet[row, 'tape_length']).strip()
            release_year = sheet[row, 'release_year']
            country = sheet[row, 'country'].strip()
            market = sheet[row, 'market'].strip()
            if brand == '':
                brand = None
            else:
                if brand not in brands:
                    object, x = CassetteBrand.objects.get_or_create(
                        title=brand
                    )
                    brands[brand] = object
                    self.category.brands.add(object)
                    brand = object
                else:
                    brand = brands[brand]

            if manufacture == '':
                manufacture = None
            else:
                if manufacture not in manufactures:
                    object, _ = CassetteManufacturer.objects.get_or_create(
                        title=manufacture
                    )
                    manufactures[manufacture] = object
                    manufacture = object
                else:
                    manufacture = manufactures[manufacture]

            if model == '':
                model = None
            else:
                if f'{brand.title}/{model}' not in models:
                    object, _ = CassetteModel.objects.get_or_create(
                        brand=brand,
                        title=model,
                    )
                    models[f'{brand.title}/{model}'] = object
                    model = object
                else:
                    model = models[f'{brand}/{model}']

            if sort == '':
                sort = None
            else:
                if sort not in sorts:
                    object, _ = CassetteSort.objects.get_or_create(
                        title=sort
                    )
                    sorts[sort] = object
                    sort = object
                else:
                    sort = sorts[sort]

            if tape_type == '':
                tape_type = None
            else:
                if tape_type not in tape_types:
                    object, _ = CassetteType.objects.get_or_create(
                        title=tape_type
                    )
                    tape_types[tape_type] = object
                    tape_type = object
                else:
                    tape_type = tape_types[tape_type]

            if tape_length == '':
                tape_length = None
            else:
                if tape_length not in tape_lengths:
                    object, _ = CassetteTapeLength.objects.get_or_create(
                        tape_length=tape_length
                    )
                    tape_lengths[tape_length] = object
                    tape_length = object
                else:
                    tape_length = tape_lengths[tape_length]

            if release_year == '':
                release_year = None
            else:
                release_year = int(release_year)

            if country == '':
                country = None
            else:
                if country not in countrys:
                    object, _ = Country.objects.get_or_create(
                        title=country
                    )
                    countrys[country] = object
                    country = object
                else:
                    country = countrys[country]

            cassette, cas_crated = Cassette.objects.get_or_create(
                coil=False,
                slim_case=False,
                category=self.category,
                brand=brand,
                tape_type=tape_type,
                model=model,
                manufacturer=manufacture,
                series=None,
                sort=sort,
                tape_length=tape_length,
                year_release=release_year,
                country=country,
                upload_row=row+2,
            )
            if not cas_crated:
                print('Warning cassete dublicate:', cassette.__repr__(),
                      cassette.id, cassette.brand, cassette.model)
            sheet[row, 'cassette_id'] = str(cassette.id)
            sheet[row, 'cassette_uuid'] = str(cassette.uuid)

            if cas_crated and market != '':
                market = market.split('/')
                for index in range(len(market)):
                    market_obj, _ = Country.objects.get_or_create(
                        title=market[index]
                    )
                    cassette.markets.add(market_obj)

        sheet.save_as(filename=os.path.join(data_dir,
                                            'all_products_mapped.ods'))
        pyexcel.free_resources()
