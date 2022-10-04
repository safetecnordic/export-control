
def main():
    text = ""
    newText = ""
    with open('Forskrift.txt',  'r', encoding="utf8" ) as f:
            while(True):
                line = f.readline()
                if not line:
                    break
                text += line

                lineSpacing = count_space(line)
                newLineSpacing = (lineSpacing // 2)*2
                newText += " "*newLineSpacing + line.strip() + "\n"
    
    #write the newText to a file
    f = open("DEMOforskrift.txt", "w",  encoding="utf8")
    f.write(newText)
    f.close()


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