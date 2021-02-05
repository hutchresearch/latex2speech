
# NOTE: I can't give type hints here since most of these functions take 
# SSML element objects as arguments, and python freaks out when I do that :/
class SSMLElement:
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.headText = None
        self.tailText = None

    def _update(self, node):
        raise NotImplementedError()

    def update(self, node):
        self._update(node)

    def _getXMLElement(self):
        raise NotImplementedError()

    def getXMLTree(self):
        elem = self._getXMLElement()
        for child in children:
            elem.append(child.getXMLTree)
        return elem

    def appendChild(self, node):
        self.children.append(node)

    def setHeadText(self, text):
        self.headText = text

    def getHeadText(self):
        return self.headText

    def setTailText(self, text):
        self.tailText = text

    def getTail(self):
        return self.tailText
