import re
import pprint


def main():
    text = ""
    with open('DEMOadjusted.txt',  'r', encoding="utf8" ) as f:
            while(True):    
                line = f.readline()
                if not line:
                    break
                text += line

    node = dict()
    parse_one_paragraph(text, node)
    # print(node)

    pprint.pprint(node)

#node["0A001"] = {"label":"a.", "parent": None, "text": "Ciao", "children": [{},{} ]}

def parse_one_paragraph(paragraph, node):
    """
    Parses one paragraph (str) into a tree structure at point 'node'
    """
    node["text"] = ""
    lines = paragraph.split("\n")
    node["children"] = list()
    i = 0
    indent = count_space(lines[0])
    while i < len(lines): #For every line in the document
        line = lines[i]
        indent = count_space(line)
        line = lines[i].strip()
        if is_item(line): #If line is a bullet-point like "4. blabla" or "c. blabla"
            sep = line.strip().index(".")
            child_node = dict()
            label = line.strip()[:sep] #ex "5" or "c"
            child_node["label"] = label
            node["children"].append(child_node)
            
            end_index = len(paragraph)
            new_indent = indent

            if i == len(lines) -1:
                end_index = len(paragraph)
                i += 1
            for j in range(i+1, len(lines)):
                line2 = lines[j]
                i += 1
                if is_item(line2) or is_note(line2) or is_nb(line2): #If line is {5. bla}, {c. bla}, {Note: bla} or {NB: bla}
                    new_indent = count_space(line2)
                    if ((is_item(line2) and is_next_item(label, line2)) or is_note(line2) or is_nb(line2)): 
                        #subpoint ex. {5. 6.} or {a. b.} or {Note:}
                        if(new_indent <= indent):
                            end_index = paragraph.index(line2)
                            break  
                        else: #if new_indent > indent. Can fill in here.
                            #end_index = paragraph.index(line2) here we dont care about this last condition.
                            break
                    elif j == len(lines)-1: #set end_index
                        end_index = len(paragraph)
                        i += 1
                else: #if line does not have identificator. basically if this line is from the previous line.
                    if j == len(lines)-1:
                        end_index = len(paragraph)
                        i += 1  
            #Parse this paragraph that we have found, into the tree.
            start = paragraph.index(line)+sep+1
            parse_one_paragraph(paragraph[start:end_index], child_node)

        elif is_note(line) or is_nb(line): #If it is a note or NB, but not a bulletpoint.
            #if a line is a start of node parse the whole note, does not find label part f. ex. Note 1, N.B.,...
            sep =  line.strip().index(":") if is_note(line) else line.strip().index(" ")
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
                if is_note(line2) or is_nb(line2):  # if new note, så er vi ferdig her
                    end_index = paragraph.index(line2)
                    break
                elif is_item(line2):
                    new_indent = count_space(line2)
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


def is_letter_item(line):
    """returns true if the line is a letter bullet-point"""
    return bool(re.search("^[ ]*[a-z][.]", line))


def is_number_item(line):
    """returns true if line is a number bullet-point"""
    return bool(re.search("^[ ]*[0-9]+[.]", line))


def is_item(line):
    """returns true if line is a bullet-point, ex. 'a. blabla' or 'b. blabla' """
    return is_letter_item(line) or is_number_item(line)


def count_space(str):
    """Returns the amount of blank_spaces in the beginning of string"""
    count = 0
    for i in str:
        if i == " ":
            count += 1   
        else:
            return count


def is_next_item(label, line):
    """returns true if next line is a next point, given the current label. 
    ex. 1. 2.
    or c. d.
    """
    if not is_item(line):
        return False
    sep = line.strip().index(".")
    line_label = line.strip()[:sep]  #frem til separation
    if label.isdigit() and line_label.isdigit():
        if int(line_label)-int(label) == 1:  #hvis det er neste tall bullet-punkt
            return True
        if (int(label) == 1 and line_label.isalpha()) or (label == 'a' and line_label.is_digit()):  #.isalpha .
            return True #sjekker vel her om neste linje er et bullet_punkt.
    if label.isalpha() and line_label.isalpha():  #hvis alfabet-punktene er 1 fra hverandre, eks b og c => true.
        if ord(line_label.strip()[0])-ord(label.strip()[0]) == 1:
            return True
    return False


def is_note(line):
    """returns true if line is a start of a Note"""
    note = bool(re.search("^[ ]*Note[ ]*[0-9]*:", line)) \
    or bool(re.search("^[ ]*N.B.:", line)) \
    or  bool(re.search("^[ ]*Technical Note[ ]*[0-9]*:", line)) 
    return note


def is_nb(line):
    """returns true if line is a start of a N.B. """
    return bool(re.search("^[ ]*N.B.[ ]*[0-9]*", line))


if __name__ == "__main__":
    main()
