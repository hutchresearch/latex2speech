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

    def _getSSMLElement(self, xml_node):
        element = None
        if xml_node.tag == 'break':
            args = {}
            if 'time' in xml_node.attrib:
                args['time'] = xml_node.attrib['time']
            if 'strength' in xml_node.attrib:
                args['strength'] = xml_node.attrib['strength']
            element = BreakElement(**args)
        elif xml_node.tag == 'emphasis':
            args = {}
            if 'level' in xml_node.attrib:
                args['level'] = xml_node.attrib['level']
            element = EmphasisElement(**args)
        elif xml_node.tag == 'prosody':
            args = {}
            if 'volume' in xml_node.attrib:
                args['volume'] = xml_node.attrib['volume']
            if 'rate' in xml_node.attrib:
                args['rate'] = xml_node.attrib['rate']
            if 'pitch' in xml_node.attrib:
                args['pitch'] = xml_node.attrib['pitch']
            if 'duration' in xml_node.attrib:
                args['duration'] = xml_node.attrib['duration']
            element = ProsodyElement(**args)
        elif xml_node.tag == 'p':
            element = ParagraphElement()
        elif xml_node.tag == 'arg':
            if 'argType' in xml_node.attrib:
                element = ArgElement(xml_node.attrib['num'], argType=xml_node.attrib['argType'])
            else:
                element = ArgElement(xml_node.attrib['num'])
        elif xml_node.tag == 'content':
            element = ContentElement()
        else:
            raise RuntimeError('Unhandled tag "' + xml_node.tag + '"encountered in conversion database')

        if element:
            if xml_node.text and not xml_node.text.isspace():
                element.setHeadText(xml_node.text.strip(" \t\n\r"))
            if xml_node.tail and not xml_node.tail.isspace():
                element.setTailText(xml_node.tail.strip(" \t\n\r"))
            for child in xml_node.findall('./*'):
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
                env_conv = env.find('says')
                if env_conv is not None:
                    conversion = []
                    if env_conv.text and not env_conv.text.isspace():
                        conversion.append(TextElement(env_conv.text.strip(" \t\n\r")))
                    for elem in env_conv.findall('./*'):
                        conversion.append(self._getSSMLElement(elem))
                break
        return conversion

    def getEnvDefinition(self, name: str) -> dict:
        definition = None
        for env in self.db.findall('./env'):
            if env.attrib['name'] == name:
                env_def = env.find('defines')
                env_type = env.attrib['type']

                definition = {}
                definition['readTable'] = False
                definition['mathmode'] = False

                if str(env_type) == 'mathmode':
                    definition['mathmode'] = True

                if str(env_type) == 'readTable':
                    definition['readTable'] = True

                if env_def:
                    definition = {}
                    for cmd in env_def.findall('cmd'):
                        cmd_def = []
                        if cmd.text and not cmd.text.isspace():
                            cmd_def.append(TextElement(cmd.text.strip(" \t\n\r")))
                        for elem in cmd.findall('./*'):
                            cmd_def.append(self._getSSMLElement(elem))

                        definition[cmd.attrib['name']] = cmd_def
                break

        return definition
