import xml.etree.ElementTree as ET

from SSMLParsing.arg_element import ArgElement
from SSMLParsing.break_element import BreakElement
from SSMLParsing.content_element import ContentElement
from SSMLParsing.emphasis_element import EmphasisElement
from SSMLParsing.prosody_element import ProsodyElement
from SSMLParsing.paragraph_element import ParagraphElement
from SSMLParsing.root_element import RootElement
from SSMLParsing.ssml_element_node import SSMLElementNode
from SSMLParsing.ssml_element import SSMLElement
from SSMLParsing.text_element import TextElement

class ConversionDB:
    def __init__(self, xmlFile):
        self.db = ET.fromstring(xmlFile)

    def _getSSMLElement(self, xmlNode):
        element = None
        if xmlNode.tag == 'break':
            args = {}
            if 'time' in xmlNode.attrib:
                args['time'] = xmlNode.attrib['time']
            if 'strength' in xmlNode.attrib:
                args['strength'] = xmlNode.attrib['strength']
            element = BreakElement(**args)
        elif xmlNode.tag == 'emphasis':
            args = {}
            if 'level' in xmlNode.attrib:
                args['level'] = xmlNode.attrib['level']
            element = EmphasisElement(**args)
        elif xmlNode.tag == 'prosody':
            args = {}
            if 'volume' in xmlNode.attrib:
                args['volume'] = xmlNode.attrib['volume']
            if 'rate' in xmlNode.attrib:
                args['rate'] = xmlNode.attrib['rate']
            if 'pitch' in xmlNode.attrib:
                args['pitch'] = xmlNode.attrib['pitch']
            if 'duration' in xmlNode.attrib:
                args['duration'] = xmlNode.attrib['duration']
            element = ProsodyElement(**args)
        elif xmlNode.tag == 'p':
            element = ParagraphElement()
        elif xmlNode.tag == 'arg':
            if 'argType' in xmlNode.attrib:
                element = ArgElement(xmlNode.attrib['num'], argType=xmlNode.attrib['argType'])
            else:
                element = ArgElement(xmlNode.attrib['num'])
        elif xmlNode.tag == 'content':
            element = ContentElement()
        else:
            raise RuntimeError('Unhandled tag "' + xmlNode.tag + '"encountered in conversion database')

        if element:
            if xmlNode.text and not xmlNode.text.isspace():
                element.setHeadText(xmlNode.text.strip(" \t\n\r"))
            if xmlNode.tail and not xmlNode.tail.isspace():
                element.setTailText(xmlNode.tail.strip(" \t\n\r"))
            for child in xmlNode.findall('./*'):
                element.insertChild(-1, self._getSSMLElement(child))

        return element

    def getCmdConversion(self, name: str) -> list:
        conversion = None
        for cmd in self.db.findall('./cmd'):
            if cmd.attrib['name'] == name:
                conversion = []
                if cmd.text and not cmd.text.isspace():
                    conversion.append(TextElement(cmd.text.strip(" \t\n\r")))
                for elem in cmd.findall('./*'):
                    conversion.append(self._getSSMLElement(elem))
                break
        return conversion

    def getEnvConversion(self, name: str) -> list:
        conversion = None
        for env in self.db.findall('./env'):
            if env.attrib['name'] == name:
                envConv = env.find('says')
                if envConv is not None:
                    conversion = []
                    if envConv.text and not envConv.text.isspace():
                        conversion.append(TextElement(envConv.text.strip(" \t\n\r")))
                    for elem in envConv.findall('./*'):
                        conversion.append(self._getSSMLElement(elem))
                break
        return conversion

    def getEnvDefinition(self, name: str) -> dict:
        definition = None
        for env in self.db.findall('./env'):
            if env.attrib['name'] == name:
                envDef = env.find('defines')
                envType = env.attrib['type']

                definition = {}
                definition['readTable'] = False
                definition['mathmode'] = False

                if str(envType) == 'mathmode':
                    definition['mathmode'] = True

                if str(envType) == 'readTable':
                    definition['readTable'] = True

                if envDef:
                    definition = {}
                    
                    for cmd in envDef.findall('cmd'):
                        cmdDef = []
                        if cmd.text and not cmd.text.isspace():
                            cmdDef.append(TextElement(cmd.text.strip(" \t\n\r")))
                        for elem in cmd.findall('./*'):
                            cmdDef.append(self._getSSMLElement(elem))

                        definition[cmd.attrib['name']] = cmdDef
                break

        return definition
