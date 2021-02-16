import TexSoup

from conversion_db import ConversionDB
from SSMLParsing.arg_element import ArgElement
from SSMLParsing.break_element import BreakElement
from SSMLParsing.content_element import ContentElement
from SSMLParsing.emphasis_element import EmphasisElement
from SSMLParsing.prosody_element import ProsodyElement
from SSMLParsing.root_element import RootElement
from SSMLParsing.ssml_element_node import SSMLElementNode
from SSMLParsing.ssml_element import SSMLElement
from SSMLParsing.text_element import TextElement

from tex_soup_utils import exprTest, seperateContents

class ConversionParser:
    def __init__(self, db: ConversionDB):
        self.db = db
        self.envStack = []

    def _resolveEnvironmentElements(self, envNode, elemListParent, elemList):
        if len(elemList) > 0:
            while isinstance(elemList[0], TextElement):
                textElem = elemList.pop(0)
                elemListParent.setHeadText(elemListParent.getHeadText() + textElem.getHeadText())
            offset = 0
            for k in range(len(elemList)):
                i = k + offset
                nextOffset = 0
                if not isinstance(elemList[i], SSMLElementNode):
                    elem = elemList.pop(i)
                    nextOffset -= 1
                    newInd = i
                    if isinstance(elem, ArgElement):
                        self.envStack.append(self.db.getEnvDefinition(envNode.name))
                        contents = envNode.args[elem.getArgNum].contents
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, index=i)
                        self.envStack.pop()
                    elif isinstance(elem, ContentElement):
                        self.envStack.append(self.db.getEnvDefinition(envNode.name))
                        _, contents = seperateContents(envNode)
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, index=i)
                        self.envStack.pop()
                    elif isinstance(elem, TextElement):
                        elemList[i-1].setTailText(elemList[i-1].getTailText() + elem.getHeadText())
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                    nextOffset += newInd - i
                else:
                    self._resolveEnvironmentElements(envNode, elemList[i], elemList[i].children)
                offset += nextOffset

    def _parseEnvironment(self, envNode, ssmlNode, ssmlChildren, index):
        args, contents = seperateContents(envNode)

        conv = self.db.getEnvConversion(envNode.name)
        if not conv:
            self._parseNodes(contents, ssmlNode, ssmlChildren=ssmlChildren, index=index)
        else:
            self._resolveEnvironmentElements(envNode, ssmlNode, conv)
            for ssmlSubNode in conv:
                ssmlNode.children.insert(index, ssmlSubNode)
                index += 1
        return index

    def _resolveCmdElements(self, cmdNode, elemListParent, elemList):
         if len(elemList) > 0:
            while isinstance(elemList[0], TextElement):
                textElem = elemList.pop(0)
                elemListParent.setHeadText(elemListParent.getHeadText() + textElem.getHeadText())
            offset = 0
            for k in range(len(elemList)):
                i = k + offset
                nextOffset = 0
                if not isinstance(elemList[i], SSMLElementNode):
                    elem = elemList.pop(i)
                    nextOffset -= 1
                    newInd = i
                    if isinstance(elem, ArgElement):
                        contents = cmdNode.args[elem.getArgNum].contents
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, index=i)
                    elif isinstance(elem, TextElement):
                        elemList[i-1].setTailText(elemList[i-1].getTailText() + elem.getHeadText())
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                    nextOffset += newInd - i
                else:
                    self._resolveEnvironmentElements(cmdNode, elemList[i], elemList[i].children)
                offset += nextOffset

    def _parseCommand(self, cmdNode, ssmlNode, index):
        args, _ = seperateContents(cmdNode)
        
        conv = None
        if len(self.envStack) > 0 and cmdNode.name in self.envStack[-1]:
            conv = self.envStack[-1][cmdNode.name]
        else:
            conv = self.db.getCmdConversion(cmdNode.name)
        
        if conv:
            self._resolveCmdElements(cmdNode, ssmlNode, conv)
            for ssmlSubNode in conv:
                ssmlNode.children.insert(index, ssmlSubNode)
                index += 1
        return index

    def _parseNodes(self, texNodes: list, ssmlNode: SSMLElementNode, ssmlChildren=None, index=0):
        if ssmlChildren is None:
            ssmlChildren = ssmlNode.children
        for texNode in texNodes:
            if exprTest(texNode, TexSoup.data.TexEnv):
                index = self._parseEnvironment(texNode, ssmlNode, ssmlChildren, index)
            elif exprTest(texNode, TexSoup.data.TexCmd):
                index = self._parseCommand(texNode, ssmlNode, index) # TODO: FIGURE out function later
            elif exprTest(texNode, TexSoup.data.Token):
                if len(ssmlChildren) == 0 or index == 0:
                    ssmlNode.setHeadText(ssmlNode.getHeadText() + str(texNode))
                else:
                    ssmlChildren[index].setTailText(ssmlChildren[index].getTailText() + str(texNode))
        return index #????

    def parse(self, doc: TexSoup.data.TexNode):
        tree = RootElement()
        self._parseNodes(doc.contents, tree)
        return tree

import unittest
from unittest.mock import patch, Mock
import conversion_db

class testLol(unittest.TestCase):
    @patch('conversion_db.ConversionDB')
    def testTextElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        a = [TextElement('text 1'), BreakElement()]
        cmds = {'a': a}
        def mockCmdConversion(cmd):
            nonlocal cmds
            return cmds[cmd]
        
        b = [BreakElement(), ContentElement()]
        envs = {'b': b}
        def mockEnvConversion(env):
            nonlocal envs
            return envs[env]

        a_override = [BreakElement(), TextElement('text 3')]
        envsDefn = {'b': {'a': a_override}}
        def mockEnvDefinition(env):
            nonlocal envsDefn
            return envsDefn[env]

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'text1a\a\begin{b}\a text2a\a\begin{b}\a text3a\a\end{b}\a text4a\a\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc)

if __name__ == "__main__":
    unittest.main()