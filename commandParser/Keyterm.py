import os

directory = '/projects/49x/tex2speech/texFiles'

#create dictionary (Hashmap)
keyWord = {}

#loop through directory to get all .tex files
for filename in os.listdir(directory):

    #open files that have .tex extension
    if filename.endswith(".tex"):
        try:

            with open('/projects/49x/tex2speech/texFiles/' + filename, 'r',encoding='mac_roman') as file:
                #loop line by line in file
                for line in file:

                    #search every character in the line
                    for i in range(len(line)):
                        #enter if we find a keyword starting with \
                        if line[i] == "\\" and i!= len(line):
                            temp = ""
                            #this eliminates the \ when adding as a key, and doesnt cause
                            #errors when there are two commands in a row i.e \sqrt \beta
                            i = i+1
                            while (1):
                                #I did it this way instead of having all of these checks in the
                                #while loop condition, I also had errors looping with all in the condition

                                #I may be missing some cases
                                if line[i] == '':
                                    break
                                if line[i] == "{" or line[i] == "}":
                                    break
                                elif line[i] == "[" or line[i] == "]":
                                    break
                                elif line[i] == " ":
                                    break
                                elif line[i] == "\n":
                                    break
                                elif line[i] == "(" or line[i] == ")":
                                    break
                                elif line[i] == "\\":
                                    break
                                else:
                                    #append the read character to form a complete word
                                    temp = temp + line[i]
                                    i = i + 1

                            #if temp is in t    he dictionary, add 1 to the value
                            #else, add temp as a key and assign value as 1
                            if temp in keyWord:
                                keyWord[temp] += 1
                            else:
                                keyWord[temp] = 1
        except:
            pass

#Sort the dictionary (Hashmap) from highest value to lowest value
sortedKeyWords = sorted(keyWord.items(), key=lambda x: x[1], reverse=True)

#print the sorted dictionary (Hashmap)
for i in sortedKeyWords:
    print(i[0], "  ==>", i[1])
