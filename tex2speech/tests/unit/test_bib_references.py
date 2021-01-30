import unittest
from app import app 

import tex2speech.expand_labels

class TestExpandLabels(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        return str(doc1) == str(doc2)

if __name__ == '__main__':
    unittest.main()