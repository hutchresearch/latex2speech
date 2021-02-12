from SSMLParsing.ssml_element import SSMLElement

class ContentElement(SSMLElement):
    def __init__(self):
        super().__init__()

    def _update(self, node: SSMLElement):
        raise RuntimeError('Content element can\'t be in SSML tree')

    def _getXMLElement(self):
        raise RuntimeError('Content element can\'t be in SSML tree')