import unittest, TexSoup
from app import app 

import tex2speech.expand_labels, tex2speech.tex_parser, tex2speech.expand_macros


class TestExpandLabels(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        return str(doc1) == str(doc2)

    def testing_hashContents(self):
        print("TEST")

    def testing_replace(self):
        print("TEST")

class TestEmbeddedBibliographies(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        return str(doc1) == str(doc2)

    '''Not a test, just a helper method to simulate
    file reading in parse function of tex_parser'''
    def parseContents(self, document):
        self.output = ''
        self.envList = []
        self.inTable = False
        docstr = None

        try:
            docstr = str(document, 'utf-8')
        except TypeError:
            docstr = document

        doc = tex2speech.expand_macros.expandDocMacros(docstr)
        return doc

    '''Testing inline references to the bibliography'''
    def testing_inline_ref_bibliography(self):
# [NOTE] -> I put this in the bug log, but notice how \LaTeX\, it will render \LaTeX as a command AND \Companion as a command
        # First test of inline commentation of bibliogrpahy references
        doc = TexSoup.TexSoup(r"Three items are cited: \textit{The \LaTeX\ Companion} "+
                        r"book \cite{latexcompanion}, the Einstein journal paper \cite{einstein}, and the "+
                        r"Donald Knuth's website \cite{knuthwebsite}. The \LaTeX\ related items are"+
                        r"\cite{latexcompanion,knuthwebsite}. ")
        doc = self.parseContents(doc)
        expand = tex2speech.tex_parser.TexParser()._parseNodeContents(doc.contents)
        # self.assertTrue(self._docsEqual(expand, ""))

    '''Testing embedded bibliographies function at the bottom of tex file'''
    def testing_bibliography_at_bottom(self):
        # First test of bibliopgahy
        doc = TexSoup.TexSoup(r"\begin{thebibliography}{9}"+
                                r"\bibitem{latexcompanion}"+ 
                                    r"Michel Goossens, Frank Mittelbach, and Alexander Samarin."+ 
                                    r"\textit{The \LaTeX\ Companion}. "
                                    r"Addison-Wesley, Reading, Massachusetts, 1993."+
                            r"\end{thebibliography}")
        doc = self.parseContents(doc)
        expand = tex2speech.tex_parser.TexParser()._parseNodeContents(doc.contents)
        # self.assertTrue(self._docsEqual(expand, ""))

        #  Second test of bibliography output
        doc = TexSoup.TexSoup(r"\begin{thebibliography}{9}"+
                                    r"\bibitem{einstein} "+
                                        r"Albert Einstein. "+ 
                                        r"\textit{Zur Elektrodynamik bewegter K{\"o}rper}. (German) "+
                                        r"[\textit{On the electrodynamics of moving bodies}]. "+
                                        r"Annalen der Physik, 322(10):891–921, 1905."+
                                r"\end{thebibliography}")
        expand = tex2speech.tex_parser.TexParser()._parseNodeContents(doc.contents)
        # self.assertTrue(self._docsEqual(expand, ""))

        # Third test of bibliography output
        doc = TexSoup.TexSoup(r"\begin{thebibliography}{9}"+
                                    r"\bibitem{knuthwebsite} "+
                                        r"Knuth: Computers and Typesetting,"+
                                        r"\\\texttt{http://www-cs-faculty.stanford.edu/\~{}uno/abcde.html}"+
                                r"\end{thebibliography}")
        expand = tex2speech.tex_parser.TexParser()._parseNodeContents(doc.contents)
        # self.assertTrue(self._docsEqual(expand, ""))

if __name__ == '__main__':
    unittest.main()