import re
from PyPDF2 import PdfFileReader
from regulations.models import  Category, SubCategory, Regime, Regulation
from django.core.management.base import BaseCommand, CommandError
from base.utils import get_values_from_paragraph_name

class Command(BaseCommand):

    def handle(self, *args, **options):
        patt = "[0-9][A-E][0-9]{3}"
        with open('Forskrift.pdf', 'rb') as f:
            matches = set()
            text = ''
            reader = PdfFileReader(f)
            pages = reader.numPages
            for page in range(pages):
                page_obj = reader.getPage(page)
                text += '\n' + page_obj.extractText()
                matches.update(set(x for x in re.findall(
                patt, text)))

        for m in matches:
            category_id, subcategory, regime_number, regime_name = get_values_from_paragraph_name(m)
            Regulation.objects.get_or_create(category = category_id,
                                            sub_category = SubCategory.objects.get(identifier = subcategory),
                                            regime_number = regime_number, 
                                            regime = Regime.objects.filter(name = regime_name).first())