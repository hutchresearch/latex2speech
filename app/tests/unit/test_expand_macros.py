import TexSoup
import unittest

import expand_macros

'''Unit tests for the classes. Since the expandMacro functionality is tested
   thouroughly in Testexpand_doc_macros these are just small tests to test
   the classes expansion capabilities'''
class TestCmdMacro(unittest.TestCase):
    def testRelativeExpansion(self):
        doc = TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\c}{\a}\c')
        cmd = expand_macros.CmdMacro(doc.contents[0], {}, {})
        cmdDict = {'a' : cmd}
        cmd = expand_macros.CmdMacro(doc.contents[1], cmdDict, {})
        cmdOut = cmd.expand_macro(doc.contents[2])
        self.assertEqual(cmdOut, r'\b')

class TestEnvMacro(unittest.TestCase):
    def testRelativeExpansion(self):
        doc = TexSoup.TexSoup(r'\newenvironment{a}{\b}{\b}\newenvironment{c}{\begin{a}\end{a}}{\begin{a}\end{a}}\begin{c}\end{c}')
        env = expand_macros.EnvMacro(doc.contents[0], {}, {})
        envDict = {'a' : env}
        env = expand_macros.EnvMacro(doc.contents[1], {}, envDict)
        envOut = env.expand_macro(doc.contents[2])
        self.assertEqual(envOut, r'\b\b\b\b')

'''Unit Testing class for the combined functionality'''
class Testexpand_doc_macros(unittest.TestCase):
    '''Since equality between two TexSoup trees doesn't work as we'd like, this
         method is necessary for unit testing. This definition of equality here is possibly
         too strict.'''
    def _docsEqual(self, doc1, doc2):
        return str(doc1) == str(doc2)

    '''Tests whether arguments and optional arguments work'''
    def testArguments(self):
        # Some number of arguments in newcommand
        doc = TexSoup.TexSoup(r'\newcommand{\a}[3]{#1 #2 #3}\a{a}{b}{c}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}[3]{#1 #2 #3}a b c')))

        # Optional arguments in newcommand
        doc = TexSoup.TexSoup(r'\newcommand{\a}[3][d]{#1 #2 #3}\a{b}{c}\a[a]{b}{c}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}[3][d]{#1 #2 #3}d b ca b c')))

        # Some number of arguments in newenvironment
        doc = TexSoup.TexSoup(r'\newenvironment{a}[3]{#1 #2 #3}{#3 #2 #1}\begin{a}{a}{b}{c}\end{a}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newenvironment{a}[3]{#1 #2 #3}{#3 #2 #1}a b cc b a')))

        # Optional arguments in newenvironment
        doc = TexSoup.TexSoup(r'\newenvironment{a}[3][d]{#1 #2 #3}{#3 #2 #1}\begin{a}{b}{c}\end{a}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newenvironment{a}[3][d]{#1 #2 #3}{#3 #2 #1}d b cc b d')))

    '''Tests whether forward definitions of macros are expanded in subsequent macros to 
         an arbitrary level of depth'''
    def testForwardDefinition(self):
        # Simple case
        doc = TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\c}{\a}\c')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\c}{\b}\b')))
        
        # Multiple nested levels
        doc = TexSoup.TexSoup(r'\newcommand{\a}[1]{\b{#1}}\newcommand{\c}{\d}' +
                              r'\newcommand{\e}{' + 
                                  r'\begin{dummy}'  +
                                      r'\a{\c}'       +
                                  r'\end{dummy}}'   +
                              r'\f{\e}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, \
            TexSoup.TexSoup(r'\newcommand{\a}[1]{\b{#1}}\newcommand{\c}{\d}' +
                            r'\newcommand{\e}{' + 
                                r'\begin{dummy}'  +
                                    r'\b{\d}'       +
                                r'\end{dummy}}'   +
                            r'\f{\begin{dummy}\b{\d}\end{dummy}}')))

        # Proper definition used in the case of redefinition
        doc = TexSoup.TexSoup(r'\newcommand{\a}{\ba}\newcommand{\ca}{\a}\ca\renewcommand{\a}{\bb}\newcommand{\cb}{\a}\cb')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}{\ba}\newcommand{\ca}{\ba}\ba\renewcommand{\a}{\bb}\newcommand{\cb}{\bb}\bb')))

    '''TODO: Add functionality to pass this. 
         Each normalize call must also modify PREVIOUS macros that are defined in terms of the currently defined macro'''
    def testRecursiveDefinition(self):
        doc = TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\b}{\c}\a')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\b}{\c}\c')))
        
        doc = TexSoup.TexSoup(r'\newenvironment{a}{\begin{b}\end{b}}{\begin{b}\end{b}}\newenvironment{b}{\c}{\c}\begin{a}\end{a}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newenvironment{a}{\c\c}{\c\c}\newenvironment{b}{\c}{\c}\c\c\c\c')))

    '''Tests whether a macro is only expanded after it has been defined/redefined'''
    def testEarlyDefinition(self):
        doc = TexSoup.TexSoup(r'\a\newcommand{\a}{\b}\a')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\a\newcommand{\a}{\b}\b')))

        doc = TexSoup.TexSoup(r'\a\renewcommand{\a}{\b}\a\renewcommand{\a}{\c}\a')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\a\renewcommand{\a}{\b}\b\renewcommand{\a}{\c}\c')))
        
        doc = TexSoup.TexSoup(r'\begin{a}\end{a}\newenvironment{a}{\b}{\c}\begin{a}\end{a}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\begin{a}\end{a}\newenvironment{a}{\b}{\c}\b\c')))

        doc = TexSoup.TexSoup(r'\begin{a}\end{a}\renewenvironment{a}{\b}{\c}\begin{a}\end{a}\renewenvironment{a}{\c}{\d}\begin{a}\end{a}')
        expanded = expand_macros.expand_doc_macros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\begin{a}\end{a}\renewenvironment{a}{\b}{\c}\b\c\renewenvironment{a}{\c}{\d}\c\d')))

if __name__ == "__main__":
    unittest.main()