class SSMLElement:
    def __init__(self):
        self.headText = None
        self.tailText = None

    def setHeadText(self, text):
        self.headText = text

    def getHeadText(self):
        return self.headText

    def setTailText(self, text):
        self.tailText = text

    def getTail(self):
        return self.tailText
