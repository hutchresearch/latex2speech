from SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

class EmphasisElement(SSMLElementNode):
    def __init__(self, level=None):
        super().__init__()
        self.level = level
        self.levels = ['none', 'reduced', 'moderate', 'strong']
        self.levelIndex = {'none': 0, 'reduced': 1, 'moderate': 2, 'strong': 3}

    def _levelDiff(self, nestedLevel):
        mid = (self.levelIndex[self.level] + self.levelIndex(nestedLevel))/2
        return self.levels[mid]

    def _update(self):
        for i, child in enumerate(self.children):
            if isinstance(child, EmphasisElement):
                newLevel = self._levelDiff(child.getLevel())

    def _getXMLElement(self):
        attrib = {}
        if self.level:
            attrib['level'] = self.level
        elem = ET.Element('emph', attrib=attrib)
        if self.getHeadText() != '':
            elem.text = self.getHeadText()
        if self.getTailText() != '':
            elem.tail = self.getTailText()
        return elem

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
