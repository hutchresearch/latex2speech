import TexSoup
import xml.etree.ElementTree as ET
import enum

class TexParser:
    def __init__(self):
        self.latex = ET.parse('pronunciation.xml').getroot()
        self.mathmode = ET.parse('mathmode_pronunciation.xml').getroot()

    def parse(self, file):
        self.output = ''

        docstr = file.read()
        docstr = docstr.replace('\n', ' ')
        # TODO: More cleanup/command expansion

        doc = TexSoup.TexSoup(docstr)
        self._concatOutput("<speak>")
        self._parseNodeContents(doc.contents, [])
        self._concatOutput("</speak>")

        # TODO: Final cleanup

        return self.output

    def _concatOutput(self, string):
        if len(self.output) == 0 or self.output[-1] == ' ':
            self.output += string
        elif len(string) == 0 or string[0] == ' ':
            self.output += string
        else:
            self.output += ' ' + string

    def _parseMathModeToken(self, tokenNode):
        mathTokens = self._getMathTokens(tokenNode.text)
        #print("math mode parsed from: " + tokenNode.text)
        for t in mathTokens:
            #print(t)
            found = False
            for s in self.mathmode.findall('symb'):
                if s.get('name') == t:
                    if s.find('say_as') is not None:
                        self._concatOutput(str(s.find('say_as').text))
                    found = True
            if not found:
                self._concatOutput(str(t))

    def _getMathTokens(self, mathStr):
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
        
    def _parseCmdSub(self, cmdNode, cmdElem, envList):
        if cmdElem.find('prefix') is not None:
            self._concatOutput(cmdElem.find('prefix').text)

        argIndex = 0
        for arg in cmdElem.findall('arg'):
            while argIndex < len(cmdNode.args) and type(cmdNode.args[argIndex]) is not TexSoup.data.BraceGroup:
                argIndex += 1

            if argIndex == len(cmdNode.args):
                print("Error: Expected more arguments then given in command")
                break

            if arg.find('prefix') is not None:
                self._concatOutput(arg.find('prefix').text)
        
            if arg.get('say_contents') == 'true':
                self._parseNodeContents(cmdNode.args[argIndex].contents, envList)
                
            if arg.find('suffix') is not None:
                self._concatOutput(arg.find('suffix').text)
        
            argIndex += 1

        if cmdElem.find('say_as') is not None:
            self._concatOutput(cmdElem.find('say_as').text)

        if cmdElem.find('suffix') is not None:
            self._concatOutput(cmdElem.find('suffix').text)

    def _parseCmd(self, cmdNode, envList):
        found = False
        searchEnvs = []
        
        if len(envList) > 0:
            searchEnvs.append(envList[-1])
            if envList[-1].get('mathmode') == 'true':
                searchEnvs.append(self.mathmode)
            else:
                searchEnvs.append(self.latex)
        else: 
            searchEnvs.append(self.latex)
            
        i = 0
        while i < len(searchEnvs) and not found:
            for cmdElem in searchEnvs[i].findall('cmd'):
                if cmdElem.get('name') == cmdNode.name:
                    self._parseCmdSub(cmdNode, cmdElem, envList)
                    found = True
            i += 1

        # Go down next recursive level, excluding arguments
        self._parseNodeContents(cmdNode.contents[len(cmdNode.args):], envList)

    def _parseEnv(self, envNode, envList):
        found = False
        for envElem in self.latex.findall('env'):
            if envElem.get('name') == envNode.name:
                found = True
                envList.append(envElem)
                
                if envElem.find('prefix') is not None:
                    self._concatOutput(envElem.find('prefix').text)

                # Go down next recursive level, excluding arguments
                self._parseNodeContents(envNode.contents[len(envNode.args):], envList)

                if envElem.find('suffix') is not None:
                    self._concatOutput(envElem.find('suffix').text)

                envList.pop()
                break

        if not found:
            self._parseNodeContents(envNode.contents[len(envNode.args):], envList)

    def _parseNodeContents(self, nodeContents, envList):
        if len(nodeContents) > 0:
            for node in nodeContents:
                # if type(node) == TexSoup.utils.Token:
                if isinstance(node, TexSoup.utils.Token):
                    if len(envList) > 0 and (envList[-1].get('mathmode') == 'true'):
                        self._parseMathModeToken(node)
                    #TODO: Check for reserved tokens (e.g. r"\\")
                    else:
                        self._concatOutput(str(node))
                elif isinstance(node, TexSoup.data.TexNode):
                    if isinstance(node.expr, TexSoup.data.TexEnv):
                        self._parseEnv(node, envList)
                    elif isinstance(node.expr, TexSoup.data.TexCmd):
                        self._parseCmd(node, envList)
                    else:
                        self._parseNodeContents(node.contents, envList)

