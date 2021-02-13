from SSMLParsing.ssml_element_node import SSMLElementNode

class RootElement(SSMLElementNode):
    def __init__(self):
        super().__init__()

    def _update(self, node: SSMLElementNode):
        pass

    def _getXMLElement(self):
        pass
