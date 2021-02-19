from SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

class ProsodyElement(SSMLElementNode):
    def __init__(self):
        super().__init__()

    def _update(self):
        pass

    def _getXMLElement(self):
        pass

    def __str__(self):
        a = "ProsodyElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
