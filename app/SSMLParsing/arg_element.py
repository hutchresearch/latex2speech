from SSMLParsing.ssml_element import SSMLElement

class ArgElement(SSMLElement):
    def __init__(self, argNum, argType='brace'):
        super().__init__()
        self.argNum = int(argNum)
        self.argType = argType

    def getArgNum(self):
        return self.argNum

    def getArgType(self):
        return self.argType
    
    def __str__(self):
        a = "ArgElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
