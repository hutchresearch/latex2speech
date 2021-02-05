import TexSoup
from conversion_db import ConversionDB

class ConversionParser:
    def __init__(self, doc: TexSoup.data.TexNode, db: ConversionDB):
        self.doc = doc
        self.db = db

    def _generateSSMLTree(self):
        # TODO: Confirm if this is true:
        # If text is not in a text node, it must be in a tail node
        # and the inverse as well
        pass

    def parse(self):
        pass