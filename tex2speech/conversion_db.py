class ConversionDB:
    def getCmdConv(self, name: str) -> list[SSMLElement]:
        raise NotImplementedError()

    def getEnvConv(self, env: str) -> list[SSMLElement]:
        raise NotImplementedError()

class XMLConversionDB(ConversionDB):
    def __init__(self, xmlFile: file):
        pass

    def getCmdConv(self, name: str) -> list[SSMLElement]:
        pass
