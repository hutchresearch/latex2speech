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

        a = [TextElement('text 1')]
        cmds = {'a': a}
        def mockCmdConversion(cmd):
            nonlocal cmds
            return cmds[cmd]
        
        b = [TextElement('text 2'), ContentElement()]
        envs = {'b': b}
        def mockEnvConversion(env):
            nonlocal envs
            return envs[env]

        a_override = [TextElement('text 3')]
        envsDefn = {'b': {'a': a_override}}
        def mockEnvDefinition(env):
            nonlocal envsDefn
            return envsDefn[env]

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
        self.assertEqual(len(ssmlParseTree.children), 3)
        
        self.assertIsInstance(ssmlParseTree.children[0], TextElement)
        self.assertEqual(ssmlParseTree.children[0].getHeadText(), 'text 1')

        self.assertIsInstance(ssmlParseTree.children[1], TextElement)
        self.assertEqual(ssmlParseTree.children[1].getHeadText(), 'text 2')

        self.assertIsInstance(ssmlParseTree.children[2], ContentElement)
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)
        
        self.assertIsInstance(ssmlParseTree.children[2].children[0], TextElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].getHeadText, 'text 3')

    @patch('conversion_db.ConversionDB')
    def testBreakElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        a = [BreakElement(time='3ms')]
        cmds = {'a': a}
        def mockCmdConversion(cmd):
            nonlocal cmds
            return cmds[cmd]
        
        b = [BreakElement(strength='strong'), ContentElement(), BreakElement(strength='weak')]
        envs = {'b': b}
        def mockEnvConversion(env):
            nonlocal envs
            return envs[env]

        a_override = [BreakElement(time='5ms', strength='x-weak')]
        envsDefn = {'b': {'a': a_override}}
        def mockEnvDefinition(env):
            nonlocal envsDefn
            return envsDefn[env]

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

        self.assertIsInstance(ssmlParseTree.children[2], ContentElement)
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)
        
        self.assertIsInstance(ssmlParseTree.children[2].children[0], BreakElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].getTime(), '5ms')
        self.assertEqual(ssmlParseTree.children[2].children[0].getStrength(), 'x-weak')

        self.assertIsInstance(ssmlParseTree.children[3], BreakElement)
        self.assertEqual(ssmlParseTree.children[3].getTime(), None)
        self.assertEqual(ssmlParseTree.children[3].getStrength(), 'weak')

    @patch('conversion_db.ConversionDB')
    def testEmphasisElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        # Testing basic nested emphasis resolution
        a = [EmphasisElement(level='strong')]
        a[0].appendChild(EmphasisElement(level='weak'))
        
        b = [EmphasisElement(level='x-strong'), EmphasisElement(level='default')]
        b[0].appendChild(ContentElement())
        b[1].appendChild(EmphasisElement(level='x-weak'))

        a_override = [EmphasisElement(level='weak')]

        # Testing more complex nested emphasis resolution
        # \c will resolve to the text surrounded by strong emphasis, 
        #   followed by another emphasis element with strong and weak
        #   canceled out.
        c = [EmphasisElement(level='strong')]
        c[0].setHeadText('text 1')
        c[0].appendChild(EmphasisElement(level='weak'))

        d = [EmphasisElement(level='x-strong')]
        d[0].appendChild(BreakElement())
        d[0].appendChild(EmphasisElement(level='x-weak'))        
        d[0].appendChild(ContentElement())

        cmds = {'a': a, 'c': c}
        def mockCmdConversion(cmd):
            nonlocal cmds
            return cmds[cmd]
            
        envs = {'b': b, 'd': d}
        def mockEnvConversion(env):
            nonlocal envs
            return envs[env]

        envsDefn = {'b': {'a': a_override}, 'd': {'a': a_override}}
        def mockEnvDefinition(env):
            nonlocal envsDefn
            return envsDefn[env]

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a\begin{b}\a\end{b}\c\begin{d}\a\end{d}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc)

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