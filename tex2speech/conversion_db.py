from SSMLParsing.ssml_element import SSMLElement
import xml.etree.ElementTree as ET

class ConversionDB:
    def __init__(self, xmlFile):
        self.db = ET.parse(xmlFile)

    def getCmdConversion(self, name: str) -> list:
        self.db.find('./'+name)

    def getEnvConversion(self, name: str) -> list:
        pass

    def getEnvCommands(self, name: str) -> dict:
        pass