import re
from PyPDF2 import PdfFileReader
from regulations.models import  Category, SubCategory, Regime, Regulation
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        patt = "[0-9][A-E][0-9]{3}"
        text = ''
        with open('Forskrift.pdf', 'rb') as f:
            matches = set()
            reader = PdfFileReader(f)
            #pages = reader.numPages
            for page in range(24,248):
                page_obj = reader.getPage(page)
                page_text = page_obj.extractText()
                text += process_page_text(page_text) + "\n"
                matches.update(set(x for x in re.findall(patt, text))) 
        matches = list(matches)
        matches.sort()
 

        # remove part 1, part 2 texts
        text = text[:text.index("Part 1 - TELECOMMUNICATIONS")] + text[text.index("5A001"):]
        text = text[:text.index('Part 2 - "INFORMATION SECURITY"')] + text[text.index("ractices of the supplier")+25:]
        i = 0
        paragraphs = list()

        index5 = matches.index("5A001")
        matches[index5+1] = "5A101"
        matches[index5+2] = "5B001"
        matches[index5+3] = "5D001"
        matches[index5+4] = "5D101"
        matches[index5+5] = "5E001"
        matches[index5+6] = "5E101"
        matches[index5+7] = "5A002"
        matches[index5+8] = "5A003"
        matches[index5+9] = "5A004"
        matches[index5+10] = "5B002"
        matches[index5+11] = "5D002"
        matches[index5+12] = "5E002"

        for i in range(len(matches) - 1):
            start = text.index(matches[i] + "\x20")
            end = text.index(matches[i+1] + "\x20")
            par_text = text[start:end].strip()
            if par_text[-5:].__contains__("None"):
                par_text = par_text[:-5]
            paragraphs.append(par_text)
            text = text[end:]
        paragraphs.append(text)
        #print(paragraphs[228])

        #create dictionary from paragraphs
        paragraphs_dict = dict()
        for par in paragraphs:
            par_key = par[:5]
            par_val = par[5:]
            paragraphs_dict[par_key] = par_val
        
        print(paragraphs_dict["1B115"])


    
def process_page_text(page_text):
    lines = page_text.split("\n")[2:]
    for line in lines:
        if (line.__contains__("continued") and bool(re.search("[0-9][A-E][0-9]{3}", line))) \
        or bool(re.search("CATEGORY", line)) \
        or bool(re.search("[0-9][A-E]", line[:3])) and not bool(re.search("[0-9][A-E][0-9]{3}", line[:6])) \
        or line.__contains__("None."): 
                lines.remove(line)
    return "\n".join(lines)


def parse_one_paragraph(par_key, par_val):
    pass
