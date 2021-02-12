class ArgElement(SSMLElement):
    def __init__(self, argNum):
        super().__init__()
        self.argNum = argNum

    def _update(self, node):
        raise RuntimeError('Arg element can\'t be in SSML tree')

    def _getXMLElement(self):
        raise RuntimeError('Arg element can\'t be in SSML tree')

    def getArgNum(self):
        return self.argNum