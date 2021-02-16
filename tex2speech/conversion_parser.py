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

    def _resolveEnvironmentElements(self, envNode, elemListParent, elemList):
        self.resEnvCount += 1
        self.totalCount += 1
        # print("RESOLVE ENVIRONMENT " + str(self.resEnvCount) + ", " + str(self.totalCount) + " DEEP")
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
                        self.envStack.append(self.db.getEnvDefinition(envNode.name))
                        contents = envNode.args[elem.getArgNum].contents
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, insertIndex=i)
                        self.envStack.pop()
                    elif isinstance(elem, ContentElement):
                        self.envStack.append(self.db.getEnvDefinition(envNode.name))
                        _, contents = seperateContents(envNode)
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, insertIndex=i)
                        self.envStack.pop()
                    elif isinstance(elem, TextElement):
                        elemList[i-1].appendTailText(elem.getHeadText())
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                    nextOffset += newInd - i
                else:
                    self._resolveEnvironmentElements(envNode, elemList[i], elemList[i].children)
                offset += nextOffset
        # print("END RESOLVE ENVIRONMENT " + str(self.resEnvCount) + ", " + str(self.totalCount) + " DEEP")
        self.resEnvCount -= 1
        self.totalCount -= 1


    def _parseEnvironment(self, envNode, ssmlNode, ssmlChildren, insertIndex):
        self.parEnvCount += 1
        self.totalCount += 1
        # print("PARSE ENVIRONMENT " + str(self.parEnvCount) + ", " + str(self.totalCount) + " DEEP")
        args, contents = seperateContents(envNode)
        # print("env: " + envNode.name + " recieved")

        conv = self.db.getEnvConversion(envNode.name)
        if not conv:
            self._parseNodes(contents, ssmlNode, ssmlChildren=ssmlChildren, insertIndex=insertIndex)
        else:
            # print("env: " + envNode.name + ": pre " + str(conv))
            self._resolveEnvironmentElements(envNode, ssmlNode, conv)
            # print("env: " + envNode.name + ": post " + str(conv))
            for ssmlSubNode in conv:
                ssmlChildren.insert(insertIndex, ssmlSubNode)
                insertIndex += 1

        # print("END PARSE ENVIRONMENT " + str(self.parEnvCount) + ", " + str(self.totalCount) + " DEEP")
        self.parEnvCount -= 1
        self.totalCount -= 1
        return insertIndex

    def _resolveCmdElements(self, cmdNode, elemListParent, elemList):
        self.resCmdCount += 1
        self.totalCount += 1
        # print("RESOLVE COMMAND " + str(self.resCmdCount) + ", " + str(self.totalCount) + " DEEP")
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
                        contents = cmdNode.args[elem.getArgNum].contents
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, insertIndex=i)
                    elif isinstance(elem, TextElement):
                        elemList[i-1].appendTailText(elem.getHeadText())
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                    nextOffset += newInd - i
                else:
                    self._resolveCmdElements(cmdNode, elemList[i], elemList[i].children)
                offset += nextOffset
        # print("END RESOLVE COMMAND " + str(self.resCmdCount) + ", " + str(self.totalCount) + " DEEP")
        self.resCmdCount -= 1
        self.totalCount -= 1

    def _parseCommand(self, cmdNode, ssmlNode, ssmlChildren, insertIndex):
        self.parCmdCount += 1
        self.totalCount += 1
        # print("PARSE COMMAND " + str(self.parCmdCount) + ", " + str(self.totalCount) + " DEEP")
        args, _ = seperateContents(cmdNode)
        
        # print("cmd: " + cmdNode.name + " recieved")
        conv = None
        if len(self.envStack) > 0 and cmdNode.name in self.envStack[-1]:
            conv = self.envStack[-1][cmdNode.name]
        else:
            conv = self.db.getCmdConversion(cmdNode.name)
        
        if conv:
            # print("cmd: " + cmdNode.name + ": pre " + str(conv))
            self._resolveCmdElements(cmdNode, ssmlNode, conv)
            # print("cmd: " + cmdNode.name + ": post " + str(conv))
            for ssmlSubNode in conv:
                ssmlChildren.insert(insertIndex, ssmlSubNode)
                insertIndex += 1

        # print("END PARSE COMMAND " + str(self.parCmdCount) + ", " + str(self.totalCount) + " DEEP")
        self.parCmdCount -= 1
        self.totalCount -= 1
        return insertIndex

    def _parseNodes(self, texNodes: list, ssmlNode: SSMLElementNode, ssmlChildren=None, insertIndex=0):
        self.parNodCount += 1
        self.totalCount += 1
        # print()
        # print("PARSE NODES " + str(self.parNodCount) + ", " + str(self.totalCount) + " DEEP")
        if ssmlChildren is None:
            ssmlChildren = ssmlNode.children
        # print("insertIndex " + str(insertIndex) + " in " + str(ssmlChildren))
        for texNode in texNodes:
            if exprTest(texNode, TexSoup.data.TexEnv):
                insertIndex = self._parseEnvironment(texNode, ssmlNode, ssmlChildren, insertIndex)
                # print("Updated insertIndex " + str(insertIndex) + " in " + str(ssmlChildren))
            elif exprTest(texNode, TexSoup.data.TexCmd):
                insertIndex = self._parseCommand(texNode, ssmlNode, ssmlChildren, insertIndex) # TODO: FIGURE out function later
                # print("Updated insertIndex " + str(insertIndex) + " in " + str(ssmlChildren))
            elif exprTest(texNode, TexSoup.data.Token):
                if len(ssmlChildren) == 0 or insertIndex == 0:
                    ssmlNode.appendHeadTextstr(str(texNode))
                else:
                    ssmlChildren[insertIndex-1].appendTailText(str(texNode))
        # print("END PARSE NODES " + str(self.parNodCount) + ", " + str(self.totalCount) + " DEEP")
        # print()
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
        return tree
