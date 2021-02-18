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
    
        # DEBUG
        self.resEnvCount = 0
        self.parEnvCount = 0
        self.resCmdCount = 0
        self.parCmdCount = 0
        self.parNodCount = 0
        self.totalCount = 0

    def _getArg(self, node, argElem):
        targetType = TexSoup.data.BraceGroup
        if argElem.getArgType() == 'bracket':
            targetType = TexSoup.data.BracketGroup
        
        i = -1
        num = 0
        arg = None
        while num < argElem.getArgNum() and i+1 < len(node.args):
            i += 1
            if isinstance(node.args[i], targetType):
                num += 1

        if num == argElem.getArgNum():
            arg = node.args[i]

        return arg

    def _resolveEnvironmentElements(self, envNode, elemListParent, elemList, leftSibling):
        self.resEnvCount += 1
        self.totalCount += 1
        if len(elemList) > 0:
            while isinstance(elemList[0], TextElement):
                textElem = elemList.pop(0)
                elemListParent.appendHeadText(textElem.getHeadText())
            offset = 0
            for k in range(len(elemList)):
                i = k + offset
                nextOffset = 0
                if not isinstance(elemList[i], SSMLElementNode):
                    elem = elemList.pop(i)
                    nextOffset -= 1
                    newInd = i
                    if isinstance(elem, ArgElement):
                        contents = self._getArg(envNode, elem).contents
                        if i > 0:
                            while len(contents) > 0 and isinstance(contents[0], TexSoup.data.Token):
                                text = str(contents.pop(0))
                                elemList[i-1].appendTailText(text)
                        elif leftSibling:
                            while len(contents) > 0 and isinstance(contents[0], TexSoup.data.Token):
                                text = str(contents.pop(0))
                                leftSibling.appendTailText(text)
                        self.envStack.append(self.db.getEnvDefinition(envNode.name))
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, insertIndex=i)
                        self.envStack.pop()
                    elif isinstance(elem, ContentElement):
                        _, contents = seperateContents(envNode)
                        if i > 0:
                            while len(contents) > 0 and isinstance(contents[0], TexSoup.data.Token):
                                text = str(contents.pop(0))
                                elemList[i-1].appendTailText(text)
                        elif leftSibling:
                            while len(contents) > 0 and isinstance(contents[0], TexSoup.data.Token):
                                text = str(contents.pop(0))
                                leftSibling.appendTailText(text)
                        self.envStack.append(self.db.getEnvDefinition(envNode.name))
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, insertIndex=i)
                        self.envStack.pop()
                    elif isinstance(elem, TextElement):
                        if i > 0:
                            elemList[i-1].appendTailText(elem.getHeadText())
                        elif leftSibling:
                            leftSibling.appendTailText(elem.getHeadText())
                        else:
                            elemListParent.appendHeadText(elem.getHeadText())
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                    nextOffset += newInd - i
                else:
                    newLeftSibling = leftSibling
                    if i > 0:
                        newLeftSibling = elemList[i-1]
                    self._resolveEnvironmentElements(envNode, elemList[i], elemList[i].children, newLeftSibling)
                offset += nextOffset
        self.resEnvCount -= 1
        self.totalCount -= 1


    def _parseEnvironment(self, envNode, ssmlNode, ssmlChildren, insertIndex):
        self.parEnvCount += 1
        self.totalCount += 1
        args, contents = seperateContents(envNode)

        elemList = self.db.getEnvConversion(envNode.name)
        if not elemList:
            self._parseNodes(contents, ssmlNode, ssmlChildren=ssmlChildren, insertIndex=insertIndex)
        else:
            leftSibling = None
            if insertIndex > 0:
                leftSibling = ssmlChildren[insertIndex-1]
            self._resolveEnvironmentElements(envNode, ssmlNode, elemList, leftSibling)
            for ssmlSubNode in elemList:
                ssmlChildren.insert(insertIndex, ssmlSubNode)
                insertIndex += 1

        self.parEnvCount -= 1
        self.totalCount -= 1
        return insertIndex

    def _resolveCmdElements(self, cmdNode, elemListParent, elemList, leftSibling):
        self.resCmdCount += 1
        self.totalCount += 1
        if len(elemList) > 0:
            while len(elemList) > 0 and isinstance(elemList[0], TextElement):
                textElem = elemList.pop(0)
                elemListParent.appendHeadText(textElem.getHeadText())
            offset = 0
            for k in range(len(elemList)):
                i = k + offset
                nextOffset = 0
                if not isinstance(elemList[i], SSMLElementNode):
                    elem = elemList.pop(i)
                    nextOffset -= 1
                    newInd = i
                    if isinstance(elem, ArgElement):
                        contents = self._getArg(cmdNode, elem).contents
                        if i > 0:
                            while len(contents) > 0 and isinstance(contents[0], TexSoup.data.Token):
                                text = str(contents.pop(0))
                                elemList[i-1].appendTailText(text)
                        elif leftSibling:
                            while len(contents) > 0 and isinstance(contents[0], TexSoup.data.Token):
                                text = str(contents.pop(0))
                                leftSibling.appendTailText(text)
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, insertIndex=i)
                    elif isinstance(elem, TextElement):
                        elemList[i-1].appendTailText(elem.getHeadText())
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                    nextOffset += newInd - i
                else:
                    newLeftSibling = leftSibling
                    if i > 0:
                        newLeftSibling = elemList[i-1]
                    self._resolveCmdElements(cmdNode, elemList[i], elemList[i].children, newLeftSibling)
                offset += nextOffset
        self.resCmdCount -= 1
        self.totalCount -= 1

    def _parseCommand(self, cmdNode, ssmlNode, ssmlChildren, insertIndex):
        self.parCmdCount += 1
        self.totalCount += 1
        args, _ = seperateContents(cmdNode)
        
        elemList = None
        if len(self.envStack) > 0 and cmdNode.name in self.envStack[-1]:
            elemList = self.envStack[-1][cmdNode.name]
        else:
            elemList = self.db.getCmdConversion(cmdNode.name)
        
        if elemList:
            leftSibling = None
            if insertIndex > 0:
                leftSibling = ssmlChildren[insertIndex-1]
            self._resolveCmdElements(cmdNode, ssmlNode, elemList, leftSibling)
            for ssmlSubNode in elemList:
                ssmlChildren.insert(insertIndex, ssmlSubNode)
                insertIndex += 1

        self.parCmdCount -= 1
        self.totalCount -= 1
        return insertIndex

    def _parseNodes(self, texNodes: list, ssmlNode: SSMLElementNode, ssmlChildren=None, insertIndex=0):
        self.parNodCount += 1
        self.totalCount += 1
        print("BEFORE: " + str(self.parNodCount))
        print(ssmlNode)
        print(ssmlChildren)
        print()
        if ssmlChildren is None:
            ssmlChildren = ssmlNode.children
        for texNode in texNodes:
            if exprTest(texNode, TexSoup.data.TexEnv):
                insertIndex = self._parseEnvironment(texNode, ssmlNode, ssmlChildren, insertIndex)
            elif exprTest(texNode, TexSoup.data.TexCmd):
                insertIndex = self._parseCommand(texNode, ssmlNode, ssmlChildren, insertIndex)
            elif exprTest(texNode, TexSoup.data.Token):
                if len(ssmlChildren) == 0 or insertIndex == 0:
                    ssmlNode.appendHeadText(str(texNode))
                else:
                    ssmlChildren[insertIndex-1].appendTailText(str(texNode))
            
            print("LOOP IN " + str(self.parNodCount))
            print(ssmlNode)
            print(ssmlChildren)
            print()
        print("AFTER: " + str(self.parNodCount))
        print(ssmlNode)
        print(ssmlChildren)
        print()
        self.parNodCount -= 1
        self.totalCount -= 1
        return insertIndex

    def _printTreeSub(self, tree, level, levelArr, atIndex, parentIndex):
        if len(levelArr) == level:
            levelArr.append([])
        levelArr[level].append(str(parentIndex) + ' -> ' + str(tree))
        for i, child in enumerate(tree.children):
            self._printTreeSub(child, level+1, levelArr, i, atIndex)

    # Method for debugging
    def printTree(self, tree):
        levelArr = []
        self._printTreeSub(tree, 0, levelArr, 0, -1)
        for level in levelArr:
            print(level)

    def parse(self, doc: TexSoup.data.TexNode):
        tree = RootElement()
        self._parseNodes(doc.contents, tree)
        # TODO: Should avoid this by using insertChild always
        # TODO: TODO: do the parent attaching
        return tree
