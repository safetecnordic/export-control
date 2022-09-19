import re
from PyPDF2 import PdfFileReader
from regulations.models import Category
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        Category.objects.get_or_create(identifier=0, name = "NUCLEAR MATERIALS FACILITIES AND EQUIPMENT")
        Category.objects.get_or_create(identifier=1, name = "SPECIAL MATERIALS AND RELATED EQUIPMENT")
        Category.objects.get_or_create(identifier=2, name = "MATERIALS PROCESSING")
        Category.objects.get_or_create(identifier=3, name = "ELECTRONICS")
        Category.objects.get_or_create(identifier=4, name = "COMPUTERS")
        Category.objects.get_or_create(identifier=5, name = "TELECOMMUNICATIONS AND INFORMATION SECURITY")
        Category.objects.get_or_create(identifier=6, name = "SENSORS AND LASERS")
        Category.objects.get_or_create(identifier=7, name = "NAVIGATION AND AVIONICS")
        Category.objects.get_or_create(identifier=8, name = "MARINE")
        Category.objects.get_or_create(identifier=9, name = "AEROSPACE AND PROPULSION")