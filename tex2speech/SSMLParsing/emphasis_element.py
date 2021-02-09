from SSMLParsing.ssml_element import SSMLElement

class EmphasisElement(SSMLElement):
    def __init__(self, level=None):
        super.__init__()
        self.level = level

    def _update(self, node: SSMLElement):
        pass

    def _getXMLElement(self):
        pass

    def getLevel(self):
        return self.level