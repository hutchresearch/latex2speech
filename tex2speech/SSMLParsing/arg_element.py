from ssml_element import SSMLElement

class ArgElement(SSMLElement):
    def __init__(self, parent, argNum):
        super.__init__(parent)
        self.argNum = argNum

    def _update(self, node: SSMLElement):
        raise RuntimeError('Arg element can\'t be in SSML tree')

    def _getXMLElement(self):
        raise RuntimeError('Arg element can\'t be in SSML tree')

    def getArgNum(self):
        return self.argNum