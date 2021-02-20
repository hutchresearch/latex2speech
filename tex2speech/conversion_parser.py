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

'''
Main parsing class. Parses TexSoup parse trees into SSMLElementNode
    trees for future output. The conversion rules for every command 
    and environment found in the tree is determined by the database
    the class is initialized with.
'''
class ConversionParser:
    def __init__(self, db: ConversionDB):
        self.db = db
        self.envStack = []

    '''
    Retrieves the correct argument node's list of arguments with respect to 
        the format of the ArgElement class.
    '''
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

    '''
    Recursively resolves non-node SSMLElements within elemList with respect to 
        envNode. Also manages the envStack.
    '''
    def _resolveEnvironmentElements(self, envNode, elemListParent, elemList, leftChild):
        if len(elemList) > 0:
            offset = 0
            i = 0
            for k in range(len(elemList)):
                if not isinstance(elemList[i], SSMLElementNode):
                    elem = elemList.pop(i)
                    nextOffset = -1
                    newInd = i
                    parseTarget = None
                    if isinstance(elem, ArgElement):
                        parseTarget = self._getArg(envNode, elem).contents
                    elif isinstance(elem, ContentElement):
                        _, parseTarget = seperateContents(envNode)
                    elif isinstance(elem, TextElement):
                        text = elem.getHeadText()
                        if leftChild:
                            leftChild.appendTailText(text)
                        else:
                            elemListParent.appendHeadText(text)
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                        
                    # TODO: Should args within an environment's arguments reference the environment
                    # If not, stack operations should only occur in ContentElement
                    if parseTarget:
                        definition = self.db.getEnvDefinition(envNode.name)
                        if definition:
                            self.envStack.append(definition)
                            newInd = self._parseNodes(parseTarget, elemListParent, ssmlChildren=elemList, insertIndex=i, leftChild=leftChild)
                            self.envStack.pop()
                        else:
                            newInd = self._parseNodes(parseTarget, elemListParent, ssmlChildren=elemList, insertIndex=i, leftChild=leftChild)
                    
                    nextOffset += newInd - i
                    offset += nextOffset
                else:
                    self._resolveEnvironmentElements(envNode, elemList[i], elemList[i].children, None)
                
                i = (k + 1) + offset
                if i > 0:
                    leftChild = elemList[i-1]


    '''
    Handles environment parsing, returning the result of its parsing or 
        or none of no appropriate definition is found.
    '''
    def _parseEnvironment(self, envNode, ssmlParent, leftChild):
        args, contents = seperateContents(envNode)

        elemList = self.db.getEnvConversion(envNode.name)
        if not elemList:
            self._parseNodes(contents, ssmlParent, leftChild=leftChild)
        else:
            self._resolveEnvironmentElements(envNode, ssmlParent, elemList, leftChild)

        return elemList

    '''
    Recursively resolves non-node SSMLElements within elemList with respect to 
        envNode.
    '''
    def _resolveCmdElements(self, cmdNode, elemListParent, elemList, leftChild):
        if len(elemList) > 0:
            offset = 0
            i = 0
            for k in range(len(elemList)):
                if not isinstance(elemList[i], SSMLElementNode):
                    elem = elemList.pop(i)
                    nextOffset = -1
                    newInd = i
                    if isinstance(elem, ArgElement):
                        contents = self._getArg(cmdNode, elem).contents
                        newInd = self._parseNodes(contents, elemListParent, ssmlChildren=elemList, insertIndex=i, leftChild=leftChild)
                    elif isinstance(elem, TextElement):
                        text = elem.getHeadText()
                        if leftChild:
                            leftChild.appendTailText(text)
                        else:
                            elemListParent.appendHeadText(text)
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")

                    nextOffset += newInd - i
                    offset += nextOffset
                else:
                    self._resolveCmdElements(cmdNode, elemList[i], elemList[i].children, None)
                
                i = (k + 1) + offset
                if i > 0:
                    leftChild = elemList[i-1]

    '''
    Handles command parsing, returning the result of its parsing or 
        or none of no appropriate definition is found.
    '''
    def _parseCommand(self, cmdNode, ssmlParent, leftChild):
        args, _ = seperateContents(cmdNode)
        
        elemList = None
        if len(self.envStack) > 0 and cmdNode.name in self.envStack[-1]:
            elemList = self.envStack[-1][cmdNode.name]
        else:
            elemList = self.db.getCmdConversion(cmdNode.name)
        
        if elemList:
            self._resolveCmdElements(cmdNode, ssmlParent, elemList, leftChild)

        return elemList

    '''
    Main entry point to all parsing. Parses wih respect to a list of TexSoup
        nodes, a parent SSMLElementNode and its children. The children don't 
        necessarily correspond to the parent's actual list of children in 
        order to facilitate processing seperate lists of nodes.
    '''
    def _parseNodes(self, texNodes: list, ssmlParent: SSMLElementNode, ssmlChildren=None, insertIndex=0, leftChild=None):
        if ssmlChildren is None:
            ssmlChildren = ssmlParent.children
        for texNode in texNodes:
            parseOut = None
            if insertIndex > 0:
                leftChild = ssmlChildren[insertIndex-1]

            if exprTest(texNode, TexSoup.data.TexEnv):
                parseOut = self._parseEnvironment(texNode, ssmlParent, leftChild)
            elif exprTest(texNode, TexSoup.data.TexCmd):
                parseOut = self._parseCommand(texNode, ssmlParent, leftChild)
            elif exprTest(texNode, TexSoup.data.Token):
                text = str(texNode)
                if leftChild:
                    leftChild.appendTailText(text)
                else:
                    ssmlParent.appendHeadText(text)
            
            if parseOut:
                for ssmlChild in parseOut:
                    ssmlChildren.insert(insertIndex, ssmlChild)
                    insertIndex += 1

            if insertIndex > 0:
                leftChild = ssmlChildren[insertIndex-1]
        return insertIndex

    def _printTreeSub(self, tree, level, levelArr, atIndex, parentIndex):
        if len(levelArr) == level:
            levelArr.append([])
        levelArr[level].append(str(parentIndex) + ' -> ' + str(tree))
        for i, child in enumerate(tree.children):
            self._printTreeSub(child, level+1, levelArr, i, atIndex)

    '''
    Basic print method to see whats happening within the tree
    '''
    def printTree(self, tree):
        levelArr = []
        self._printTreeSub(tree, 0, levelArr, 0, -1)
        for level in levelArr:
            print(level)

    '''
    Parse doc with respect to the database the parser was initialized with.
    '''
    def parse(self, doc: TexSoup.data.TexNode):
        tree = RootElement()
        self._parseNodes(doc.contents, tree)
        return tree
