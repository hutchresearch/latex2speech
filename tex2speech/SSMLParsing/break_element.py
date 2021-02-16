from SSMLParsing.ssml_element_node import SSMLElementNode

class BreakElement(SSMLElementNode):
    def __init__(self, time=None, strength=None):
        super().__init__()
        self.time = time
        self.strength = strength

    def _update(self, node: SSMLElementNode):
        pass

    def _getXMLElement(self):
        pass

    def getTime(self):
        return self.time
    
    def getStrength(self):
        return self.strength

    def __str__(self):
        a = "BreakElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
