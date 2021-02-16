from SSMLParsing.ssml_element import SSMLElement

class ArgElement(SSMLElement):
    def __init__(self, argNum):
        super().__init__()
        self.argNum = int(argNum)

    def getArgNum(self):
        return self.argNum
    
    def __str__(self):
        a = "ArgElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
