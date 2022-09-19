import re
from PyPDF2 import PdfFileReader
from django.core.management.base import BaseCommand, CommandError
from regulations.models import Category, SubCategory, Regime, Regulation


class Command(BaseCommand):
    """
    ./manage.py import_data_from_pdf  --file=test.pdf
    """

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str)
        parser.add_argument(
            "--flush",
            type=bool,
            default=False,
            help="Indicates whether to delete all data from the database",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("START"))
        print(options["file"])
        print(options["flush"])
        self._import_data()
        self.stdout.write(self.style.SUCCESS("FINISH"))

    def _import_data(self):
        self.stdout.write("Start reding PDF")
