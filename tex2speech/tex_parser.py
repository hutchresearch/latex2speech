import TexSoup
import xml.etree.ElementTree as ET
import enum
import expand_macros, expand_labels
from doc_cleanup import cleanXMLString
from tex_soup_utils import seperateContents

class TexParser:
    def __init__(self):
        self.latex = ET.parse('./static/pronunciation.xml').getroot()
        self.mathmode = ET.parse('./static/mathmode_pronunciation.xml').getroot()

    def parse(self, docContents):
        self.output = ''
        self.envStack = []
        self.ssmlStack = []
        self.inTable = False

        docstr = None
        try:
            docstr = str(docContents, 'utf-8')
        except TypeError:
            docstr = docContents
        docstr = docstr.replace('\n', ' ')
        docstr = docstr.replace('\hline', '')

        doc = TexSoup.TexSoup(docstr)
        doc = expand_macros.expandDocMacros(doc)

        self._concatOutput("<speak>")
        self._parseNodeContents(doc.contents)
        self._concatOutput("</speak>")

        self.output = cleanXMLString(self.output)

        return self.output

    def _concatOutput(self, string):
        if len(self.output) == 0 or self.output[-1] == ' ':
            self.output += string
        elif len(string) == 0 or string[0] == ' ':
            self.output += string
        else:
            self.output += ' ' + string

    # Flip switch for true/false in environment
    # This might be able to done better, when printing node
    # in _nodeparseNodeContents that single node is the \begin to \end tabular
    def _checkIfInTableEnvionment(self):
        if len(self.envStack) > 0 and (self.envStack[-1].get('readTable') == 'true'):
            self.inTable = not self.inTable
        elif (self.inTable == True):
            self.inTable = not self.inTable
            self._concatOutput(" End table.")

    # Function that will take in new table contents, and parse
    # each column
    def _parseTableContents(self, contentsNode):
        self._concatOutput("New Row: ")
        split = str(contentsNode).split('&') 
        column = 1
        for word in split: 
            if word != "&":
                self._concatOutput(", Column " + str(column) + ", Value: " + word)
                column += 1

    def _parseEnv(self, node):
        envElem = None
        for envElem in self.latex.findall("env"):
            if envElem.name == node.name:
                break 

        if envElem:
            self.envStack.append(envElem)
        else:
            self._parseNodeContents(envElem.contents)

    def _parseCmd(self, node):
        pass

    def _parseNodeContents(self, nodeContents):
        if len(nodeContents) > 0:
            for node in nodeContents:
                if isinstance(node, TexSoup.utils.Token):
                    if len(self.envStack) > 0 and (self.envStack[-1].get('mathmode') == 'true'):
                        self._parseMathModeToken(node)
                    else:
                        self._checkIfInTableEnvionment() # Could be more efficient
                        if self.inTable == True:
                            self._parseTableContents(node)
                        else:
                            self._concatOutput(str(node))

                elif isinstance(node, TexSoup.data.TexNode):
                    if isinstance(node.expr, TexSoup.data.TexEnv):
                        self._parseEnv(node)
                    elif isinstance(node.expr, TexSoup.data.TexCmd):
                        self._parseCmd(node)
                    else:
                        self._parseNodeContents(node.contents)