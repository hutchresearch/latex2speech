from app.logger import logging, writelog

import TexSoup
import os
from os import path

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
def aux_file_hash_table(aux_file):
    hash = {}

    for line in aux_file:
        if (line[0:9] == r"\newlabel"):
            hash_object = []
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
            label_type = ""
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
                    label_type += char

            # Adding object information to hash array object 
            hash_object.append(page)
            hash_object.append(section)
            hash_object.append(caption)
            hash_object.append(label_type)

            # Adding to hashtable
            hash[name] = hash_object

    return hash

'''With the hash table that was created, use findall from TexSoup to replace file contents'''
def replace_references(contents, my_hash):
    # Traverse doc file, replacing them, by looking into hashtable
    myDoc = TexSoup.TexSoup(str(contents))
    for name in my_hash:
        if (my_hash[name][3][0:8] == "equation"):
            old = "Eq.~(\\ref{" + name + "})"
            new = "Equation " + my_hash[name][0]
        else:
            old = "\\ref{" + name + "}"
            new = my_hash[name][0]

        contents = contents.replace(old, new)
    return contents

def expand_doc_new_labels(doc):
    # TODO
    # Create .aux file
    os.system("pdflatex -interaction=nonstopmode " + doc)

    # Get appropriate .aux file to corresponding document
    # Open .aux file (Assuming it's been generated)
    split_string = doc.split(".tex", 1)
    doc_name = split_string[0] + ".aux"

    # Traverse .aux file, create hashtable for commands -> vallues
    if path.exists(split_string[0] + ".aux"):
        auxFile = open(doc_name, "r")
        myHash = aux_file_hash_table(auxFile)

        # Repalce all references to correct for figures and equations
        doc = open(doc, "r+")
        contents = replace_references(doc.read(), myHash)
        doc.truncate(0)
        doc.write(contents)

        # Delete .pdf, .out, .log, and .aux file
        if path.exists(split_string[0] + ".log"):
            os.remove(split_string[0] + ".log")

        if path.exists(split_string[0] + ".out"):
            os.remove(split_string[0] + ".out")

        if path.exists(split_string[0] + ".pdf"):
            os.remove(split_string[0] + ".pdf")

        if path.exists(split_string[0] + ".aux"):
            os.remove(split_string[0] + ".aux")

'''This function is to help test, since the main function expects a file, while this has contents'''
def hash_table_test(contents):
    hash = {}
    contents = contents.splitlines()

    for line in contents:
        if (line[0:9] == r"\newlabel"):
            hash_object = []
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
            label_type = ""
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
                    label_type += char

            # Adding object information to hash array object 
            hash_object.append(page)
            hash_object.append(section)
            hash_object.append(caption)
            hash_object.append(label_type)

            # Adding to hashtable
            hash[name] = hash_object
    return hash