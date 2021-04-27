import os

# Path to upload
path = os.getcwd() + '/upload'

# Helper method used if found a corresponding input file
def found_input_file(line, outfile, i, input):
    tmp = ""  
    contained = False

    while(line[i] != '}'):
        tmp = tmp + line[i]                          

        # Checks if input/include keyword was found in list of fiels
        for input_file in input:
            append = tmp

            if(tmp[len(tmp)-3:len(tmp)] != ".tex"):
                append = tmp + ".tex"

            if(append == input_file):
                bib = []
                inner = []
                write_to_file(outfile, bib, input, input_file, inner)
                contained = True

        i = i + 1

    if(contained == False):
        outfile.write(tmp + " Input file not found \n")

# Helper method used if found a corresponding bib file
# Will return inner file which records corresponding bib file,
# master file and if there was a bib or not
def found_bibliography_file(line, outfile, i, bib, inner_file):
    tmp = ""  
    contained = False
    
    while(line[i] != '}'):
        tmp = tmp + line[i]                          

        # Checks if bibliography keyword was found in list of fiels
        for bib_file in bib:
            append = tmp

            if(tmp[len(tmp)-3:len(tmp)] != ".bib"):
                append = tmp + ".bib"

            if(append == bib_file):
                the_path = path + "/" + bib_file
                inner_file.append(str(the_path))
                contained = True

        i = i + 1

    if(contained == False):
        outfile.write(tmp + " Bibliography file not found \n")
        inner_file.append("")

    inner_file.append(str(contained))
    return inner_file

# Function to check if the command is equal
def check(tmp, cmd):
    if tmp == cmd[:len(tmp)]:
        return True 
    return False

# Get rid of extra \ at end of words
def rid_of_back_backslash(line, i, potential):
    # Get end of line slashes out    
    if i > 0 and line[i - 1] == ' ' and line[i] == '\\':
        potential = 'True'

    if line[i] == ' ':
        potential = 'False'

    if i < len(line) and potential == 'True' and line[i] == '\\' and (line[i + 1] == ' ' or line[i + 1] == '\n'):
        potential = 'Changed'

    return potential

def write_to_file(outfile, bib, input, file, inner_file):
    potential = 'False'

    with open(path + "/" + file, 'r') as in_file:
        # For each line, add to the master file
        for line in in_file:
            tmp = ""
            
            for i in range(len(line)):
                potential = rid_of_back_backslash(line, i, potential)
                if (potential == 'Changed'):
                    i = i + 1
                    potential = 'False'

                tmp = tmp + line[i]

                # Handle comments
                if tmp == "%":
                    break

                if not check(tmp, r"\include{") and not check(tmp, r"\input{") and not check(tmp, r"\bibliography{"):
                    outfile.write(tmp)
                    tmp = ""

                i = i + 1
                # Finds include or input file
                if (tmp == "\\include{" or tmp == "\\input{"):
                    found_input_file(line, outfile, i, input)

                # Finds bibliography file
                if (tmp == "\\bibliography{"):
                    inner_file = found_bibliography_file(line, outfile, i, bib, inner_file)

# Creates a list of master files to hold the uploaded main 
# files and input files that are referenced into a single 
# master file
#
# returns list of master files
def create_master_files(main, input, bib):
    master_files = []
    add = 0

    # For every uploaded main file
    for main_file in main:
        add = add + 1

        # Create new master file
        with open("final" + str(add) + ".tex", 'w') as outfile:
            inner_file = []
            inner_file.append("final" + str(add) + ".tex")

            # Writes content to the outfile
            write_to_file(outfile, bib, input, main_file, inner_file)
            outfile.close()

            master_files.append(inner_file)
                        
        outfile.close()
    return master_files

# Checks each document to see if the file is a main document or input document
# This is denoted by \begin{document} and \end{document} as main, and not if input
# Returns the array of all master files and input files
def seperate_main_input(files):
    total = []
    master = []
    input_list = []
    for filename in files:
        with open(path + '/' + filename, 'r') as file:
            contents = file.read()
            if r'\begin{document}' in contents and r'\end{document}' in contents:
                master.append(filename)
            else:
                input_list.append(filename)
            file.close()

    total.append(master)
    total.append(input_list)
    
    return total

# Facilitator to get the list of master files.
# Input -> Tex Files (input + master)
#       -> Bib Files
# Output
#       -> Returns name of the main tex files
#       -> Returns list of main files to run
def format_master_files(tex, bib):
    texFiles = seperate_main_input(tex)

    master_files = create_master_files(texFiles[0], texFiles[1], bib)

    files = []
    files.append(texFiles[0])
    files.append(master_files)

    return files