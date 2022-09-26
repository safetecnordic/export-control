import string
import re
import PyPDF2
from django.core.management.base import BaseCommand, CommandError
from regulations.models import Category, SubCategory, Regime, Regulation, Paragraph


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
        if options["flush"]:
            self.stdout.write(self.style.ERROR("DELETE ALL"))
            Category.objects.all().delete()
            SubCategory.objects.all().delete()
            Regime.objects.all().delete()
            Regulation.objects.all().delete()
            Paragraph.objects.all().delete()
            self.stdout.write(self.style.ERROR("DELETED ALL"))

        self._import_data(options["file"])
        self.stdout.write(self.style.SUCCESS("FINISH"))

    def _setup_initial_data(self):
        Category.objects.create(identifier=0, name="Nuclear materials, facilities and equipment")
        Category.objects.create(identifier=1, name="Special materials and related equipment")
        Category.objects.create(identifier=2, name="Materials processing")
        Category.objects.create(identifier=3, name="Electronics")
        Category.objects.create(identifier=4, name="Computers")
        Category.objects.create(identifier=5, name="Telecommunications and «information security»")
        Category.objects.create(identifier=6, name="Sensors and lasers")
        Category.objects.create(identifier=7, name="Navigation and avionics")
        Category.objects.create(identifier=8, name="Marine")
        Category.objects.create(identifier=9, name="Aerospace and propulsion")

        SubCategory.objects.create(identifier=1, name="Systems, equipment and components")
        SubCategory.objects.create(identifier=2, name="Test, inspection and production equipment")
        SubCategory.objects.create(identifier=3, name="Materials")
        SubCategory.objects.create(identifier=4, name="Software")
        SubCategory.objects.create(identifier=5, name="Tecnology (technical assistance and technical data)")

    def _import_data(self, file_name):
        self.stdout.write("Start reding PDF")
        """pdf_obj = open(file_name, "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf_obj)

        for page_number in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_number)
            print(page.extractText())
        pdf_obj.close()
        """

        top_sequence = ". ".join([*string.ascii_lowercase]).split()
        with open(file_name) as file:
            lines = file.readlines()
            for line in lines:
                first_word = line.split()[0]
                if bool(re.match("[1-9][A-E][0-4][0-9][0-9]", first_word)):
                    category, new = Category.objects.get_or_create(identifier=first_word[0])
                    sub_category, new = SubCategory.objects.get_or_create(identifier=first_word[1])
                    regime, new = Regime.objects.get_or_create(identifier=first_word[2:])
                    breakpoint()
                    regulation = Regulation.objects.create(category=category, sub_category=sub_category, regime=regime)
                    paragraph = Paragraph.objects.create(regulation=regulation)
                elif first_word in top_sequence:
                    paragraph = Paragraph.objects.create(regulation=regulation)
                else:
                    pass
                    # paragraph.update_text()

    def _get_empty_dict(parent=None, level=0, id=0) -> dict:
        return {
            "level": level,
            "id": id,
            "text": "",
            "children": [],
            "parent": parent,
        }

    def _prepare_datasource(d: dict, indent: int = 0) -> str:
        output = ""
        for node_pk, node_dict in d.items():
            for key, value in node_dict.items():
                if key == "children":
                    if value:
                        output += "'children' : [%s ]," % prepare_var_datasource_organigram(value, indent + 1)
                else:
                    if isinstance(value, str):
                        value = value.replace("'", "`")
                    output += "'%s': '%s'," % (key, value)
            output += "},{"
        output = "{%s}," % output.strip("},{")
        if indent == 0:
            output = "var datasource = %s;" % output.strip(",")
        return output


"""
lines = file.readlines()
for line in lines:
    first_character = line.split()[0]
    index = top_sequence.index(first_character) if first_character in top_sequence else -1
    if not index == -1:
        node = self._get_empty_dict(id=index)
        print("# create new node")
        # create new node
        pass
    else:
        print("# continue to add data")
        pass
    """
