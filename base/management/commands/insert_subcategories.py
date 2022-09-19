from regulations.models import SubCategory
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        SubCategory.objects.get_or_create(identifier="A", name = "Systems, Equipment and Components")
        SubCategory.objects.get_or_create(identifier="B", name = "Test, Inspection and Production Equipment")
        SubCategory.objects.get_or_create(identifier="C", name = "Materials")
        SubCategory.objects.get_or_create(identifier="D", name = "Software")
        SubCategory.objects.get_or_create(identifier="E", name = "Technology (technical assistance and technical data)")