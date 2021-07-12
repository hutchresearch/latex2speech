from app.SSMLParsing.ssml_element import SSMLElement

class ContentElement(SSMLElement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        a = "ContentElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
