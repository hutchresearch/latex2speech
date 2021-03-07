import unittest
from app import app 
import os

import tex2speech.expand_labels, tex2speech.conversion_parser, tex2speech.aws_polly_render

class TestExternalBibliographies(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        doc1 = doc1.replace("'", '"')
        doc2 = doc2.replace("'", '"')

        return set(str(doc1).split(' ')) == set(str(doc2).split(' '))

    # Testing single function of author being read correctly
    def testing_external_author(self):
        # Create new file
        with open("testingBib.bib", 'w') as outfile:
            outfile.write('@Book{gG07,'+
                            'author = "Gratzer, George A."'
                        '}');

        path = os.getcwd() + "/testingBib.bib"
        bibContent = tex2speech.aws_polly_render.parse_bib_file(path);

        self.assertTrue(self._docsEqual(bibContent,"<emphasis level='strong'> References Section </emphasis> <break time='1s'/>  Bibliography item is read as: <break time='0.5s'/>gG07. Type: book<break time='0.5s'/>  Authors: Gratzer, George A., <break time='0.3s'/>"))

    # Testing single function of title being read correctly
    def testing_external_title(self):
        # Create new file
        with open("testingBib.bib", 'w') as outfile:
            outfile.write('@Book{gG07,'+
                            'title = "More Math Into LaTeX"'
                        '}');

        path = os.getcwd() + "/testingBib.bib"
        bibContent = tex2speech.aws_polly_render.parse_bib_file(path);

        self.assertTrue(self._docsEqual(bibContent,"<emphasis level='strong'> References Section </emphasis> <break time='1s'/>  Bibliography item is read as: <break time='0.5s'/>gG07. Type: book<break time='0.5s'/> title: More Math Into LaTeX<break time='0.3s'/>"))

    # Testing single function of publisher being read correctly
    def testing_external_publisher(self):
        # Create new file
        with open("testingBib.bib", 'w') as outfile:
            outfile.write('@Book{gG07,'+
                            'publisher = "Birkhauser"'
                        '}');

        path = os.getcwd() + "/testingBib.bib"
        bibContent = tex2speech.aws_polly_render.parse_bib_file(path);

        self.assertTrue(self._docsEqual(bibContent,"<emphasis level='strong'> References Section </emphasis> <break time='1s'/>  Bibliography item is read as: <break time='0.5s'/>gG07. Type: book<break time='0.5s'/> publisher: Birkhauser<break time='0.3s'/>"))

    # Testing single function of address being read correctly
    def testing_external_address(self):
        # Create new file
        with open("testingBib.bib", 'w') as outfile:
            outfile.write('@Book{gG07,'+
                            'address = "Boston"'
                        '}');

        path = os.getcwd() + "/testingBib.bib"
        bibContent = tex2speech.aws_polly_render.parse_bib_file(path);

        self.assertTrue(self._docsEqual(bibContent,"<emphasis level='strong'> References Section </emphasis> <break time='1s'/>  Bibliography item is read as: <break time='0.5s'/>gG07. Type: book<break time='0.5s'/> address: Boston<break time='0.3s'/>"))

    # Testing single function of year being read correctly
    def testing_external_year(self):
        # Create new file
        with open("testingBib.bib", 'w') as outfile:
            outfile.write('@Book{gG07,'+
                            'year = 2007'
                        '}');

        path = os.getcwd() + "/testingBib.bib"
        bibContent = tex2speech.aws_polly_render.parse_bib_file(path);

        self.assertTrue(self._docsEqual(bibContent,"<emphasis level='strong'> References Section </emphasis> <break time='1s'/>  Bibliography item is read as: <break time='0.5s'/>gG07. Type: book<break time='0.5s'/> year: 2007<break time='0.3s'/>"))

    # Testing single function of edition being read correctly
    def testing_external_edition(self):
        # Create new file
        with open("testingBib.bib", 'w') as outfile:
            outfile.write('@Book{gG07,'+
                            'edition = "4th"'
                        '}');

        path = os.getcwd() + "/testingBib.bib"
        bibContent = tex2speech.aws_polly_render.parse_bib_file(path);

        self.assertTrue(self._docsEqual(bibContent,"<emphasis level='strong'> References Section </emphasis> <break time='1s'/>  Bibliography item is read as: <break time='0.5s'/>gG07. Type: book<break time='0.5s'/> edition: 4th<break time='0.3s'/>"))

    # test to test parse bib files for external, gives overall
    def testing_external_bib_file(self):
        # Create new file
        with open("testingBib.bib", 'w') as outfile:
            outfile.write('@Book{gG07,'+
                            'author = "Gratzer, George A.",'+
                            'title = "More Math Into LaTeX",'+
                            'publisher = "Birkhauser",'+
                            'address = "Boston",'+
                            'year = 2007,'+
                            'edition = "4th"'+
                        '}');

        path = os.getcwd() + "/testingBib.bib"
        bibContent = tex2speech.aws_polly_render.parse_bib_file(path);

        self.assertTrue(self._docsEqual(bibContent,"<emphasis level='strong'> References Section </emphasis> <break time='1s'/>  Bibliography item is read as: <break time='0.5s'/>gG07. Type: book<break time='0.5s'/>  Authors: Gratzer, George A., <break time='0.3s'/> title: More Math Into LaTeX<break time='0.3s'/>publisher: Birkhauser<break time='0.3s'/>address: Boston<break time='0.3s'/>year: 2007<break time='0.3s'/>edition: 4th<break time='0.3s'/>"))
        
class TestEmbeddedBibliographies(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        doc1 = doc1.replace("'", '"')
        doc2 = doc2.replace("'", '"')
        print(set(str(doc1).split(' ')))
        print(set(str(doc2).split(' ')))
        # print(doc1 + "\n" + doc2 + "\n" + doc1 == doc2)
        return set(str(doc1).split(' ')) == set(str(doc2).split(' '))

    '''Testing inline references to the bibliography'''
    def testing_inline_ref_bibliography(self):
# [NOTE] -> I put this in the bug log, but notice how \LaTeX\, it will render \LaTeX as a command AND \Companion as a command
        # First test of inline commentation of bibliogrpahy references
        doc = (r"Three items are cited: \textit{The \LaTeX\ Companion} "+
                        r"book \cite{latexcompanion}, the Einstein journal paper \cite{einstein}, and the "+
                        r"Donald Knuth's website \cite{knuthwebsite}. The \LaTeX\ related items are"+
                        r"\cite{latexcompanion,knuthwebsite}. ")

        expand = tex2speech.aws_polly_render.start_conversion(doc)

        self.assertTrue(self._docsEqual(expand, r"Three items are cited: The  LaTeX book Cited in reference as: latexcompanion, the Einstein journal paper Cited in reference as: einstein, and the Donald Knuth's website Cited in reference as: knuthwebsite. The  LaTeXCited in reference as: latexcompanion,knuthwebsite."))

    '''Testing embedded bibliographies function at the bottom of tex file'''
    def testing_bibliography_at_bottom(self):
        # First test of bibliopgahy
        doc = (r"\begin{thebibliography}{9}"+
                                r"\bibitem{latexcompanion}"+ 
                                    r"Michel Goossens, Frank Mittelbach, and Alexander Samarin."+ 
                                    r"\textit{The \LaTeX\ Companion}. "
                                    r"Addison-Wesley, Reading, Massachusetts, 1993."+
                            r"\end{thebibliography}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)

        self.assertTrue(self._docsEqual(expand, "Reference Section:Bibliography item is read as:latexcompanion Michel Goossens, Frank Mittelbach, and Alexander Samarin.The  LaTeX. Addison-Wesley, Reading, Massachusetts, 1993."))

        #  Second test of bibliography output
        doc = (r"\begin{thebibliography}{9}"+
                                    r"\bibitem{einstein} "+
                                        r"Albert Einstein. "+ 
                                        r"\textit{Zur Elektrodynamik bewegter K{\"o}rper}. (German) "+
                                        r"[\textit{On the electrodynamics of moving bodies}]. "+
                                        r"Annalen der Physik, 322(10):891–921, 1905."+
                                r"\end{thebibliography}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)

        self.assertTrue(self._docsEqual(expand, "Reference Section:Bibliography item is read as:einstein  Albert Einstein. Zur Elektrodynamik bewegter K \" o rper. (German)  [On the electrodynamics of moving bodies] . Annalen der Physik, 322(10):891–921, 1905."))

        # Third test of bibliography output
        doc = (r"\begin{thebibliography}{9}"+
                                    r"\bibitem{knuthwebsite} "+
                                        r"Knuth: Computers and Typesetting,"+
                                        r"\\\texttt{http://www-cs-faculty.stanford.edu/\~{}uno/abcde.html}"+
                                r"\end{thebibliography}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)

        self.assertTrue(self._docsEqual(expand, r"<speak> <emphasis level='strong'> References Section </emphasis> <break time='1s'/>Bibliography item is read as: <break time='0.5s'/> knuthwebsite Knuth: Computers and Typesetting, \\ <emphasis level='strong'> http://www-cs-faculty.stanford.edu/ \~ uno/abcde.html </emphasis> </speak>"))

class TestExpandLabels(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        return str(doc1) == str(doc2)

    '''This Unit Test, will test the contents of the hashtable when looking through .aux file contents'''
    def testing_hashContents(self):
        # Aux file containing single label
        doc = (r"\newlabel{strings}{{1}{1}{}{equation.0.1}{}}")
        hashContents = tex2speech.expand_labels.hashTableTest(doc)
        self.assertTrue(self._docsEqual(hashContents['strings'], r"['1', '1', '', 'equation.0.1']"))

        # Aux file contains new labels for equations - together
        doc = (r"\newlabel{fl}{{1}{1}{}{equation.0.1}{}}" + "\n" +
            r"\newlabel{sl}{{2}{1}{}{equation.0.1}{}}")
        hashContents = tex2speech.expand_labels.hashTableTest(doc)
        self.assertTrue(self._docsEqual(hashContents['fl'], r"['1', '1', '', 'equation.0.1']"))
        self.assertTrue(self._docsEqual(hashContents['sl'], r"['2', '1', '', 'equation.0.1']"))

        # Aux file contains new labels for a given figure
        doc = (r"\newlabel{sample}{{1}{1}{Sample figure plotting $T=300~{\rm K}$ isotherm for air when modeled as an ideal gas}{figure.1}{}}")
        hashContents = tex2speech.expand_labels.hashTableTest(doc)
        self.assertTrue(self._docsEqual(hashContents['sample'], r"['1', '1', 'Sample figure plotting $T=300~\\rm K}$ isotherm for air when modeled as an ideal gas', 'figure.1']"))

    def testing_replace(self):
        # Testing single equation in file
        aux = (r"\newlabel{strings}{{1}{1}{}{equation.0.1}{}}")
        hash = tex2speech.expand_labels.hashTableTest(aux)
        doc = r"Eq.~(\ref{strings}) is the first law."
        replace = tex2speech.expand_labels.replaceReferences(doc, hash)
        self.assertTrue(self._docsEqual(replace, r"Equation 1 is the first law."))

        # Testing multiple figures
        aux = (r"\newlabel{sample}{{1}{1}{Sample figure plotting $T=300~{\rm K}$ isotherm for air when modeled as an ideal gas}{figure.1}{}}")
        hash = tex2speech.expand_labels.hashTableTest(aux)
        # print(hash['sample'])
        doc = r"Figure \ref{sample}, below, plots an isotherm for air modeled as an ideal gas."
        replace = tex2speech.expand_labels.replaceReferences(doc, hash)
        self.assertTrue(self._docsEqual(replace, r"Figure 1, below, plots an isotherm for air modeled as an ideal gas."))

if __name__ == '__main__':
    unittest.main()