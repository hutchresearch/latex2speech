import TexSoup
from conversion_db import ConversionDB

class ConversionParser:
    def __init__(self, doc: TexSoup.data.TexNode, db: ConversionDB):
        self.doc = doc
        self.db = db

    def _generateSSMLTree(self):
        pass

    def parse(self):
        pass