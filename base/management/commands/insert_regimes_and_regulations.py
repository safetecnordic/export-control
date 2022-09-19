import re
from PyPDF2 import PdfFileReader
from regulations.models import  Category, SubCategory, Regime, Regulation
from django.core.management.base import BaseCommand, CommandError

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
            category = m[0:1]
            subcategory = m[1:2]
            regime = m[2:]
            Regime.objects.get_or_create(identifier=regime)
            # in regulation we need id fields
            Regulation.objects.get_or_create(category = Category.objects.get(identifier=int(category)), 
                                            sub_category = SubCategory.objects.get(identifier = subcategory),
                                            regime = Regime.objects.get(identifier = regime))
   # return matches