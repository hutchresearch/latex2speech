from SSMLParsing.ssml_element import SSMLElement
import xml.etree.ElementTree as ET
import copy

class SSMLElementNode(SSMLElement):
    def __init__(self):
        super().__init__()
        self.children = []
        self.parent = None

    def insertChild(self, i, node):
        self.children.insert(i, node)
        if isinstance(node, SSMLElementNode):
            node.setParent(self)

    def getIndexOfChild(self, child):
        i = 0
        while i < len(self.children) and self.children[i] != child:
            i += 1
        if i == len(self.children):
            i = None
        return i

    def setParent(self, parent):
        self.parent = parent

    def _update(self):
        raise NotImplementedError()

    def update(self):
        for child in self.children:
            child.update()
        if len(self.children) > 0:
            self._update()

    def _getHeadTag(self):
        raise NotImplementedError()

    def _getTailTag(self):
        raise NotImplementedError()

    def getString(self):
        string = self._getHeadTag()
        string += " " + self.getHeadText()
        for child in self.children:
            string += " " + child.getString()
        string += " " + self._getTailTag()
        string += " " + self.getTailText()
        return string
