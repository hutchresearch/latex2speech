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
