import os

directory = '/home/nemethj2/sproj/latex2speech/commandParser/tests'

keyWord = {}

for filename in os.listdir(directory):

    if filename.endswith(".tex"):
        try:

            with open('/home/nemethj2/sproj/latex2speech/commandParser/tests/' + filename, 'r',encoding='mac_roman') as file:
                for line in file:

                    for i in range(len(line)):
                        if line[i] == "\\" and i!= len(line):
                            temp = ""
                            i = i+1
                            while (1):
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
                                    temp = temp + line[i]
                                    i = i + 1

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
