import re
import PyPDF2
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
        self._setup_initial_data()
        self._import_data(options["file"])
        self.stdout.write(self.style.SUCCESS("FINISH"))

    def _setup_initial_data(self):
        Category.objects.create(identifier="Cat0")
        Category 0 – Nuclear materials, facilities and equipment 
        Category1 – Special materials and related equipment
        Category 2 – Materials processing
        Category 3 – Electronics
        Category 4 – Computers
        Category 5 – Telecommunications and «information security»
        Part 1 – Telecommunications  
        Part 2 – «information security» 
        Category 6 – Sensors and lasers
        Category 7 – Navigation and avionics  
        Category 8 – Marine
        Category 9 – Aerospace and propulsion 
    def _import_data(self, file_name):
        self.stdout.write("Start reding PDF")
        pdf_obj = open(file_name, "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf_obj)

        for page_number in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_number)
            print(page.extractText())
        pdf_obj.close()
