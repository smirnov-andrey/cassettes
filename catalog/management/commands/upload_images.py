import os
import pyexcel

from pyexcel_ods3 import get_data
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from catalog.models import *


class Command(BaseCommand):
    help = 'Upload images to catalog'
    # category = Category.objects.get(pk=1)

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'upload_data')
        book = pyexcel.get_book(
            file_name=os.path.join(data_dir, 'all_products_mapped.ods'))
        sheet = book['all_products']
        sheet.name_columns_by_row(0)

        for row in range(0, 15421):
            print(f'================== ROW: {row + 2}  ==================')

            product_pngs_cell = sheet[row, 'product_pngs'].strip()
            cassette = Cassette.objects.get(pk=int(sheet[row, 'cassette_id']))
            if product_pngs_cell != '':
                image_paths = product_pngs_cell.split(',')
                has_cover = False
                for path in image_paths:
                    _, _, folder, file = path.split('/')
                    src_path = os.path.join(settings.BASE_DIR,
                                            'upload_data',
                                            'photos',
                                            folder,
                                            file)
                    if os.path.exists(src_path) and os.path.isfile(src_path):
                        with open(src_path, 'rb') as f:
                            image_object = Image()
                            image_object.cassette = cassette
                            image_object.image.save(name=file,
                                                    content=File(f),
                                                    save=True)
                            if not has_cover:
                                image_object.is_cover = True
                                image_object.view = 1
                                image_object.save()
                                has_cover = True
                        os.remove(src_path)
                src_path = os.path.join(settings.BASE_DIR, 'upload_data',
                                        'photos', folder)
                try:
                    os.rmdir(src_path)
                except OSError:
                    print('Dir not empty:', src_path)
        pyexcel.free_resources()
