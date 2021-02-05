from SSMLParsing.ssml_element import SSMLElement

class BreakElement(SSMLElement):
    def __init__(self, parent, time=None, strength=None):
        super.__init__(parent)
        self.time = time
        self.strength = strength

    def _update(self, node: SSMLElement):
        pass

    def _getXMLElement(self):
        pass

    def getTime(self):
        return self.time
    
    def getStrength(self):
        return self.strength