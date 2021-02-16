from SSMLParsing.ssml_element_node import SSMLElementNode

class EmphasisElement(SSMLElementNode):
    def __init__(self, level=None):
        super().__init__()
        self.level = level

    def _update(self, node: SSMLElementNode):
        pass

    def _getXMLElement(self):
        pass

    def getLevel(self):
        return self.level

    def __str__(self):
        a = "EmphasisElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
