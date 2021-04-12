from SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

class RootElement(SSMLElementNode):
    def __init__(self):
        super().__init__()

    def _update(self):
        pass

    def _getXMLElement(self):
        elem = ET.Element('speak')
        if self.getHeadText() != '':
            elem.text = self.getHeadText()
        if self.getTailText() != '':
            elem.tail = self.getTailText()

        return elem

    
    def _getHeadTag(self):
        # return "<speak>"
        return ''

    def _getTailTag(self):
        # return "</speak>"
        return ''

    def __str__(self):
        a = "RootElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'

        return a

    __repr__ = __str__
