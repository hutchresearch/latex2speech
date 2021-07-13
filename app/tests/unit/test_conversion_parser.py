import unittest
from unittest.mock import patch, Mock
import xml.etree.ElementTree as ET

import TexSoup

from SSMLParsing.text_element import TextElement
from SSMLParsing.root_element import RootElement
from SSMLParsing.break_element import BreakElement
from SSMLParsing.arg_element import ArgElement
from SSMLParsing.content_element import ContentElement
from SSMLParsing.emphasis_element import EmphasisElement
from SSMLParsing.prosody_element import ProsodyElement
import conversion_db
from conversion_parser import ConversionParser

class testConversionParser(unittest.TestCase):
    '''
    Tests basic text replacement in commands and environments.
    '''
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
                return {'a': [TextElement('text 3')], 'type': None}
            else:
                return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a\begin{b}\a\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)
        print("TESTING SSSML PARSE " + str(ssmlParseTree))
        # Check resulting tree structure
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 0)
        
        self.assertEqual(ssmlParseTree.getHeadText(), 'text 1 text 2 text 3')

    '''
    Tests the BreakElement with various attributes in both commands and
        environments.
    '''
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
                return {'a': [BreakElement(time='5ms', strength='x-weak')], 'mathmode': False}
            else:
                return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a\begin{b}\a\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)

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

    '''
    Tests the EmphasisElement with various attributes in both commands and
        environments. One important test is here is ensuring the ContentElement 
        and ArgElement work properly while being children of an EmphasisElement.
    '''
    @patch('conversion_db.ConversionDB')
    def testEmphasisElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                a = [EmphasisElement(level='strong'), ArgElement(1)]
                a[0].insertChild(0, EmphasisElement(level='reduced'))
                a[0].children[0].insertChild(0, ArgElement(2))
                return a
            else:
                return None

        def mockEnvConversion(env):
            if env == 'b':
                b = [ContentElement(), EmphasisElement(level='moderate'), ArgElement(2), EmphasisElement(level='none')]
                b[1].insertChild(0, ContentElement())
                b[1].insertChild(0, ArgElement(1))
                b[3].insertChild(0, EmphasisElement(level='strong'))
                return b
            else:
                return None

        def mockEnvDefinition(env):
            return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a{1}{2}\begin{b}{3}{4}\a{5}{6}\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)
        
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 4)

        self.assertIsInstance(ssmlParseTree.children[0], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[0].getTailText().strip(), '1')
        self.assertEqual(ssmlParseTree.children[0].getLevel(), 'strong')
        self.assertEqual(len(ssmlParseTree.children[0].children), 1)

        self.assertIsInstance(ssmlParseTree.children[0].children[0], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[0].children[0].getHeadText().strip(), '2')
        self.assertEqual(ssmlParseTree.children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[0].children[0].getLevel(), 'reduced')

        self.assertIsInstance(ssmlParseTree.children[1], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[1].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[1].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[1].getLevel(), 'strong')
        self.assertEqual(len(ssmlParseTree.children[1].children), 1)

        self.assertIsInstance(ssmlParseTree.children[1].children[0], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[1].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[1].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[1].children[0].getLevel(), 'reduced')

        self.assertIsInstance(ssmlParseTree.children[2], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[2].getHeadText().strip(), '3')
        self.assertEqual(ssmlParseTree.children[2].getTailText().strip(), '4')
        self.assertEqual(ssmlParseTree.children[2].getLevel(), 'moderate')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[2].children[0].getLevel(), 'strong')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0].children[0], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getLevel(), 'reduced')
        
        self.assertIsInstance(ssmlParseTree.children[3], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[3].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].getLevel(), 'none')
        self.assertEqual(len(ssmlParseTree.children[3].children), 1)

        self.assertIsInstance(ssmlParseTree.children[3].children[0], EmphasisElement)
        self.assertEqual(ssmlParseTree.children[3].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getLevel(), 'strong')

    '''
    Tests that arguments are properly expanded when the ArgElement object
        is used in cmd/env definitions.
    '''
    @patch('conversion_db.ConversionDB')
    def testArgElement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                a = [ArgElement(2), ArgElement('1', argType='bracket')]
                return a
            elif cmd == 'd':
                d = [BreakElement()]
                return d
            else:
                return None

        def mockEnvConversion(env):
            if env == 'b':
                b = [ArgElement(1, 'bracket'), ArgElement(4, argType='brace'), ContentElement()]
                return b
            else:
                return None

        def mockEnvDefinition(env):
            if env == 'b':
                return {'a': [ArgElement(1), ArgElement('2', argType='bracket')], \
                        'c': [ArgElement(3)], 'mathmode': False}
            else:
                return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a{1}{\a{2}[3]{\d}}[\d]\begin{b}{4}{5}[6]{7}{\a[8]{9}{10}[\d]}\d\a[11]{12}[13]\d\c{14}{15}{\d 16}\d\end{b}')
        # Should be <speak> <break/> 3 <break/> 6 9 <break/> <break/> 12 13 <break/> <break/> 16 <break/> <speak/>
        #                   ^ Cmd               ^ Env say    ^ Env contents

        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)
        
        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(ssmlParseTree.getHeadText(), '')
        self.assertEqual(len(ssmlParseTree.children), 7)

        self.assertIsInstance(ssmlParseTree.children[0], BreakElement)
        self.assertEqual(ssmlParseTree.children[0].getTailText().strip(), '3')

        self.assertIsInstance(ssmlParseTree.children[1], BreakElement)
        self.assertEqual(ssmlParseTree.children[1].getTailText().strip().replace("  ", " "), '6 9')

        self.assertIsInstance(ssmlParseTree.children[2], BreakElement)
        self.assertEqual(ssmlParseTree.children[2].getTailText(), '')

        self.assertIsInstance(ssmlParseTree.children[3], BreakElement)
        self.assertEqual(ssmlParseTree.children[3].getTailText().strip().replace("  ", " "), '12 13')

        self.assertIsInstance(ssmlParseTree.children[4], BreakElement)
        self.assertEqual(ssmlParseTree.children[4].getTailText(), '')

        self.assertIsInstance(ssmlParseTree.children[5], BreakElement)
        self.assertEqual(ssmlParseTree.children[5].getTailText(), ' 16')

        self.assertIsInstance(ssmlParseTree.children[6], BreakElement)
        self.assertEqual(ssmlParseTree.children[6].getTailText(), '')
    
    '''
    Testing environments and ensuring undefined environments still have
        their contents read out, while defined environments without the content
        tag are not.
    '''
    @patch('conversion_db.ConversionDB')
    def testEnvironments(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                a = [TextElement('text1')]
                return a
            else:
                return None

        def mockEnvConversion(env):
            if env == 'a':
                a = [TextElement('text2')]
                return a
            if env == 'b':
                b = [ContentElement()]
                return b
            else:
                return None

        def mockEnvDefinition(env):
            if env == 'b':
                return {'a': [TextElement('text3')], 'mathmode': False}
            else:
                return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\begin{a}\a\end{a}\begin{c}\begin{a}\a\end{a}\end{c}\begin{c}\begin{b}\a\end{b}\end{c}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)

        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 0)
        self.assertEqual(ssmlParseTree.getHeadText().strip().replace("  ", " "), 'text2 text2 text3')
    
    '''
    Prosody <prosody attribute = "value"></prosody>
        <prosody volume = ""></prosody>
            - default (regular)
            - silent, x-soft, soft, medium, loud, x-loud. Sets volume
            - +ndB, -ndB : Changes volume relative to the current
              level. A value of +0dB means no change, +6dB means
              approximately twice the current volume and -6dB means
              approsimately half the current volume
    '''
    @patch('conversion_db.ConversionDB')
    def testProsodyElementVolume(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                a = [ProsodyElement(volume='x-loud'), ArgElement(1)]
                a[0].insertChild(0, ProsodyElement(volume='medium'))
                a[0].children[0].insertChild(0, ArgElement(2))
                return a
            else:
                return None

        def mockEnvConversion(env):
            if env == 'b':
                b = [ContentElement(), ProsodyElement(volume='-3dB'), ArgElement(2), ProsodyElement(volume='none')]
                b[1].insertChild(0, ContentElement())
                b[1].insertChild(0, ArgElement(1))
                b[3].insertChild(0, ProsodyElement(volume='loud'))
                return b
            else:
                return None

        def mockEnvDefinition(env):
            return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a{1}{2}\begin{b}{3}{4}\a{5}{6}\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)

        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 4)

        self.assertIsInstance(ssmlParseTree.children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[0].getTailText().strip(), '1')
        self.assertEqual(ssmlParseTree.children[0].getVolume(), 'x-loud')
        self.assertEqual(len(ssmlParseTree.children[0].children), 1)

        self.assertIsInstance(ssmlParseTree.children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].children[0].getHeadText().strip(), '2')
        self.assertEqual(ssmlParseTree.children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[0].children[0].getVolume(), 'medium')

        self.assertIsInstance(ssmlParseTree.children[1], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[1].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[1].getVolume(), 'x-loud')
        self.assertEqual(len(ssmlParseTree.children[1].children), 1)

        self.assertIsInstance(ssmlParseTree.children[1].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[1].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[1].children[0].getVolume(), 'medium')

        self.assertIsInstance(ssmlParseTree.children[2], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].getHeadText().strip(), '3')
        self.assertEqual(ssmlParseTree.children[2].getTailText().strip(), '4')
        self.assertEqual(ssmlParseTree.children[2].getVolume(), '-3dB')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[2].children[0].getVolume(), 'x-loud')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getVolume(), 'medium')
        
        self.assertIsInstance(ssmlParseTree.children[3], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].getVolume(), 'medium')
        self.assertEqual(len(ssmlParseTree.children[3].children), 1)

        self.assertIsInstance(ssmlParseTree.children[3].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getVolume(), 'loud')

    ''' <prosody rate = ""></prosody>
            - x-slow, slow, medium, fast, x-fast. Sets pitch  
            - n% a non negative percentage change in the speaking rate
              For example, a value of 100% means no change in speaking 
              rate, a value of 200% means twice the default rate, value
              of 50% means a speaking rate of half the default rate.
              This value has a range of 20-200%'''
    @patch('conversion_db.ConversionDB')
    def testProsodyElementRate(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                a = [ProsodyElement(rate='slow'), ArgElement(1)]
                a[0].insertChild(0, ProsodyElement(rate='x-fast'))
                a[0].children[0].insertChild(0, ArgElement(2))
                return a
            else:
                return None

        def mockEnvConversion(env):
            if env == 'b':
                b = [ContentElement(), ProsodyElement(rate='40%'), ArgElement(2), ProsodyElement(rate='none')]
                b[1].insertChild(0, ContentElement())
                b[1].insertChild(0, ArgElement(1))
                b[3].insertChild(0, ProsodyElement(rate='180%'))
                return b
            else:
                return None

        def mockEnvDefinition(env):
            return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a{1}{2}\begin{b}{3}{4}\a{5}{6}\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)

        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 4)

        self.assertIsInstance(ssmlParseTree.children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[0].getTailText().strip(), '1')
        self.assertEqual(ssmlParseTree.children[0].getRate(), 'slow')
        self.assertEqual(len(ssmlParseTree.children[0].children), 1)

        self.assertIsInstance(ssmlParseTree.children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].children[0].getHeadText().strip(), '2')
        self.assertEqual(ssmlParseTree.children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[0].children[0].getRate(), 'x-fast')

        self.assertIsInstance(ssmlParseTree.children[1], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[1].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[1].getRate(), 'slow')
        self.assertEqual(len(ssmlParseTree.children[1].children), 1)

        self.assertIsInstance(ssmlParseTree.children[1].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[1].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[1].children[0].getRate(), 'x-fast')

        self.assertIsInstance(ssmlParseTree.children[2], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].getHeadText().strip(), '3')
        self.assertEqual(ssmlParseTree.children[2].getTailText().strip(), '4')
        self.assertEqual(ssmlParseTree.children[2].getRate(), '40%')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[2].children[0].getRate(), 'slow')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getRate(), 'x-fast')
        
        self.assertIsInstance(ssmlParseTree.children[3], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].getRate(), 'medium')
        self.assertEqual(len(ssmlParseTree.children[3].children), 1)

        self.assertIsInstance(ssmlParseTree.children[3].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getRate(), '180%')

    '''<prosody pitch = ""></prosody>
            - deafult (regular)
            - x-low, low, medium, high, x-hgih. Sets pitch
            - +n% or -n% adjusts pitch by a relative percentage. For
              example, a value of +0% means no baseline pitch change, +5%
              gives a little higher baseline pitch, and -5% results in a lower
              baseline pitch'''
    @patch('conversion_db.ConversionDB')
    def testProsodyElementPitch(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                a = [ProsodyElement(pitch='x-low'), ArgElement(1)]
                a[0].insertChild(0, ProsodyElement(pitch='high'))
                a[0].children[0].insertChild(0, ArgElement(2))
                return a
            else:
                return None

        def mockEnvConversion(env):
            if env == 'b':
                b = [ContentElement(), ProsodyElement(pitch='-40%'), ArgElement(2), ProsodyElement(pitch='none')]
                b[1].insertChild(0, ContentElement())
                b[1].insertChild(0, ArgElement(1))
                b[3].insertChild(0, ProsodyElement(pitch='90%'))
                return b
            else:
                return None

        def mockEnvDefinition(env):
            return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a{1}{2}\begin{b}{3}{4}\a{5}{6}\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)

        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 4)

        self.assertIsInstance(ssmlParseTree.children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[0].getTailText().strip(), '1')
        self.assertEqual(ssmlParseTree.children[0].getPitch(), 'x-low')
        self.assertEqual(len(ssmlParseTree.children[0].children), 1)

        self.assertIsInstance(ssmlParseTree.children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].children[0].getHeadText().strip(), '2')
        self.assertEqual(ssmlParseTree.children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[0].children[0].getPitch(), 'high')

        self.assertIsInstance(ssmlParseTree.children[1], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[1].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[1].getPitch(), 'x-low')
        self.assertEqual(len(ssmlParseTree.children[1].children), 1)

        self.assertIsInstance(ssmlParseTree.children[1].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[1].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[1].children[0].getPitch(), 'high')

        self.assertIsInstance(ssmlParseTree.children[2], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].getHeadText().strip(), '3')
        self.assertEqual(ssmlParseTree.children[2].getTailText().strip(), '4')
        self.assertEqual(ssmlParseTree.children[2].getPitch(), '-40%')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].getTailText().strip(), '5')
        self.assertEqual(ssmlParseTree.children[2].children[0].getPitch(), '-20%')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getHeadText().strip(), '6')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getPitch(), '+10%')
        
        self.assertIsInstance(ssmlParseTree.children[3], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].getPitch(), '+0%')
        self.assertEqual(len(ssmlParseTree.children[3].children), 1)

        self.assertIsInstance(ssmlParseTree.children[3].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getPitch(), '+90%')

    '''<prosody amazon:max-duration = "2s"></prosody>
            - "n"s maximum duration in seconds
            - "n"ms maximum duration in milliseconds'''
    @patch('conversion_db.ConversionDB')
    def testProsodyElementMaxDura(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        def mockCmdConversion(cmd):
            if cmd == 'a':
                a = [ProsodyElement(duration='2000s'), ArgElement(1)]
                a[0].insertChild(0, ProsodyElement(duration='1000s'))
                a[0].children[0].insertChild(0, ArgElement(2))
                return a
            else:
                return None

        def mockEnvConversion(env):
            if env == 'b':
                b = [ContentElement(), ProsodyElement(duration='3000ms'), ArgElement(2), ProsodyElement(duration='5000ms')]
                b[1].insertChild(0, ContentElement())
                b[1].insertChild(0, ArgElement(1))
                b[3].insertChild(0, ProsodyElement(duration='9000s'))
                return b
            else:
                return None

        def mockEnvDefinition(env):
            return None

        db.getCmdConversion = Mock(side_effect=mockCmdConversion)
        db.getEnvConversion = Mock(side_effect=mockEnvConversion)
        db.getEnvDefinition = Mock(side_effect=mockEnvDefinition)

        # Set up TexSoup parse tree to be parsed
        doc = TexSoup.TexSoup(r'\a{1}{2}\begin{b}{3}{4}\a{5}{6}\end{b}')

        # Parse on the given db and tree
        parser = ConversionParser(db)
        ssmlParseTree = parser.parse(doc, test=True)

        self.assertIsInstance(ssmlParseTree, RootElement)
        self.assertEqual(len(ssmlParseTree.children), 4)

        self.assertIsInstance(ssmlParseTree.children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[0].getTailText(), '1')
        self.assertEqual(ssmlParseTree.children[0].getDuration(), '2000000ms')
        self.assertEqual(len(ssmlParseTree.children[0].children), 1)

        self.assertIsInstance(ssmlParseTree.children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[0].children[0].getHeadText(), '2')
        self.assertEqual(ssmlParseTree.children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[0].children[0].getDuration(), '1000000ms')

        self.assertIsInstance(ssmlParseTree.children[1], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[1].getTailText(), '5')
        self.assertEqual(ssmlParseTree.children[1].getDuration(), '2000000ms')
        self.assertEqual(len(ssmlParseTree.children[1].children), 1)

        self.assertIsInstance(ssmlParseTree.children[1].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[1].children[0].getHeadText(), '6')
        self.assertEqual(ssmlParseTree.children[1].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[1].children[0].getDuration(), '1000000ms')

        self.assertIsInstance(ssmlParseTree.children[2], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].getHeadText(), '3')
        self.assertEqual(ssmlParseTree.children[2].getTailText(), '4')
        self.assertEqual(ssmlParseTree.children[2].getDuration(), '3000ms')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].getTailText(), '5')
        self.assertEqual(ssmlParseTree.children[2].children[0].getDuration(), '2000000ms')
        self.assertEqual(len(ssmlParseTree.children[2].children), 1)

        self.assertIsInstance(ssmlParseTree.children[2].children[0].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getHeadText(), '6')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[2].children[0].children[0].getDuration(), '1000000ms')
        
        self.assertIsInstance(ssmlParseTree.children[3], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].getDuration(), '5000ms')
        self.assertEqual(len(ssmlParseTree.children[3].children), 1)

        self.assertIsInstance(ssmlParseTree.children[3].children[0], ProsodyElement)
        self.assertEqual(ssmlParseTree.children[3].children[0].getHeadText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getTailText(), '')
        self.assertEqual(ssmlParseTree.children[3].children[0].getDuration(), '9000000ms')


        # Test cases for prosody -> A lot (Might need a different function for each attribute) Only weird if there is nested resolution (not sure if we will impelement it yet, whatJacob is doing for emphasis). -> Assume we will be doing it since the custoemr asked us to do it

        # When the mocks are happenign you have to return mock objects
        # Convert previous janky xml into the new format
        # Update XML
            # Design XML documentation

        # For each node
            # Looks at child but if has emphasis fine
            # Look at next, possibly creates new node, reaches up to the parent, modifies the list of children, then leave, now it's the parents turn

if __name__ == "__main__":
    unittest.main()