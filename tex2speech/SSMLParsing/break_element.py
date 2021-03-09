from SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

class BreakElement(SSMLElementNode):
    def __init__(self, time=None, strength=None):
        super().__init__()
        self.time = time
        self.strength = strength

    def _update(self):
        pass

    def _getXMLElement(self):
        attrib = {}
        if self.time:
            attrib['time'] = self.time
        if self.strength:
            attrib['strength'] = self.strength
        elem = ET.Element('break', attrib=attrib)
        if self.getHeadText() != '':
            elem.text = self.getHeadText()
        if self.getTailText() != '':
            print("HERE? " + str(self.getTailText()))
            elem.tail = self.getTailText()
            print("TESTING AGAIN " + str(elem.tail))
        return elem

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
