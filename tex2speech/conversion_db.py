from SSMLParsing.ssml_element import SSMLElement
import xml.etree.ElementTree as ET

class ConversionDB:
    def __init__(self, xmlFile):
        self.db = ET.parse(xmlFile)

    def getCmdConversion(self, name: str) -> list:
        pass

    def getEnvConversion(self, name: str) -> list:
        pass

    def getEnvDefinition(self, name: str) -> dict:
        pass
