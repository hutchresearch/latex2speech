from app.SSMLParsing.ssml_element import SSMLElement

'''Simple wrapper for when text can't be placed to an adjacent node'''
class TextElement(SSMLElement):
    def __init__(self, text):
        super().__init__()
        self.setHeadText(text)

    def __str__(self):
        a = "TextElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
