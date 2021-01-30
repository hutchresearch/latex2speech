import TexSoup
import os


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
        if (line[0:9] == "\\newlabel"):
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
def replaceReferences(doc, myHash):
    # Traverse doc file, replacing them, by looking into hashtable
    contents = doc.read()
    myDoc = TexSoup.TexSoup(str(contents))
    for name in myHash:
        if (myHash[name][3][0:8] == "equation"):
            old = "Eq.~(\\ref{" + name + "})"
            new = "Equation " + myHash[name][0]
        else:
            old = "\\ref{" + name + "}"
            new = myHash[name][0]
        # FUTURE TODO
            # Talk to Connor about this, currently
            # We are just updating the contents of the page
            # The actual file needs to be updated...
        # myDoc.ref.replace_with(new)
        # myDoc.itemize
        contents = contents.replace(old, new)

    print(contents)

def expandDocNewLabels(doc):
    # TODO
    # Create .aux file

    # Get appropriate .aux file to corresponding document
    # Open .aux file (Assuming it's been generated)
    split_string = doc.name.split(".tex", 1)
    docName = split_string[0] + ".aux"

    # Traverse .aux file, create hashtable for commands -> vallues
    auxFile = open(docName, "r")
    myHash = auxFileHashTable(auxFile)

    # Repalce all references to correct for figures and equations
    replaceReferences(doc, myHash)

    # Delete .pdf, .out, .log, and .aux file
    os.remove(split_string[0] + ".log")
    os.remove(split_string[0] + ".out")
    os.remove(split_string[0] + ".pdf")
    os.remove(split_string[0] + ".aux")

# file = open("sample.tex", "r")
# expandDocMacros(file)
