import unittest
from unittest.mock import patch, Mock
import xml.etree.ElementTree as ET

import TexSoup

from SSMLParsing.text_element import TextElement
from SSMLParsing.root_element import RootElement
from SSMLParsing.break_element import BreakElement
from SSMLParsing.content_element import ContentElement
from SSMLParsing.emphasis_element import EmphasisElement
from SSMLParsing.prosody_element import ProsodyElementVolume
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
        # TESTING REMOVE LATER
        print()
        ET.dump(ssmlParseTree.getXMLTree())

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

        # TESTING REMOVE LATER
        print()
        ET.dump(ssmlParseTree.getXMLTree())

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
        # TESTING REMOVE LATER
        print()
        ET.dump(ssmlParseTree.getXMLTree())

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

    '''
    Prosody <prosody attribute = "value"></prosody>
        <prosody volume = ""></prosody>
            - default (regular)
            - silent, x-soft, soft, medium, loud, x-loud. Sets volume
            - +ndB, -ndB : Changes volume relative to the current
              level. A value of +0dB means no change, +6dB means
              approximately twice the current volume and -6dB means
              approsimately half the current volume
        <prosody rate = ""></prosody>
            - x-slow, slow, medium, fast, x-fast. Sets pitch  
            - n% a non negative percentage change in the speaking rate
              For example, a value of 100% means no change in speaking 
              rate, a value of 200% means twice the default rate, value
              of 50% means a speaking rate of half the default rate.
              This value has a range of 20-200%
        <prosody pitch = ""></prosody>
            - deafult (regular)
            - x-low, low, medium, high, x-hgih. Sets pitch
            - +n% or -n% adjusts pitch by a relative percentage. For
              example, a value of +0% means no baseline pitch change, +5%
              gives a little higher baseline pitch, and -5% results in a lower
              baseline pitch
        <prosody amazon:max-duration = "2s"></prosody>
            - "n"s maximum duration in seconds
            - "n"ms maximum duration in milliseconds
    '''
    @patch('conversion_db.ConversionDB')
    def testProsodyElementVolume(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            # Testing basic nested prosody volume resolution
            if cmd == 'a':
                a = [ProsodyElementVolume(volume='x-loud')]
                a[0].appendChild(ProsodyElementVolume(volume='medium'))
                return a
            # Testing more complex nested prosody volume resolution
            elif cmd == 'c':
                c = [ProsodyElementVolume(volume='x-loud')]
                c[0].setHeadText('text 1')
                c[0].appendChild(ProsodyElementVolume(level='medium'))
                return c
            else:
                return None

        def mockEnvConversion(env):
            # Testing basic nested prosody resolution
            if env == 'b':
                b = [ProsodyElementVolume(volume='x-strong'), ProsodyElementVolume(volume='default')]
                b[0].appendChild(ContentElement())
                b[1].appendChild(ProsodyElementVolume(volume='x-weak'))
                return b
            # Testing more complex nested prosody resolution
            elif env == 'd':
                d = [ProsodyElementVolume(volume='x-strong')]
                d[0].appendChild(BreakElement())
                d[0].appendChild(ProsodyElementVolume(volume='x-weak'))        
                d[0].appendChild(ContentElement())
                return d
            else:
                return None

        def mockEnvDefinition(env):
            # Simple override for both environments
            if env == 'b' or env == 'd':
                return {'a': [ProsodyElementVolume(volume='medium')]}
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
        # TESTING REMOVE LATER
        print()
        ET.dump(ssmlParseTree.getXMLTree())

        # Check resulting tree structure
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 8)
        
        # \a
        self.assertIsInstance(ssmlParseTree.children[0], ProsodyElementVolume)
        self.assertEqual(ssmlParseTree.children[0].getVolume(), '+3dB')
        self.assertEqual(len(ssmlParseTree.children[0].children), 0)

        # \begin{b}\a\end{a}
        self.assertIsInstance(ssmlParseTree.children[1], ProsodyElementVolume)
        self.assertEqual(ssmlParseTree.children[1].getVolume(), '+6dB')
        self.assertEqual(len(ssmlParseTree.children[1].children), 0)

        self.assertIsInstance(ssmlParseTree.children[2], ProsodyElementVolume)
        self.assertEqual(ssmlParseTree.children[2].getVolume(), '+0dB')
        self.assertEqual(len(ssmlParseTree.children[2].children), 0)

        # \c
        self.assertIsInstance(ssmlParseTree.children[3], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[3].getVolume(), '+6dB')
        self.assertIsEqual(ssmlParseTree.children[3].getHeadText(), 'text 1')

        self.assertIsInstance(ssmlParseTree.children[4], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[4].getVolume(), '+3dB')
        self.assertIsNone(ssmlParseTree.children[4].getHeadText())
        self.assertIsEqual(len(ssmlParseTree.children[4].children), 0)

        # \begin{d}\a\end{d}
        self.assertIsInstance(ssmlParseTree.children[5], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[5].getVolume(), '+6dB')
        self.assertIsEqual(len(ssmlParseTree.children[5].children), 1)
        self.assertIsInstance(ssmlParseTree.children[5].children[0], BreakElement)

        self.assertIsInstance(ssmlParseTree.children[6], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[6].getVolume(), '+0dB')
        self.assertIsEqual(len(ssmlParseTree.children[6].children), 0)

        self.assertIsInstance(ssmlParseTree.children[7], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[7].getVolume(), '+6dB')
        self.assertIsEqual(len(ssmlParseTree.children[7].children), 0)

        # Testing with mix of dB and selected voice
        def mockCmdConversion(cmd):
                # Testing basic nested prosody volume resolution
            if cmd == 'a':
                a = [ProsodyElementVolume(volume='x-soft')]
                a[0].appendChild(ProsodyElementVolume(volume='+4dB'))
                return a
            # Testing more complex nested prosody volume resolution
            elif cmd == 'c':
                c = [ProsodyElementVolume(volume='silent')]
                c[0].setHeadText('text 1')
                c[0].appendChild(ProsodyElementVolume(level='+5dB'))
                return c
            else:
                return None

        def mockEnvConversion(env):
            # Testing basic nested prosody resolution
            if env == 'b':
                b = [ProsodyElementVolume(volume='+2dB'), ProsodyElementVolume(volume='-1dB')]
                b[0].appendChild(ContentElement())
                b[1].appendChild(ProsodyElementVolume(volume='-3dB'))
                return b
            # Testing more complex nested prosody resolution
            elif env == 'd':
                d = [ProsodyElementVolume(volume='loud')]
                d[0].appendChild(BreakElement())
                d[0].appendChild(ProsodyElementVolume(volume='-1dB'))        
                d[0].appendChild(ContentElement())
                return d
            else:
                return None

        def mockEnvDefinition(env):
            # Simple override for both environments
            if env == 'b' or env == 'd':
                return {'a': [ProsodyElementVolume(volume='medium')]}
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
        # TESTING REMOVE LATER
        print()
        ET.dump(ssmlParseTree.getXMLTree())

        # Check resulting tree structure
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 8)
        
        # \a
        self.assertIsInstance(ssmlParseTree.children[0], ProsodyElementVolume)
        self.assertEqual(ssmlParseTree.children[0].getVolume(), '-1dB')
        self.assertEqual(len(ssmlParseTree.children[0].children), 0)

        # \begin{b}\a\end{a}
        self.assertIsInstance(ssmlParseTree.children[1], ProsodyElementVolume)
        self.assertEqual(ssmlParseTree.children[1].getVolume(), '')
        self.assertEqual(len(ssmlParseTree.children[1].children), 0)

        self.assertIsInstance(ssmlParseTree.children[2], ProsodyElementVolume)
        self.assertEqual(ssmlParseTree.children[2].getVolume(), '')
        self.assertEqual(len(ssmlParseTree.children[2].children), 0)

        # \c
        self.assertIsInstance(ssmlParseTree.children[3], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[3].getVolume(), '')
        self.assertIsEqual(ssmlParseTree.children[3].getHeadText(), 'text 1')

        self.assertIsInstance(ssmlParseTree.children[4], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[4].getVolume(), '')
        self.assertIsNone(ssmlParseTree.children[4].getHeadText())
        self.assertIsEqual(len(ssmlParseTree.children[4].children), 0)

        # \begin{d}\a\end{d}
        self.assertIsInstance(ssmlParseTree.children[5], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[5].getVolume(), '')
        self.assertIsEqual(len(ssmlParseTree.children[5].children), 1)
        self.assertIsInstance(ssmlParseTree.children[5].children[0], BreakElement)

        self.assertIsInstance(ssmlParseTree.children[6], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[6].getVolume(), '')
        self.assertIsEqual(len(ssmlParseTree.children[6].children), 0)

        self.assertIsInstance(ssmlParseTree.children[7], ProsodyElementVolume)
        self.assertIsEqual(ssmlParseTree.children[7].getVolume(), '')
        self.assertIsEqual(len(ssmlParseTree.children[7].children), 0)

        # Test cases for prosody -> A lot (Might need a different function for each attribute) Only weird if there is nested resolution (not sure if we will impelement it yet, whatJacob is doing for emphasis). -> Assume we will be doing it since the custoemr asked us to do it

        # When the mocks are happenign you have to return mock objects
        # Convert previous janky xml into the new format
        # Update XML
            # Design XML documentation

        # For each node
            # Looks at child but if has emphasis fine
            # Look at next, possibly creates new node, reaches up to the parent, modifies the list of children, then leave, now it's the parents turn

    @patch('conversion_db.ConversionDB')
    def testProsodyElementRate(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

    @patch('conversion_db.ConversionDB')
    def testProsodyElementPitch(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

    @patch('conversion_db.ConversionDB')
    def testProsodyElementMaxDura(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

if __name__ == "__main__":
    unittest.main()