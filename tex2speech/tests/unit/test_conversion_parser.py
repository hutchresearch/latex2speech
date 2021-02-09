import unittest
from unittest.mock import patch, Mock

from SSMLParsing.text_element import TextElement
import conversion_db
from conversion_parser import ConversionParser

class testConversionParser(unittest.TestCase):
    def _applyTest(self, cmdConversionDict, envConversionDict, envDefinitionDict, texTree):
        pass

    @patch('conversion_db.ConversionDB')
    def testTextReplacement(self, MockConversionDB):
        # Set up mock database
        db = conversion_db.ConversionDB()

        a = [TextElement('text 1')]
        cmds = {'a': a}
        def mockCmdConversion(cmd):
            nonlocal cmds
            return cmds[cmd]
        
        b = [TextElement('text 2')]
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

        # Parse on the given 
        parser = ConversionParser(None, db)

if __name__ == "__main__":
    unittest.main()