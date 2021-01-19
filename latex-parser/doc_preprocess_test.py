import TexSoup
import unittest

import doc_preprocess

'''Unit Testing class for the macro expansion functionality'''
class TestMacroExpansion(unittest.TestCase):
    '''Since equality between two TexSoup trees doesn't work as we'd like, this
         method is necessary for unit testing. This definition of equality here is possibly
         too strict.'''
    def _docsEqual(self, doc1, doc2):
        return str(doc1) == str(doc2)

    '''Tests whether arguments and optional arguments work'''
    def testArguments(self):
        # Some number of arguments
        doc = TexSoup.TexSoup(r'\newcommand{\a}[3]{#1 #2 #3}\a{a}{b}{c}')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}[3]{#1 #2 #3}a b c')))

        # Optional arguments
        doc = TexSoup.TexSoup(r'\newcommand{\a}[3][d]{#1 #2 #3}\a{b}{c}\a[a]{b}{c}')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}[3][d]{#1 #2 #3}d b ca b c')))

    '''Tests whether forward definitions of macros are expanded in subsequent macros to 
         an arbitrary level of depth'''
    def testForwardDefinition(self):
        # Simple case
        doc = TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\c}{\a}\c')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\c}{\b}\b')))
        
        # Multiple nested levels
        doc = TexSoup.TexSoup(r'\newcommand{\a}[1]{\b{#1}}\newcommand{\c}{\d}' +
                              r'\newcommand{\e}{' + 
                                  r'\begin{dummy}'  +
                                      r'\a{\c}'       +
                                  r'\end{dummy}}'   +
                              r'\f{\e}')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, \
            TexSoup.TexSoup(r'\newcommand{\a}[1]{\b{#1}}\newcommand{\c}{\d}' +
                            r'\newcommand{\e}{' + 
                                r'\begin{dummy}'  +
                                    r'\b{\d}'       +
                                r'\end{dummy}}'   +
                            r'\f{\begin{dummy}\b{\d}\end{dummy}}')))

        # Proper definition used in the case of redefinition
        doc = TexSoup.TexSoup(r'\newcommand{\a}{\ba}\newcommand{\ca}{\a}\ca\renewcommand{\a}{\bb}\newcommand{\cb}{\a}\cb')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}{\ba}\newcommand{\ca}{\ba}\ba\renewcommand{\a}{\bb}\newcommand{\cb}{\bb}\bb')))

    '''TODO: Add functionality to pass this. 
         Each normalize call must also modify PREVIOUS macros that are defined in terms of the currently defined macro'''
    def testRecursiveDefinition(self):
        doc = TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\b}{\c}\a')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\newcommand{\a}{\b}\newcommand{\b}{\c}\c')))

    '''Tests whether a macro is only expanded after it has been defined/redefined'''
    def testEarlyDefinition(self):
        doc = TexSoup.TexSoup(r'\a\newcommand{\a}{\b}\a')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\a\newcommand{\a}{\b}\b')))

        doc = TexSoup.TexSoup(r'\a\renewcommand{\a}{\b}\a\renewcommand{\a}{\c}\a')
        expanded = doc_preprocess.expandDocMacros(doc)
        self.assertTrue(self._docsEqual(expanded, TexSoup.TexSoup(r'\a\renewcommand{\a}{\b}\b\renewcommand{\a}{\c}\c')))

if __name__ == "__main__":
    unittest.main()