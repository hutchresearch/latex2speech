from SSMLParsing.ssml_element import SSMLElement

'''Simple wrapper for when text can't be placed to an adjacent node'''
class TextElement(SSMLElement):
    def __init__(self, text):
        super().__init__()
        self.setHeadText(text)
