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
        
        paragraph = paragraphs_dict["0B005"]

        node = Node()
        parse_one_paragraph(paragraph, node)
        print(node.children["Technical Note"].label)

def parse_one_paragraph(paragraph, node, indent = 0):
    lines = paragraph.split("\n")
    i = 0
    indent = count_space(lines[0])
    while i < len(lines):
        line = lines[i]
        if is_item(line) or is_note(line) or is_nb(line):
            indent = count_space(line)
            child_node = Node()
            if is_item(line):
                sep = line.strip().index(".")
            elif is_note(line):
                sep = line.strip().index(":")
            else: #is NB
                sep = line.strip().index(" ")
            child_node.label = line.strip()[:sep+1]
            node.children[line.strip()[:sep]] = child_node
            child_node.parent = node
            end_index = len(paragraph)
            new_indent = indent
            if i == len(lines) -1:
                end_index = len(paragraph)
                i += 1
            for j in range(i+1, len(lines)):
                line2 = lines[j]
                i += 1
                if is_item(line2) or is_note(line2) or is_nb(line2):
                    new_indent = count_space(line2)
                    if new_indent <= indent: #and ((is_note(line2) or is_nb(line2)) or line2.strip()[0]=="1" or  line2.strip()[0]=="a"): # TOOO
                        end_index = paragraph.index(line2)
                        break   
                    elif j == len(lines)-1:
                        end_index = len(paragraph)
                        i += 1  
                else:
                    if j == len(lines)-1:
                        end_index = len(paragraph)
                        i += 1  
            start = paragraph.index(line)+sep+1+indent
            parse_one_paragraph(paragraph[start:end_index], child_node, new_indent)
        else:
            node.text += line #text fortsetter
            i += 1



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

def is_item(line):
    return bool(re.search("^[ ]*[a-z][.]", line)) or bool(re.search("^[ ]*[0-9]+[.]", line))

def is_note(line):
    """
    Determines whether the text line is a start of a Note
    """
    note = bool(re.search("^[ ]*Note[ ]*[0-9]*:", line)) \
    or bool(re.search("^[ ]*N.B.:", line)) \
    or  bool(re.search("^[ ]*Technical Note[ ]*[0-9]*:", line)) 
    return note

def is_nb(line):
    return  bool(re.search("^[ ]*N.B.[ ]*[0-9]*", line))