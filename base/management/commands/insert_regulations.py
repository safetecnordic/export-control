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
            regime_number = int(m[2:])
            regime_name = "Wassenaar Arrangement"
            if regime_number / 100 == 1:
                regime_name = "Missile Technology Control Regime"
            elif regime_number / 100 == 2:
                regime_name = "Nuclear Suppliers Group"
            elif regime_number / 100 == 3:
                regime_name = "Australia Group"
            else:
                regime_name = "Chemical Weapons Convention"    
            
            # find out which part of category 5 the regulations belongs tp
            if category == "5" and subcategory + str(regime_number) in ["A2", "A3", "A4", "B2", "D2", "E2"]:
                category_id = category = Category.objects.filter(identifier=int(category), part = 2).first()
            elif category == "5":
                category_id = category = Category.objects.filter(identifier=int(category), part = 1).first()
            else: 
            # for other categories the identifier is unique
                category_id = category = Category.objects.filter(identifier=int(category)).first()
            Regulation.objects.get_or_create(category = category_id,
                                            sub_category = SubCategory.objects.get(identifier = subcategory),
                                            regime_number = regime_number, 
                                            regime = Regime.objects.filter(name = regime_name).first())