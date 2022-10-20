import string
import re
from django.core.management.base import BaseCommand
from regulations.models import Category, SubCategory, Regime, Regulation, Paragraph


class Command(BaseCommand):
    """
    To run the command:
    `python manage.py import_data_from_pdf --file=regulations/static/export-control.txt --flush=True`

    To dump imported data to `regulations.json`:
    `python manage.py dumpdata regulations > regulations.json`
    """

    TOP_SEQUENCE = ". ".join([*string.ascii_lowercase]).split()
    LOW_SEQUENCE = ". ".join(map(str, range(99 + 1))).split()

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
        if options["flush"]:
            self.stdout.write(self.style.ERROR("DELETE ALL"))
            self._delete_all()
        self._setup_initial_data()
        self._import_data(options["file"])
        self.stdout.write(self.style.SUCCESS("FINISH"))

    def _delete_all(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Regime.objects.all().delete()
        Regulation.objects.all().delete()
        Paragraph.objects.all().delete()

    def _setup_initial_data(self):
        self._create_category()
        self._create_sub_category()
        self._create_regime()

    def _import_data(self, file_name):
        self.stdout.write("Start file")
        with open(file_name) as file:
            lines = file.readlines()
            regulation = None
            parent_paragraph = None
            for line in lines:
                print(line)
                first_word = line.split()[0] if len(line.split()) > 0 else ""
                if self._is_line_to_skip(first_word):
                    continue
                elif self.is_regulation(first_word):
                    if "continued" in line:
                        continue
                    regulation = self._create_regulation(first_word, line)
                    parent_paragraph = regulation.get_last_paragraph()
                elif self.is_paragraph(first_word):
                    note_type = "base"
                    if self.is_first_level_paragraph(line):
                        if self.is_special_paragraph(first_word):
                            note_type = first_word
                        parent_first_level = self._create_paragraph(
                            regulation, line, note_type, first_word, parent_paragraph
                        )
                    elif self.is_second_level_paragraph(line):
                        if self.is_special_paragraph(first_word):
                            note_type = first_word
                        parent_second_level = self._create_paragraph(
                            regulation, line, note_type, first_word, parent_first_level
                        )
                    elif self.is_third_level_paragraph(line):
                        if self.is_special_paragraph(first_word):
                            note_type = first_word
                        parent_third_level = self._create_paragraph(
                            regulation, line, note_type, first_word, parent_second_level
                        )
                    elif self.is_fourth_level_paragraph(line):
                        if self.is_special_paragraph(first_word):
                            note_type = first_word
                        self._create_paragraph(regulation, line, note_type, first_word, parent_third_level)
                    else:
                        if regulation and regulation.get_last_paragraph():
                            paragraph = regulation.get_last_paragraph()
                            if first_word in self.TOP_SEQUENCE or first_word.startswith("Technical"):
                                paragraph.text += f"<br>{line}"
                            elif first_word in self.LOW_SEQUENCE:
                                paragraph.text += f"<br>&emsp;{line}"
                            else:
                                paragraph.text += f" {line}"
                            paragraph.save()
                else:
                    if regulation and regulation.get_last_paragraph():
                        paragraph = regulation.get_last_paragraph()
                        paragraph.text += f" {line}"
                        paragraph.save()

    def is_first_level_paragraph(self, line):
        return self.count_space(line) in range(7, 14)

    def is_second_level_paragraph(self, line):
        return self.count_space(line) in range(14, 21)

    def is_third_level_paragraph(self, line):
        return self.count_space(line) in range(21, 28)

    def is_fourth_level_paragraph(self, line):
        return self.count_space(line) in range(28, 35)

    def count_space(self, line):
        count = 0
        for char in line:
            if char == " ":
                count += 1
            else:
                break
        return count

    def is_regulation(self, first_word):
        value = False
        if len(first_word) == 5 and bool(re.match("[0-9][A-E][0-4][0-9][0-9]", first_word)):
            value = True
        return value

    def is_special_paragraph(self, first_word):
        value = False
        if first_word.startswith(("N.B.", "Note", "Technical")):
            value = True
        return value

    def is_paragraph(self, first_word):
        value = False
        if first_word in self.TOP_SEQUENCE or first_word in self.LOW_SEQUENCE or self.is_special_paragraph(first_word):
            value = True
        return value

    def _is_line_to_skip(self, first_word):
        if not first_word:
            return True
        if first_word.isdigit():
            return True
        if first_word.startswith(("CATEGORY",)):
            return True
        if len(first_word) == 2 and bool(re.match("[0-9][A-E]", first_word)):
            return True
        return False

    def _create_paragraph(self, regulation, line, note_type, first_word, paragraph_parent):
        text = " ".join(line.split()[1:])
        code = f"0{first_word}" if first_word in self.LOW_SEQUENCE[:10] else first_word
        if code == "Note":
            code = f"{code} {line.split()[1]}"
        if code.startswith("Technical"):
            code = f"{code} {line.split()[1]}"
        paragraph = paragraph_parent.add_child(
            regulation=regulation,
            text=text,
            code=code,
            note_type=note_type,
            category=regulation.category,
            sub_category=regulation.sub_category,
        )
        return paragraph

    def _create_regulation(self, first_word, line):
        part = None
        if first_word[0] == "5":
            part = 1
            if first_word in ["5A002", "5A003", "5A004", "5B002", "5D002", "5E002"]:
                part = 2
        category, new = Category.objects.get_or_create(identifier=first_word[0], part=part)
        sub_category, new = SubCategory.objects.get_or_create(identifier=first_word[1])

        regime = self._get_regime_from_code(first_word)
        regulation = Regulation.objects.create(
            category=category, sub_category=sub_category, regime=regime, code=first_word
        )
        text = " ".join(line.split()[1:])
        Paragraph.add_root(
            regulation=regulation,
            text=text,
            code=f"{regulation.__str__()}.",
            note_type="base",
            category=category,
            sub_category=sub_category,
        )
        return regulation

    def _create_category(self):
        Category.objects.create(identifier=0, name="Nuclear materials, facilities and equipment")
        Category.objects.create(identifier=1, name="Special materials and related equipment")
        Category.objects.create(identifier=2, name="Materials processing")
        Category.objects.create(identifier=3, name="Electronics")
        Category.objects.create(identifier=4, name="Computers")
        Category.objects.create(identifier=5, name="Telecommunications and Information security", part=1)
        Category.objects.create(identifier=5, name="Telecommunications and Information security", part=2)
        Category.objects.create(identifier=6, name="Sensors and lasers")
        Category.objects.create(identifier=7, name="Navigation and avionics")
        Category.objects.create(identifier=8, name="Marine")
        Category.objects.create(identifier=9, name="Aerospace and propulsion")

    def _create_sub_category(self):
        SubCategory.objects.create(identifier="A", name="Systems, equipment and components")
        SubCategory.objects.create(identifier="B", name="Test, inspection and production equipment")
        SubCategory.objects.create(identifier="C", name="Materials")
        SubCategory.objects.create(identifier="D", name="Software")
        SubCategory.objects.create(identifier="E", name="Tecnology (technical assistance and technical data)")

    def _create_regime(self):
        Regime.objects.create(number_range_min=0, number_range_max=99, name="Wassenaar Arrangement (WA)")
        Regime.objects.create(
            number_range_min=101, number_range_max=199, name="Missile Technology Control Regime (MTCR)"
        )
        Regime.objects.create(number_range_min=201, number_range_max=299, name="Nuclear Suppliers Group (NSG)")
        Regime.objects.create(number_range_min=301, number_range_max=399, name="Australia Group (AG)")
        Regime.objects.create(number_range_min=401, number_range_max=499, name="Chemical Weapons Convention (CWC)")

    def _get_regime_from_code(self, code):
        if code and len(code) == 5:
            regime_number = int(code[2:])
            return Regime.objects.filter(number_range_max__gte=regime_number).first()
        return None
