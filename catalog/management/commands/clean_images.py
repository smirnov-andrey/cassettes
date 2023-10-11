from django.core.management.base import BaseCommand

from catalog.models import *


class Command(BaseCommand):
    help = 'Clean data from catalog'

    def handle(self, *args, **options):
        Image.objects.all().delete()