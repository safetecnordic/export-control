from django.core.management.base import BaseCommand
from regulations.utils import set_postgres_search_config


class Command(BaseCommand):
    def handle(self, *args, **options):
        set_postgres_search_config()
