from PyPDF2 import PdfFileReader
import re
from regulations.models import Category

with open("Forskrift.pdf", "rb") as f:
    reader = PdfFileReader(f)
    contents = reader.getPage(1).extractText()

    index1 = contents.index("CATEGORY 0")
    index2 = contents.index("2020")
    step0 = contents[index1:index2]
    step1 = step0.split("\n")[:-1]

    categories = list()
    for line in step1:
        line = re.split("[–]|[-]", line)
        if "CATEGORY" in line[0]:
            line[0] = "".join(c for c in line[0] if c.isdigit())
            line[1] = "".join(c for c in line[1] if c.isalpha() or c == " ")
            line[1] = line[1].strip()
            categories.append(line)

    for line in categories:
        Category.objects.get_or_create(identifier=line[0], name=line[1])

    # print(categories)

    # test branch remote
