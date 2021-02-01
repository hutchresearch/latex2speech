import unittest
from app import app 

import tex2speech.expand_labels, tex2speech.tex_parser


class TestExpandLabels(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        return str(doc1) == str(doc2)

    def testing_hashContents(self):
        # Aux file containing single label
        doc = (r"\newlabel{strings}{{1}{1}{}{equation.0.1}{}}")
        hashContents = tex2speech.expand_labels.hashTableTest(doc)
        self.assertTrue(self._docsEqual(hashContents['strings'], r"['1', '1', '', 'equation.0.1']"))

        # Aux file contains new labels for equations - together
        doc = (r"\newlabel{fl}{{1}{1}{}{equation.0.1}{}}" + "\n" +
            r"\newlabel{sl}{{2}{1}{}{equation.0.1}{}}")
        hashContents = tex2speech.expand_labels.hashTableTest(doc)
        print(hashContents['fl'])
        self.assertTrue(self._docsEqual(hashContents['fl'], r"['1', '1', '', 'equation.0.1']"))
        self.assertTrue(self._docsEqual(hashContents['sl'], r"['2', '1', '', 'equation.0.1']"))

        # Aux file contains new labels for a given figure
        doc = (r"\newlabel{sample}{{1}{1}{Sample figure plotting $T=300~{\rm K}$ isotherm for air when modeled as an ideal gas}{figure.1}{}}")
        hashContents = tex2speech.expand_labels.hashTableTest(doc)
        print(hashContents['sample'])
        self.assertTrue(self._docsEqual(hashContents['sample'], r"['1', '1', 'Sample figure plotting $T=300~\\rm K}$ isotherm for air when modeled as an ideal gas', 'figure.1']"))

    def testing_replace(self):
        print("TEST")

class TestEmbeddedBibliographies(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        doc1 = doc1.replace("'", '"')
        doc2 = doc2.replace("'", '"')

        # print("\n\n" + doc1 + "\n" + doc2)
        return str(doc1) == str(doc2)

    '''Testing inline references to the bibliography'''
    def testing_inline_ref_bibliography(self):
# [NOTE] -> I put this in the bug log, but notice how \LaTeX\, it will render \LaTeX as a command AND \Companion as a command
        # First test of inline commentation of bibliogrpahy references
        doc = (r"Three items are cited: \textit{The \LaTeX\ Companion} "+
                        r"book \cite{latexcompanion}, the Einstein journal paper \cite{einstein}, and the "+
                        r"Donald Knuth's website \cite{knuthwebsite}. The \LaTeX\ related items are"+
                        r"\cite{latexcompanion,knuthwebsite}. ")
        expand = tex2speech.tex_parser.TexParser().parse(doc)
        self.assertTrue(self._docsEqual(expand, r"<speak> Three items are cited: <emphasis level='strong'> The </emphasis> book <emphasis level='reduced'> Cited in references as latexcompanion </emphasis> , the Einstein journal paper <emphasis level='reduced'> Cited in references as einstein </emphasis> , and the Donald Knuth's website <emphasis level='reduced'> Cited in references as knuthwebsite </emphasis> . The LaTeX items are <emphasis level='reduced'> Cited in references as latexcompanion,knuthwebsite </emphasis> . </speak>"))

    '''Testing embedded bibliographies function at the bottom of tex file'''
    def testing_bibliography_at_bottom(self):
        # First test of bibliopgahy
        doc = (r"\begin{thebibliography}{9}"+
                                r"\bibitem{latexcompanion}"+ 
                                    r"Michel Goossens, Frank Mittelbach, and Alexander Samarin."+ 
                                    r"\textit{The \LaTeX\ Companion}. "
                                    r"Addison-Wesley, Reading, Massachusetts, 1993."+
                            r"\end{thebibliography}")
        expand = tex2speech.tex_parser.TexParser().parse(doc)
        self.assertTrue(self._docsEqual(expand, "<speak> <emphasis level='strong'> References Section </emphasis> <break time='1s'/>Bibliography item is read as: <break time='0.5s'/> latexcompanion Michel Goossens, Frank Mittelbach, and Alexander Samarin. <emphasis level='strong'> The </emphasis> . Addison-Wesley, Reading, Massachusetts, 1993. </speak>"))

        #  Second test of bibliography output
        doc = (r"\begin{thebibliography}{9}"+
                                    r"\bibitem{einstein} "+
                                        r"Albert Einstein. "+ 
                                        r"\textit{Zur Elektrodynamik bewegter K{\"o}rper}. (German) "+
                                        r"[\textit{On the electrodynamics of moving bodies}]. "+
                                        r"Annalen der Physik, 322(10):891–921, 1905."+
                                r"\end{thebibliography}")
        expand = tex2speech.tex_parser.TexParser().parse(doc)
        self.assertTrue(self._docsEqual(expand, "<speak> <emphasis level='strong'> References Section </emphasis> <break time='1s'/>Bibliography item is read as: <break time='0.5s'/> einstein Albert Einstein. <emphasis level='strong'> Zur Elektrodynamik bewegter K rper </emphasis> . (German) [ <emphasis level='strong'> On the electrodynamics of moving bodies </emphasis> ] . Annalen der Physik, 322(10):891–921, 1905. </speak>"))

        # Third test of bibliography output
        doc = (r"\begin{thebibliography}{9}"+
                                    r"\bibitem{knuthwebsite} "+
                                        r"Knuth: Computers and Typesetting,"+
                                        r"\\\texttt{http://www-cs-faculty.stanford.edu/\~{}uno/abcde.html}"+
                                r"\end{thebibliography}")
        expand = tex2speech.tex_parser.TexParser().parse(doc)
        self.assertTrue(self._docsEqual(expand, r"<speak> <emphasis level='strong'> References Section </emphasis> <break time='1s'/>Bibliography item is read as: <break time='0.5s'/> knuthwebsite Knuth: Computers and Typesetting, \\ <emphasis level='strong'> http://www-cs-faculty.stanford.edu/ \~ uno/abcde.html </emphasis> </speak>"))

if __name__ == '__main__':
    unittest.main()