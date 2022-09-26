
def main():
    text = ""
    newText = ""
    with open('another_paragraph.txt',  'r', encoding="utf8" ) as f:
            while(True):    
                line = f.readline()
                if not line:
                    break
                text += line

                lineSpacing = count_space(line)
                newLineSpacing = (lineSpacing // 2)*2
                newText += " "*newLineSpacing + line.strip() + "\n"
    
    #write the newText to a file
    f = open("DEMOadjusted.txt", "w")
    f.write(newText)
    f.close()


if __name__ == "__main__":
    main()