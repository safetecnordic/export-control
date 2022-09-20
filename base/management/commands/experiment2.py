import re
def main():
    text = ""
    with open('paragraph2.txt',  'r', encoding="utf8" ) as f:
            while(True):    
                line = f.readline()
                if not line:
                    break
                text += line


    node = dict()
    parse_one_paragraph(text, node)
    print(node["children"][1]["children"][2])

#node["0A001"] = {"label":"a.", "parent": None, "text": "Ciao", "children": [{},{} ]}

def parse_one_paragraph(paragraph, node):
    node["text"] = ""
    lines = paragraph.split("\n")
    node["children"] = list()
    i = 0
    indent = count_space(lines[0])
    while i < len(lines):
        line = lines[i]
        indent = count_space(line)
        line = lines[i].strip()
        if is_item(line):  
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
                if is_item(line2):
                    new_indent = count_space(line2)
                    if is_next_item(label, line2)  and new_indent <= indent:
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
            parse_one_paragraph(paragraph[start:end_index], child_node)
        else:
            node["text"] += " " + line #text fortsetter
            i += 1

def is_letter_item(line):
    return bool(re.search("^[ ]*[a-z][.]", line)) 
    

def is_number_item(line):
    return bool(re.search("^[ ]*[0-9]+[.]", line))

def is_item(line):
    return is_letter_item(line) or is_number_item(line)

def is_next_item(label, line):
    if not is_item(line):
        return False
    sep = line.strip().index(".")
    line_label = line.strip()[:sep]
    if label.isdigit() and line_label.isdigit():
        if int(line_label)-int(label) == 1:
            return True
    if label.isalpha() and line_label.isalpha():
        if ord(line_label.strip()[0])-ord(label.strip()[0]) == 1:
            return True
    return False


def count_space(str):
    # counter
    count = 0
    for i in str:
        if i == " ":
            count += 1   
        else:
            break
    return count

if __name__ == "__main__":
    main()
