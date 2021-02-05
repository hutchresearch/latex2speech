from SSMLParsing.ssml_element import SSMLElement

class ConversionDB:
    def getCmdConv(self, name: str) -> list:
        raise NotImplementedError()

    def getEnvConv(self, name: str) -> list:
        raise NotImplementedError()
    
    def getEnvCommands(self, name: str) -> dict:
        pass

class XMLConversionDB(ConversionDB):
    def __init__(self, xmlFile):
        pass

    def getCmdConversion(self, name: str) -> list:
        pass

    def getEnvConversion(self, name: str) -> list:
        pass

    def getEnvCommands(self, name: str) -> dict:
        pass