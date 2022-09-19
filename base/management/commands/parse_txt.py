import re
from regulations.models import  Category, SubCategory, Regime, Regulation
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        patt = "[0-9][A-E][0-9]{3}"
        text = ''
        page_num = 25
        with open('Forskrift.txt',  'r', encoding="utf8" ) as f:
            matches = set()
            while(True):    
                line = f.readline()
                if not line:
                    break
                if line.strip() == str(page_num):
                    page_num += 1
                elif (line.__contains__("continued") \
                    and bool(re.search("[0-9][A-E][0-9]{3}", line))) \
                    or len(line.strip()) == 0 \
                    or bool(re.search("CATEGORY", line)) \
                    or bool(re.search("[0-9][A-E]", line[:3])) and not bool(re.search("[0-9][A-E][0-9]{3}", line[:6])) \
                    or line.__contains__("None."): 
                    continue
                else:
                    text += line
                    matches.update(set(x for x in re.findall(patt, text))) 

        matches = list(matches)
        matches.sort()
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

        i = 0
        paragraphs = list()

        for i in range(len(matches) - 1):
            start = text.index(matches[i] + "\x20")
            end = text.index(matches[i+1] + "\x20")
            par_text = text[start:end].strip()
            if par_text[-5:].__contains__("None"):
                par_text = par_text[:-5]
            paragraphs.append(par_text)
            text = text[end:]
        paragraphs.append(text)

        #create dictionary from paragraphs
        paragraphs_dict = dict()
        for par in paragraphs:
            par_key = par[:5]
            par_val = par[5:]
            paragraphs_dict[par_key] = par_val
        
        paragraph = paragraphs_dict["5B001"]

        
        node = parse_one_paragraph(paragraph)
        print(node.text)

def parse_one_paragraph(paragraph, indent = 0):
    node = Node()
    lines = paragraph.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        #find out indent
        if bool(re.search("^[ ]*[a-z][.]", line)) or bool(re.search("^[ ]*[0-9]+[.]", line)):
            child_node = Node()
            dot = line.strip().index(".")
            #child_node.label = line.strip()[:dot+1]
            #node.children[line.strip()[:dot]] = child_node
            end_index = len(paragraph)-1
            new_indent = indent
            for j in range(i+1, len(lines)):
                line = lines[j]
                i += 1
                if bool(re.search("^[ ]*[a-z][.]", line)) or bool(re.search("^[ ]*[0-9]+[.]", line)):
                    new_indent = count_space(line)
                    if new_indent <= indent:
                        end_index = paragraph.index(line)
                        break   
            node.children[line.strip()[:dot]] = parse_one_paragraph(paragraph[paragraph.index(line)+dot+1+new_indent:end_index], new_indent)
            #parse_one_paragraph(child_paragraph, child_node, new_indent)
        # if new level starts: a., 1., or (N.B.//Note//Techical note and indent > curent indent)
        # node.text += line #if not new indent level just continue writinng the text to the node
        else:
            node.text += line #text fortsetter
            i += 1
    return node


class Node:

   def __init__(self):
        self.parent= None
        self.label = "" #for the root label
        self.children = dict()
        self.text = ""

    
def count_space(str):
    # counter
    count = 0
    for i in str:
        if i == " ":
            count += 1   
        else:
            break
    return count