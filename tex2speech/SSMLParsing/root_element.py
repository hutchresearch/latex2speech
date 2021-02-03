from ssml_element import SSMLElement

class RootElement(SSMLElement):
    def __init__(self, parent):
        super.__init__(parent)

    def _update(self, node: SSMLElement):
        pass

    def _getXMLElement(self):
        pass