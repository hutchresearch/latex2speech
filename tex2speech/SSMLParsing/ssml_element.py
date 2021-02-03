class SSMLElement:
    def __init__(self, parent):
        self.parent = parent
        self.children = []

    def _update(self, node: SSMLElement):
        raise NotImplementedError()

    def update(self, node: SSMLElement):
        self._update(node)

    def _getXMLElement(self):
        raise NotImplementedError()

    def getXMLTree(self):
        elem = self._getXMLElement()
        for child in children:
            elem.appendChild(child.getXMLTree)
        return elem

    def appendChild(self, node: SSMLElement):
        self.children.append(node)
