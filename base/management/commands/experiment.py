import re
def main():
    text = ""
    with open('paragraph.txt',  'r', encoding="utf8" ) as f:
            while(True):    
                line = f.readline()
                if not line:
                    break
                text += line
    node = Node()
    parse_one_paragraph(text, node)
    print(node.children["b"].children["5"].text)


def parse_one_paragraph(paragraph, node, indent = 0):
    lines = paragraph.split("\n")
    i = 0
    indent = count_space(lines[0])
    while i < len(lines):
        line = lines[i]
        if is_item(line) or is_note(line):
            indent = count_space(line)
            child_node = Node()
            if is_item(line):
                sep = line.strip().index(".")
            else:
                sep = line.strip().index(":")
            child_node.label = line.strip()[:sep+1]
            node.children[line.strip()[:sep]] = child_node
            child_node.parent = node
            end_index = len(paragraph)-1
            new_indent = indent
            if i == len(lines) -1:
                end_index = len(paragraph)
                i += 1
            for j in range(i+1, len(lines)):
                line2 = lines[j]
                i += 1
                if is_item(line2):
                    new_indent = count_space(line2)
                    if new_indent <= indent:
                        end_index = paragraph.index(line2)
                        break   
                    elif j == len(lines)-1:
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
    note = bool(re.search("^[ ]*Note[ ]*[0-9]*:", line)) or bool(re.search("^[ ]*N.B.:", line))
    return note

if __name__ == "__main__":
    main()

