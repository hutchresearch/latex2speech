from SSMLParsing.ssml_element import SSMLElement

class ContentElement(SSMLElement):
    def __init__(self, parent):
        super.__init__(parent)

    def _update(self, node: SSMLElement):
        raise RuntimeError('Content element can\'t be in SSML tree')

    def _getXMLElement(self):
        raise RuntimeError('Content element can\'t be in SSML tree')