import TexSoup
import os
from os import path
from keyboard import press
import time

'''Function that will travers aux file for \\newlabel
Create a hashtable to store in these values
    Input: .aux file to corresponding .tex file
    Output: Hashtable for \\newlabel
    HashTable format
        Key: Name of object
        Value: List
            List[0] = Page Num
            List[1] = Section Num
            List[2] = Caption (optional)
            List[3] = Type (equation, figure, etc) '''
def auxFileHashTable(auxFile):
    hash = {}

    for line in auxFile:
        if (line[0:9] == r"\newlabel"):
            hashObject = []
            count = 1
            name = ""

            # Grabbing key name of hashtable
            for char in line[10:]:
                count += 1
                if (char != "}"):
                    name += char
                else:
                    count += 10
                    break

            obj = 1
            page = ""
            section = ""
            caption = ""
            labelType = ""
            index = count

            # Adding .aux information to corresponding
            # object type
            for char in line[count:]:
                index += 1
                if (char == '}' and line[index] == '{'):
                    obj += 1
                elif (char == '{'):
                    obj = obj
                elif (obj == 1):
                    page += char
                elif(obj == 2):
                    section += char
                elif (obj == 3):
                    caption += char
                elif (obj == 4):
                    labelType += char

            # Adding object information to hash array object 
            hashObject.append(page)
            hashObject.append(section)
            hashObject.append(caption)
            hashObject.append(labelType)

            # Adding to hashtable
            hash[name] = hashObject

    # Print helpers
    # print(hash['fl'])
    # print(hash['sl'])
    # print(hash['tl'])
    # print(hash['sample'])

    return hash

'''With the hash table that was created, use findall from TexSoup to replace file contents'''
def replaceReferences(contents, myHash):
    # Traverse doc file, replacing them, by looking into hashtable
    myDoc = TexSoup.TexSoup(str(contents))
    for name in myHash:
        print("Syst " + name)
        if (myHash[name][3][0:8] == "equation"):
            old = "Eq.~(\\ref{" + name + "})"
            new = "Equation " + myHash[name][0]
        else:
            old = "\\ref{" + name + "}"
            new = myHash[name][0]

        contents = contents.replace(old, new)

    print(contents)
    return contents

def expandDocNewLabels(doc):
    # TODO
    # Create .aux file
    os.system("pdflatex -interaction=nonstopmode " + doc)

    # Get appropriate .aux file to corresponding document
    # Open .aux file (Assuming it's been generated)
    split_string = doc.split(".tex", 1)
    docName = split_string[0] + ".aux"

    # Traverse .aux file, create hashtable for commands -> vallues
    auxFile = open(docName, "r")
    myHash = auxFileHashTable(auxFile)

    # Repalce all references to correct for figures and equations
    doc = open(doc, "r")
    replaceReferences(doc.read(), myHash)

    # Delete .pdf, .out, .log, and .aux file
    # if path.exists(split_string[0] + ".log"):
    #     os.remove(split_string[0] + ".log")

    # if path.exists(split_string[0] + ".out"):
    #     os.remove(split_string[0] + ".out")

    # if path.exists(split_string[0] + ".pdf"):
    #     os.remove(split_string[0] + ".pdf")

    # if path.exists(split_string[0] + ".aux"):
    #     os.remove(split_string[0] + ".aux")

'''This function is to help test, since the main function expects a file, while this has contents'''
def hashTableTest(contents):
    hash = {}
    contents = contents.splitlines()

    for line in contents:
        if (line[0:9] == r"\newlabel"):
            hashObject = []
            count = 1
            name = ""

            # Grabbing key name of hashtable
            for char in line[10:]:
                count += 1
                if (char != "}"):
                    name += char
                else:
                    count += 10
                    break

            obj = 1
            page = ""
            section = ""
            caption = ""
            labelType = ""
            index = count

            # Adding .aux information to corresponding
            # object type
            for char in line[count:]:
                index += 1
                if index == len(line):
                    break
                if (char == '}' and line[index] == '{'):
                    obj += 1
                elif (char == '{'):
                    obj = obj
                elif (obj == 1):
                    page += char
                elif(obj == 2):
                    section += char
                elif (obj == 3):
                    caption += char
                elif (obj == 4):
                    labelType += char

            # Adding object information to hash array object 
            hashObject.append(page)
            hashObject.append(section)
            hashObject.append(caption)
            hashObject.append(labelType)

            # Adding to hashtable
            hash[name] = hashObject
    return hash

# file = open("sample.aux", "r")
# hash = hashTableTest((r"\newlabel{fl}{{1}{1}{}{equation.0.1}{}}" + "\n" +
#             r"\newlabel{sl}{{2}{1}{}{equation.0.1}{}}"))

# print(hash['fl'])
# print(hash['sl'])
