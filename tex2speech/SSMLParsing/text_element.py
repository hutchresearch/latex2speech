from SSMLParsing.ssml_element import SSMLElement

'''Simple wrapper for when text can't be placed to an adjacent node'''
class TextElement(SSMLElement):
    def __init__(self, parent, text):
        super.__init__(parent)
        self.setHeadText(text)

    def _update(self, node: SSMLElement):
        raise RuntimeError('Text element can\'t be in SSML tree')

    def _getXMLElement(self):
        raise RuntimeError('Text element can\'t be in SSML tree')