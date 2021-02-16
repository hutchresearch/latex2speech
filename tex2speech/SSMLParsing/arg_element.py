from SSMLParsing.ssml_element import SSMLElement

class ArgElement(SSMLElement):
    def __init__(self, argNum):
        super().__init__()
        self.argNum = int(argNum)

    def getArgNum(self):
        return self.argNum
