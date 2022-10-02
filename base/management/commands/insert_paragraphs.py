from cProfile import label
from cgitb import text
import re
from django.core.management.base import BaseCommand
from regulations.models import Paragraph, Regime, Regulation, SubCategory
from base.utils import get_values_from_paragraph_name

class Command(BaseCommand):

    def handle(self, *args, **options):
        paragraphs_dict = self._create_paragraphs_dictionary()
        #print(paragraphs_dict["5A003"])
        # TODO: parse all paragraphs into the dictionary
        par_key = "6A005"
        paragraph = paragraphs_dict[par_key]
        # creeate dictionary from the paragraph
        node = dict()
        self._parse_one_paragraph(paragraph, node)
        self._insert_node_into_db(node, par_key)
        

    
    def _insert_node_into_db(self, node, par_key=None, regulation = None,  parent=None, order=0):
        # regime from the par_key, if par_key is None then there is a parent id
        # if the regulation is None, it means we have not found it yet, bcs it is an upper level paragraph, 
        # specified by par_key string, i.e. '0A001'
        # after we found it we can pass it to the paragraphs children
        # order is 0 by default
        # parent is the id of parent paragraph, we get it after inserting into the db
        if regulation is None:
            # here we will find the root level regulation
            # find the reguation based on the par_key
            category_id, subcategory, regime_number, regime_name = get_values_from_paragraph_name(par_key)
            regulation = Regulation.objects.get(category = category_id,
                                            sub_category = SubCategory.objects.get(identifier = subcategory),
                                            regime_number = regime_number, 
                                            regime = Regime.objects.filter(name = regime_name).first())  
        # first insert the node itself
        note = True if ("label" in node) and (self.is_nb(node["label"]) or self.is_note(node["label"]+":")) else False      
        label = node["label"] if ("label" in node) else None                       
        paragraph, _ = Paragraph.objects.get_or_create(text=node["text"], order = order, note = note, parent = parent, regulation = regulation, label = label)
        # insert all of the children if they exist 
        if "children" in node:
            children_nodes = node["children"]
            for i in range(len(children_nodes)):
                self._insert_node_into_db(node = children_nodes[i], regulation=regulation, parent=paragraph, order = i)
        

           

    def _create_paragraphs_dictionary(self):
        """
        creates the dictionary with paragraphs where the key is regulation, e. g. "1A001" and the value is the whole text of the paragraph
        """
        patt = "[0-9][A-E][0-9]{3}"
        text = ''
        page_num = 25
        with open('DEMOforskrift.txt',  'r', encoding="utf8" ) as f:
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
        
        return paragraphs_dict

    
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
                    new_indent = self.count_space(line2)
                    i += 1
                    if (self.is_note(line2) or self.is_nb(line2)) and new_indent <= indent:  # if new note, så er vi ferdig her, but not if indented note
                        end_index = paragraph.index(line2)
                        break
                    elif self.is_item(line2):
                        #new_indent = self.count_space(line2)
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
            if (int(label) == 1 and line_label.isalpha()) or (label == 'a' and line_label.is_digit()):
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
        or  bool(re.search("^[ ]*Technical Note[ ]*[0-9]*:", line)) \
        or  bool(re.search("^[ ]*Technical Notes[ ]*[0-9]*:", line))     
        return note

    def is_nb(self, line):
        return  bool(re.search("^[ ]*N.B.[ ]*[0-9]*", line))