import unittest
from unittest.mock import patch, Mock

import TexSoup

from SSMLParsing.text_element import TextElement
from SSMLParsing.root_element import RootElement
from SSMLParsing.break_element import BreakElement
from SSMLParsing.content_element import ContentElement
from SSMLParsing.emphasis_element import EmphasisElement
import conversion_db
from conversion_parser import ConversionParser

class testConversionParser(unittest.TestCase):
    @patch('conversion_db.ConversionDB')
    def testTextElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                return [TextElement('text 1')]
            else:
                return None

        def mockEnvConversion(env):
            if env == 'b':
                return [TextElement('text 2'), ContentElement()]
            else:
                return None

        def mockEnvDefinition(env):
            if env == 'b':
                return {'a': [TextElement('text 3')]}
            else:
                return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a\begin{b}\a\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc)

        # Check resulting tree structure
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 0)
        
        self.assertEqual(ssmlParseTree.getHeadText(), 'text 1 text 2 text 3')

    @patch('conversion_db.ConversionDB')
    def testBreakElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                return [BreakElement(time='3ms')]
            else:
                return None
        
        def mockEnvConversion(env):
            if env == 'b':
                return [BreakElement(strength='strong'), ContentElement(), BreakElement(strength='weak')]
            else:
                return None

        def mockEnvDefinition(env):
            if env == 'b':
                return {'a': [BreakElement(time='5ms', strength='x-weak')]}
            else:
                return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a\begin{b}\a\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc)

        # Check resulting tree structure
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 4)
        
        self.assertIsInstance(ssmlParseTree.children[0], BreakElement)
        self.assertEqual(ssmlParseTree.children[0].getTime(), '3ms')
        self.assertEqual(ssmlParseTree.children[0].getStrength(), None)

        self.assertIsInstance(ssmlParseTree.children[1], BreakElement)
        self.assertEqual(ssmlParseTree.children[1].getTime(), None)
        self.assertEqual(ssmlParseTree.children[1].getStrength(), 'strong')
        
        self.assertIsInstance(ssmlParseTree.children[2], BreakElement)
        self.assertEqual(ssmlParseTree.children[2].getTime(), '5ms')
        self.assertEqual(ssmlParseTree.children[2].getStrength(), 'x-weak')

        self.assertIsInstance(ssmlParseTree.children[3], BreakElement)
        self.assertEqual(ssmlParseTree.children[3].getTime(), None)
        self.assertEqual(ssmlParseTree.children[3].getStrength(), 'weak')

    @patch('conversion_db.ConversionDB')
    def testEmphasisElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            # Testing basic nested emphasis resolution
            if cmd == 'a':
                a = [EmphasisElement(level='strong')]
                a[0].appendChild(EmphasisElement(level='weak'))
                return a
            # Testing more complex nested emphasis resolution
            elif cmd == 'c':
                c = [EmphasisElement(level='strong')]
                c[0].setHeadText('text 1')
                c[0].appendChild(EmphasisElement(level='weak'))
                return c
            else:
                return None

        def mockEnvConversion(env):
            # Testing basic nested emphasis resolution
            if env == 'b':
                b = [EmphasisElement(level='x-strong'), EmphasisElement(level='default')]
                b[0].appendChild(ContentElement())
                b[1].appendChild(EmphasisElement(level='x-weak'))
                return b
            # Testing more complex nested emphasis resolution
            elif env == 'd':
                d = [EmphasisElement(level='x-strong')]
                d[0].appendChild(BreakElement())
                d[0].appendChild(EmphasisElement(level='x-weak'))        
                d[0].appendChild(ContentElement())
                return d
            else:
                return None

        def mockEnvDefinition(env):
            # Simple override for both environments
            if env == 'b' or env == 'd':
                return {'a': [EmphasisElement(level='weak')]}
            else:
                return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a\begin{b}\a\end{b}\c\begin{d}\a\end{d}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc)
        parser.printTree(ssmlParseTree)

        # Check resulting tree structure
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 8)
        
        # \a
        self.assertIsInstance(ssmlParseTree.children[0], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[0].getLevel(), 'default')
        self.assertEqual(len(ssmlParseTree.children[0].children), 0)

        # \begin{b}\a\end{a}
        self.assertIsInstance(ssmlParseTree.children[1], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[1].getLevel(), 'strong')
        self.assertEqual(len(ssmlParseTree.children[1].children), 0)

        self.assertIsInstance(ssmlParseTree.children[2], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[2].getLevel(), 'x-weak')
        self.assertEqual(len(ssmlParseTree.children[2].children), 0)

        # \c
        self.assertIsInstance(ssmlParseTree.children[3], EmphasisElement)
        self.assertIsEqual(ssmlParseTree.children[3].getLevel(), 'strong')
        self.assertIsEqual(ssmlParseTree.children[3].getHeadText(), 'text 1')

        self.assertIsInstance(ssmlParseTree.children[4], EmphasisElement)
        self.assertIsEqual(ssmlParseTree.children[4].getLevel(), 'default')
        self.assertIsNone(ssmlParseTree.children[4].getHeadText())
        self.assertIsEqual(len(ssmlParseTree.children[4].children), 0)

        # \begin{d}\a\end{d}
        self.assertIsInstance(ssmlParseTree.children[5], EmphasisElement)
        self.assertIsEqual(ssmlParseTree.children[5].getlevel(), 'x-strong')
        self.assertIsEqual(len(ssmlParseTree.children[5].children), 1)
        self.assertIsInstance(ssmlParseTree.children[5].children[0], BreakElement)

        self.assertIsInstance(ssmlParseTree.children[6], EmphasisElement)
        self.assertIsEqual(ssmlParseTree.children[6].getlevel(), 'default')
        self.assertIsEqual(len(ssmlParseTree.children[6].children), 0)

        self.assertIsInstance(ssmlParseTree.children[7], EmphasisElement)
        self.assertIsEqual(ssmlParseTree.children[7].getlevel(), 'x-strong')
        self.assertIsEqual(len(ssmlParseTree.children[7].children), 0)

if __name__ == "__main__":
    unittest.main()