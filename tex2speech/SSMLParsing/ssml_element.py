class SSMLElement:
    def __init__(self):
        self.headText = ""
        self.tailText = ""

    def setHeadText(self, text):
        self.headText = text

    def getHeadText(self):
        return self.headText

    def setTailText(self, text):
        self.tailText = text

    def getTailText(self):
        return self.tailText
