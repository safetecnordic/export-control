from regulations.models import Regime
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        Regime.objects.get_or_create(name="Wassenaar Arrangement", number_range_min = 1, number_range_max = 99)
        Regime.objects.get_or_create(name="Missile Technology Control Regime", number_range_min = 101, number_range_max = 199)
        Regime.objects.get_or_create(name="Nuclear Suppliers Group", number_range_min = 201, number_range_max = 299)
        Regime.objects.get_or_create(name="Australia Group", number_range_min = 301, number_range_max = 399)
        Regime.objects.get_or_create(name="Chemical Weapons Convention", number_range_min = 401, number_range_max = 499)