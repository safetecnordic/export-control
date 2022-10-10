import re
def main():
    text = ""
    with open('paragraph2.txt',  'r', encoding="utf8" ) as f:
            while(True):    
                line = f.readline()
                if not line:
                    break
                text += line
    node = Node()
    parse_one_paragraph(text, node)
    #print(node.text)
    print(node.children)


def parse_one_paragraph(paragraph, node, indent = 0):
    lines = paragraph.split("\n")
    i = 0
    indent = count_space(lines[0])
    while i < len(lines):
        line = lines[i]
        if is_item(line) or is_note(line) or is_nb(line):
            cur_item = line
            indent = count_space(line)
            child_node = Node()
            if is_item(line):
                sep = line.strip().index(".")
            elif is_note(line):
                sep = line.strip().index(":")
            else: #is NB
                sep = line.strip().index(" ")
            child_node.label = line.strip()[:sep]
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
                    if new_indent <= indent: # TODO: change this condition, dritt i å break hvis det er neste item
                        end_index = paragraph.index(line2)
                        break  
                    elif j == len(lines)-1:
                        end_index = len(paragraph)
                        i += 1  
                    cur_item = line2
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

regulations = list()
node = dict()

node["0A001"] = {"id":"a.", "parent": None, "text": "Ciao", "children": [{},{} ]}
regulations.append(node["0A001"])

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

def is_item_node(node):
    return bool(re.search("^[a-z]", node.label)) or bool(re.search("^[0-9]+", node.label))

def is_nb(line):
    return  bool(re.search("^[ ]*N.B.[ ]*[0-9]*", line))

def is_note_node(node):
    return bool(re.search("^[ ]*Note[ ]*[0-9]*", node.label)) \
    or bool(re.search("^[ ]*N.B.", node.label)) \
    or  bool(re.search("^[ ]*Technical Note[ ]*[0-9]*", node.label))  \
    or  bool(re.search("^[ ]*N.B.[ ]*[0-9]*", node.label))

def is_next_item(line1, line2):
    # check if line2 contains next item after line2
    if is_item(line1) and is_item(line2):
        label1 = line1[:line1.index(".")].strip()
        label2 = line2[:line2.index(".")].strip()
        if label1.isdigit() and label2.isdigit():
            if int(label2)-int(label1) == 1:
                return True
        if label1.isalpha() and label2.isalpha():
            if ord(label2.strip()[0])-ord(label1.strip()[0]) == 1:
                return True
    return False


if __name__ == "__main__":
    main()

