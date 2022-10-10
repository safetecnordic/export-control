import pprint
import string
import re
import PyPDF2
from django.core.management.base import BaseCommand, CommandError
from regulations.models import Category, SubCategory, Regime, Regulation, Paragraph


class Command(BaseCommand):
    """
    ./manage.py experiment_command
    """

    def handle(self, *args, **options):
        text = ""
        with open('paragraph4.txt',  'r', encoding="utf8" ) as f:
                while(True):    
                    line = f.readline()
                    if not line:
                        break
                    text += line


        node = dict()
        self._parse_one_paragraph(text, node)
        print(node)
            
        #pprint.pprint(node)

        #node["0A001"] = {"label":"a.", "parent": None, "text": "Ciao", "children": [{},{} ]}

    def _parse_one_paragraph(self, paragraph, node):
        node["text"] = ""
        lines = paragraph.split("\n")
        node["children"] = list()
        i = 0
        indent = self.count_space(lines[0])
        while i < len(lines):
            line = lines[i]
            indent = self.count_space(line)
            line = lines[i].strip()
            if self.is_item(line):  
                sep = line.strip().index(".")
                child_node = dict()
                label = line.strip()[:sep]
                child_node["label"] = label
                node["children"].append(child_node)
                #child_node["parent"] = node
                end_index = len(paragraph)
                new_indent = indent
                if i == len(lines) -1:
                    end_index = len(paragraph)
                    i += 1
                for j in range(i+1, len(lines)):
                    line2 = lines[j]
                    i += 1
                    if self.is_item(line2) or self.is_note(line2) or self.is_nb(line2):
                        new_indent = self.count_space(line2)
                        if ((self.is_item(line2) and self.is_next_item(label, line2) and new_indent <= indent)  or (self.is_note(line2) or self.is_nb(line2) ) and new_indent <= indent):
                            end_index = paragraph.index(line2)
                            break  
                        elif j == len(lines)-1:
                            end_index = len(paragraph)
                            i += 1  
                    else:
                        if j == len(lines)-1:
                            end_index = len(paragraph)
                            i += 1  
                        
                start = paragraph.index(line)+sep+1
                self._parse_one_paragraph(paragraph[start:end_index], child_node)
            elif self.is_note(line) or self.is_nb(line):#if a line is a start of node parse the wholde note, does not 
                #find label part f. ex. Note 1, N.B.,...
                sep =  line.strip().index(":") if self.is_note(line) else line.strip().index(" ")
                child_node = dict()
                child_node["label"] = line.strip()[:sep]
                node["children"].append(child_node)
                #child_node.parent = node
                end_index = len(paragraph)
                new_indent = indent

                # find the index where the note is finished
                if i == len(lines) -1:
                    end_index = len(paragraph)
                    i += 1
                for j in range(i+1, len(lines)):
                    line2 = lines[j]
                    i += 1
                    if self.is_note(line2) or self.is_nb(line2):  # if new note, så er vi ferdig her
                        end_index = paragraph.index(line2)
                        break
                    elif self.is_item(line2):
                        new_indent = self.count_space(line2)
                        if new_indent <= indent: # manuel change of forskrift to pass this condition
                            end_index = paragraph.index(line2) 
                            break  
                        elif j == len(lines)-1:
                            end_index = len(paragraph)
                            i += 1  
                    else:
                        if j == len(lines)-1:
                            end_index = len(paragraph)
                            i += 1  
                        
                start = paragraph.index(line)+sep+1
                child_node["text"] = paragraph[start:end_index]
            else:
                node["text"] += " " + line #text fortsetter
                i += 1


    def is_letter_item(self, line):
        return bool(re.search("^[ ]*[a-z][.]", line)) 
        

    def is_number_item(self, line):
        return bool(re.search("^[ ]*[0-9]+[.]", line))

    def is_item(self, line):
        return self.is_letter_item(line) or self.is_number_item(line)

    def is_next_item(self, label, line):
        if not self.is_item(line):
            return False
        sep = line.strip().index(".")
        line_label = line.strip()[:sep]
        if label.isdigit() and line_label.isdigit():
            if int(line_label)-int(label) == 1:
                return True
            if (int(label) == 1 and line_label.is_alpha()) or (label == 'a' and line_label.is_digit()):
                return True
        if label.isalpha() and line_label.isalpha():
            if ord(line_label.strip()[0])-ord(label.strip()[0]) == 1:
                return True
        return False


    def count_space(self, str):
        # counter
        count = 0
        for i in str:
            if i == " ":
                count += 1   
            else:
                break
        return count

    def is_note(self, line):
        """
        Determines whether the text line is a start of a Note
        """
        note = bool(re.search("^[ ]*Note[ ]*[0-9]*:", line)) \
        or bool(re.search("^[ ]*N.B.:", line)) \
        or  bool(re.search("^[ ]*Technical Note[ ]*[0-9]*:", line)) 
        return note

    def is_nb(self, line):
        return  bool(re.search("^[ ]*N.B.[ ]*[0-9]*", line))

