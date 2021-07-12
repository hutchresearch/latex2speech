from app.SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

class ParagraphElement(SSMLElementNode):
    def __init__(self):
        super().__init__()

    def _update(self):
        pass

    def _getXMLElement(self):
        elem = ET.Element('p')
        if self.getHeadText() != '':
            elem.text = self.getHeadText()
        if self.getTailText() != '':
            elem.tail = self.getTailText()
        return elem

    def _getHeadTag(self):
        return "<p>"

    def _getTailTag(self):
        return "</p>"

    def __str__(self):
        a = "BreakElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
