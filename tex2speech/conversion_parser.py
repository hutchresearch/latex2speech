import TexSoup
from conversion_db import ConversionDB

class ConversionParser:
    def __init__(self, db: ConversionDB):
        self.db = db

    def _generateSSMLTree(self):
        pass

    def parse(self, doc: TexSoup.data.TexNode):
        pass