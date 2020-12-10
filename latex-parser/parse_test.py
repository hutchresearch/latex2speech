import sys
import TexSoup
import xml.etree.ElementTree as ET
import enum

#Test strings
#doc = TexSoup.TexSoup(r'''$1\leq2$ is a \emph{statement}''')
#doc = TexSoup.TexSoup(r'''\begin{itemize}\item this is an item\item this is another\end{itemize}''')
#doc = TexSoup.TexSoup(r'''\begin{itemize}\item this is an item, with math\dots $1 - 23$ \item \textbf{this} is another\end{itemize} \emph{AND THIS} is something after''')

texFile = open(sys.argv[1], "r")
docstr = texFile.read()
docstr = docstr.replace('\n', '')
doc = TexSoup.TexSoup(docstr)
texFile.close()

latex = ET.parse('pronunciation.xml').getroot()
mathmode = ET.parse('mathmode_pronunciation.xml').getroot()

output = ""

def concatOutput(string):
    global output
    if len(output) == 0 or output[-1] == ' ':
        output += string
    elif len(string) == 0 or string[0] == ' ':
        output += string
    else:
        output += ' ' + string

def parseMathModeToken(tokenNode):
    mathTokens = getMathTokens(tokenNode.text)
    #print("math mode parsed from: " + tokenNode.text)
    for t in mathTokens:
        #print(t)
        found = False
        for s in mathmode.findall('symb'):
            if s.get('name') == t:
                if s.find('say_as') is not None:
                    concatOutput(str(s.find('say_as').text))
                found = True
        if not found:
            concatOutput(str(t))

def getMathTokens(mathStr):
    class tState(enum.Enum):
        null = -1
        number = 0
        mathChar = 1
    state = -1 
    next = ""
    for c in mathStr:
        if c.isdigit() or c == '.':
            if state != tState.number:
                if len(next):
                    yield next
                    next = "" 
                state = tState.number
            next = next + c
        elif c.isspace():
            if len(next):
                yield next
                next = ""
            state = tState.null
        #FIX ME: This list should be obtained from mathmode somehow, not hard-coded 
        elif c in [r"*", r"+", r"-", r"/", r"=", r"<", r">", r"!"]:
            if len(next):
                yield next
                next = ""
            state = tState.mathChar
            yield c
        else:
            next = next + c
        
def parseCmdSub(cmdNode, cmdElem, envList):
    if cmdElem.find('prefix') is not None:
        concatOutput(cmdElem.find('prefix').text)

    argIndex = 0
    for arg in cmdElem.findall('arg'):
        while argIndex < len(cmdNode.args) and type(cmdNode.args[argIndex]) is not TexSoup.data.BraceGroup:
            argIndex += 1

        if argIndex == len(cmdNode.args):
            print("Error: Expected more arguments then given in command")
            break

        if arg.find('prefix') is not None:
            concatOutput(arg.find('prefix').text)
    
        if arg.get('say_contents') == 'true':
            parseNodeContents(cmdNode.args[argIndex].contents, envList)
            
        if arg.find('suffix') is not None:
            concatOutput(arg.find('suffix').text)
    
        argIndex += 1

    if cmdElem.find('say_as') is not None:
        concatOutput(cmdElem.find('say_as').text)

    if cmdElem.find('suffix') is not None:
        concatOutput(cmdElem.find('suffix').text)

    # Go down next recursive level, excluding arguments
    parseNodeContents(cmdNode.contents[len(cmdNode.args):], envList)

def parseCmd(cmdNode, envList):
    found = False
    searchEnvs = []
    
    if len(envList) > 0:
        searchEnvs.append(envList[-1])
        if envList[-1].get('mathmode') == 'true':
            searchEnvs.append(mathmode)
        else:
            searchEnvs.append(latex)
    else: 
        searchEnvs.append(latex)
        
    i = 0
    while i < len(searchEnvs) and not found:
        for cmdElem in searchEnvs[i].findall('cmd'):
            if cmdElem.get('name') == cmdNode.name:
                parseCmdSub(cmdNode, cmdElem, envList)
                found = True
                break
        i += 1

def parseEnv(envNode, envList):
    found = False
    for envElem in latex.findall('env'):
        if envElem.get('name') == envNode.name:
            found = True
            envList.append(envElem)
            
            if envElem.find('prefix') is not None:
                concatOutput(envElem.find('prefix').text)

            # Go down next recursive level, excluding arguments
            parseNodeContents(envNode.contents[len(envNode.args):], envList)

            if envElem.find('suffix') is not None:
                concatOutput(envElem.find('suffix').text)

            envList.pop()
            break

    if not found:
        parseNodeContents(envNode.contents[len(envNode.args):], envList)

def parseNodeContents(nodeContents, envList):
    if len(nodeContents) > 0:
        for node in nodeContents:
            if type(node) == TexSoup.utils.Token:
                if len(envList) > 0 and (envList[-1].get('mathmode') == 'true'):
                    parseMathModeToken(node)
                #TODO: Check for reserved tokens (e.g. r"\\")
                else:
                    concatOutput(str(node))
            elif type(node) == TexSoup.data.TexNode:
                if type(node.expr) == TexSoup.data.TexEnv or \
                        type(node.expr) == TexSoup.data.TexNamedEnv or \
                        type(node.expr) == TexSoup.data.TexMathEnv or \
                        type(node.expr) == TexSoup.data.TexDisplayMathEnv or \
                        type(node.expr) == TexSoup.data.TexMathModeEnv or \
                        type(node.expr) == TexSoup.data.TexDisplayMathModeEnv:
                    parseEnv(node, envList)
                elif type(node.expr) == TexSoup.data.TexCmd:
                    parseCmd(node, envList)
                else:
                    parseNodeContents(node.contents, envList)

concatOutput("<speak>")
parseNodeContents(doc.contents, [])
concatOutput("</speak>")

#print(output)
outFile = open(sys.argv[2], "w")
outFile.write(output)
outFile.close()
print("Wrote SSML to " + sys.argv[2])
