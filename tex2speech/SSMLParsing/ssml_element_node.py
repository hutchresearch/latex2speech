class SSMLElementNode(SSMLElement):
    def __init__(self):
        super().__init__()
        self.children = []

    def appendChild(self, node):
        self.children.append(node)

    def _update(self, node):
        raise NotImplementedError()

    def update(self, node):
        self._update(node)

    def _getXMLElement(self):
        raise NotImplementedError()

    def getXMLTree(self):
        elem = self._getXMLElement()
        for child in children:
            elem.append(child.getXMLTree())
        return elem
