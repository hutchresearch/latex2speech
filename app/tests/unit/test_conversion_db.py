import unittest
import tempfile
import xml.etree.ElementTree as ET
from conversion_db import ConversionDB
from SSMLParsing.text_element import TextElement
from SSMLParsing.break_element import BreakElement
from SSMLParsing.prosody_element import ProsodyElement
from SSMLParsing.emphasis_element import EmphasisElement

'''
Unit tests for the ConversionDB class.
For most tags, the tests are typically divided as follows:
    -Behavior of tag in global command definition
    -Behavior of tag in global environment definition
    -Behavior of tag in nested command definition, one overriding
       a previous globally defined command
Within these cases, attempts are made to test different combinations
  of attributes to test for edge cases and see that the parser is
  working correctly. The attributes/contents are also made unique
  to ensure we're inspecting the right elements.
'''
class testConversionDB(unittest.TestCase):
    '''
    Tests that solitary text is placed in the proper text wrapper
    '''
    def testTextTag(self):
        db = ConversionDB(r'''
        <latex>
            <cmd name="text-test" type = "none">
                text1
            </cmd>
            <env name="text-test" type = "none">
                <says>
                    text2
                </says>
            </env>
        </latex>''')
        
        elems = db.getCmdConversion("text-test")
        self.assertEqual(len(elems), 1)
        self.assertIsInstance(elems[0], TextElement)
        self.assertEqual(elems[0].getHeadText(), "text1")

        elems = db.getEnvConversion("text-test")
        print(str(elems))
        self.assertEqual(len(elems), 1)
        self.assertIsInstance(elems[0], TextElement)
        self.assertEqual(elems[0].getHeadText(), "text2")


    '''
    Tests the break command with different permutations of
      its attributes. Also tests that surrounding text is properly 
      handled.
    '''
    def testBreakTag(self):
        db = ConversionDB(r'''
        <latex>
            <cmd name="cmd1" type = "none">
                text 1
                <break time="1s"/>
                <break strength="strong"/>
                <break/>
                <break time="5s" strength="none"/>
            </cmd>
            <env name="env" type = "none">
                <says>
                    <break time="2s"/>
                    text 2
                    <break strength="weak"/>
                    <break/>
                    <break time="6s" strength="x-weak"/>
                </says>
                <defines>
                    <cmd name="cmd1" type = "none">
                        <break time="3s"/>
                        <break strength="x-strong"/>
                        text 3
                        <break/>
                        <break time="7s" strength="x-strong"/>
                    </cmd>
                    <cmd name="cmd2" type = "none">
                        <break time="4s"/>
                        <break strength="medium"/>
                        <break/>
                        text 4
                        <break time="8s" strength="weak"/>
                        text 5
                    </cmd>
                </defines>
            </env>
        </latex>''')

        # Global command definition
        elems = db.getCmdConversion('cmd1')
        self.assertEqual(len(elems), 5)

        self.assertIsInstance(elems[0], TextElement)
        self.assertEqual(elems[0].getHeadText(), "text 1")
        
        self.assertIsInstance(elems[1], BreakElement)
        self.assertEqual(elems[1].getTime(), "1s")
        self.assertIsNone(elems[1].getStrength())
        
        self.assertIsInstance(elems[2], BreakElement)
        self.assertIsNone(elems[2].getTime())
        self.assertEqual(elems[2].getStrength(), "strong")
        
        self.assertIsInstance(elems[3], BreakElement)
        self.assertIsNone(elems[3].getTime())
        self.assertIsNone(elems[3].getStrength())
        
        self.assertIsInstance(elems[4], BreakElement)
        self.assertEqual(elems[4].getTime(), "5s")
        self.assertEqual(elems[4].getStrength(), "none")
        
        # Global environment definition
        elems = db.getEnvConversion('env')
        self.assertEqual(len(elems), 4)

        self.assertIsInstance(elems[0], BreakElement)
        self.assertEqual(elems[0].getTime(), "2s")
        self.assertIsNone(elems[0].getStrength())
        self.assertEqual(elems[0].getTailText(), "text 2")
        
        self.assertIsInstance(elems[1], BreakElement)
        self.assertIsNone(elems[1].getTime())
        self.assertEqual(elems[1].getStrength(), "weak")

        self.assertIsInstance(elems[2], BreakElement)
        self.assertIsNone(elems[2].getTime())
        self.assertIsNone(elems[2].getStrength())
        
        self.assertIsInstance(elems[3], BreakElement)
        self.assertEqual(elems[3].getTime(), "6s")
        self.assertEqual(elems[3].getStrength(), "x-weak")

        # Nested command definitions
        elemDict = db.getEnvDefinition('env')

        # Overloaded command
        self.assertIsInstance(elemDict["cmd1"][0], BreakElement)
        self.assertEqual(elemDict["cmd1"][0].getTime(), "3s")
        self.assertIsNone(elemDict["cmd1"][0].getStrength())

        self.assertIsInstance(elemDict["cmd1"][1], BreakElement) 
        self.assertIsNone(elemDict["cmd1"][1].getTime())
        self.assertEqual(elemDict["cmd1"][1].getStrength(), "x-strong")
        self.assertEqual(elemDict["cmd1"][1].getTailText(), "text 3")
        
        self.assertIsInstance(elemDict["cmd1"][2], BreakElement)
        self.assertIsNone(elemDict["cmd1"][2].getTime())
        self.assertIsNone(elemDict["cmd1"][2].getStrength())

        self.assertIsInstance(elemDict["cmd1"][3], BreakElement)
        self.assertEqual(elemDict["cmd1"][3].getTime(), "7s")
        self.assertEqual(elemDict["cmd1"][3].getStrength(), "x-strong")

        # New command
        self.assertIsInstance(elemDict["cmd2"][0], BreakElement)
        self.assertEqual(elemDict["cmd2"][0].getTime(), "4s")
        self.assertIsNone(elemDict["cmd2"][0].getStrength())
        
        self.assertIsInstance(elemDict["cmd2"][1], BreakElement)
        self.assertIsNone(elemDict["cmd2"][1].getTime())
        self.assertEqual(elemDict["cmd2"][1].getStrength(), "medium")
        
        self.assertIsInstance(elemDict["cmd2"][2], BreakElement)
        self.assertIsNone(elemDict["cmd2"][2].getTime())
        self.assertIsNone(elemDict["cmd2"][2].getStrength())
        self.assertEqual(elemDict["cmd2"][2].getTailText(), "text 4")

        self.assertIsInstance(elemDict["cmd2"][3], BreakElement)
        self.assertEqual(elemDict["cmd2"][3].getTime(), "8s")
        self.assertEqual(elemDict["cmd2"][3].getStrength(), "weak")
        self.assertEqual(elemDict["cmd2"][3].getTailText(), "text 5")
    '''
    Tests the emphasis command with different permutations of
      its attribute. Also tests that surrounding/contained text 
      is properly handled.
    '''
    def testEmphasisTag(self):
        db = ConversionDB(r'''
        <latex>
            <cmd name="cmd1" type = "none">
                text 1
                <emphasis>text 2</emphasis>
                <emphasis level="weak">text 3</emphasis>
            </cmd>
            <env name="env" type = "none">
                <says>
                    <emphasis>text 4</emphasis>
                    text 5
                    <emphasis level="strong">text 6</emphasis>
                </says>
                <defines>
                    <cmd name="cmd1" type = "none">
                        <emphasis>text 7</emphasis>
                        <emphasis level="x-strong">text 8</emphasis>
                        text 9
                    </cmd>
                    <cmd name="cmd2" type = "none">
                        <emphasis>text 10</emphasis>
                        <emphasis level="strong">text 11</emphasis>
                    </cmd>
                </defines>
            </env>
        </latex>''')

            # Global command definition
        elems = db.getCmdConversion('cmd1')
        self.assertEqual(len(elems), 3)

        self.assertIsInstance(elems[0], TextElement)
        self.assertEqual(elems[0].getHeadText(), "text 1")
        
        self.assertIsInstance(elems[1], EmphasisElement)
        self.assertIsNone(elems[1].getLevel())
        self.assertEqual(elems[1].getHeadText(), "text 2")

        self.assertIsInstance(elems[2], EmphasisElement)
        self.assertEqual(elems[2].getLevel(), "weak")
        self.assertEqual(elems[2].getHeadText(), "text 3")

        # Global environment definition
        elems = db.getEnvConversion('env')
        self.assertEqual(len(elems), 2)
        
        self.assertIsInstance(elems[0], EmphasisElement)
        self.assertIsNone(elems[0].getLevel())
        self.assertEqual(elems[0].getHeadText(), "text 4")
        self.assertEqual(elems[0].getTailText(), "text 5")

        self.assertIsInstance(elems[1], EmphasisElement)
        self.assertEqual(elems[1].getLevel(), "strong")
        self.assertEqual(elems[1].getHeadText(), "text 6")

        # Nested environment definition
        elemDict = db.getEnvDefinition('env')

        # Overloaded command
        self.assertIsInstance(elemDict['cmd1'][0], EmphasisElement)
        self.assertIsNone(elemDict['cmd1'][0].getLevel())
        self.assertEqual(elemDict['cmd1'][0].getHeadText(), "text 7")

        self.assertIsInstance(elemDict['cmd1'][1], EmphasisElement)
        self.assertEqual(elemDict['cmd1'][1].getLevel(), "x-strong")
        self.assertEqual(elemDict['cmd1'][1].getHeadText(), "text 8")
        self.assertEqual(elemDict['cmd1'][1].getTailText(), "text 9")

        # New command
        self.assertIsInstance(elemDict['cmd2'][0], EmphasisElement)
        self.assertIsNone(elemDict['cmd2'][0].getLevel())
        self.assertEqual(elemDict['cmd2'][0].getHeadText(), "text 10")

        self.assertIsInstance(elemDict['cmd2'][1], EmphasisElement)
        self.assertEqual(elemDict['cmd2'][1].getLevel(), "strong")
        self.assertEqual(elemDict['cmd2'][1].getHeadText(), "text 11")

    def testProsodyTag(self):
        # TODO: This will be very complicated, handle once we have other stuff down
        pass

    def testCmdInEnv(self):
        db = ConversionDB(r'''
        <latex>
            <cmd name="cmd1" type = "none">
                text1
            </cmd>
            <env name="env" type = "none">
                <says>
                </says>
                <defines>
                    <cmd name="cmd1" type = "none">
                        text2
                    </cmd>
                    <cmd name="cmd2" type = "none">
                        text3
                    </cmd>
                </defines>
            </env>
        </latex>''')
        
        elems = db.getCmdConversion("cmd1")
        self.assertEqual(len(elems), 1)
        self.assertIsInstance(elems[0], TextElement)
        self.assertEqual(elems[0].getHeadText(), "text1")

        elemsDict = db.getEnvDefinition("env")
        self.assertIsInstance(elemsDict["cmd1"][0], TextElement)
        self.assertEqual(elemsDict["cmd1"][0].getHeadText(), "text2")

        self.assertIsInstance(elemsDict["cmd2"][0], TextElement)
        self.assertEqual(elemsDict["cmd2"][0].getHeadText(), "text3")