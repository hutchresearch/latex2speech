class SSMLElement:
    def __init__(self):
        self.headText = ''
        self.tailText = ''

    def setHeadText(self, text):
        self.headText = text

    def getHeadText(self):
        return self.headText

    def setTailText(self, text):
        self.tailText = text

    def getTailText(self):
        return self.tailText

    def appendHeadText(self, text):
        if self.headText == '':
            self.headText = text
        elif self.headText[-1] != ' ' or self.headText[-1] != '\n':
            self.headText += ' ' + text
        else:
            self.headText += text
    
    def appendTailText(self, text):
        if self.tailText == '':
            self.tailText = text
        elif self.tailText[-1] != ' ' or self.tailText[-1] != '\n':
            self.tailText += ' ' + text
        else:
            self.tailText += text