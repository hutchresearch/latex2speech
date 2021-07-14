import unittest, os

from doc_preprocess import doc_preprocess
class TestDocPreprocess(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        if str(doc1) == str(doc2):
            return True
        return False

    # Remove \left
    def test_remove_left(self):
        file = open("doc_preprocess.tex", "w")
        file.write("\\begin{document}" + 
                        r"\left"+
                    r"\end{document}")
        # file.close()
        doc_preprocess("doc_preprocess.tex")
        f = open("doc_preprocess.tex", "r")
        output = f.read()
        self._docsEqual(output, r"\begin{document}\end{document}")
        os.remove("doc_preprocess.tex")

        file = open("doc_preprocess.tex", "w")
        file.write("\\begin{document}" + 
                        r"\left just testing this \left example"+
                    r"\end{document}")
        # file.close()
        doc_preprocess("doc_preprocess.tex")
        f = open("doc_preprocess.tex", "r")
        output = f.read()
        self._docsEqual(output, r"\begin{document}just testing this example\end{document}")
        os.remove("doc_preprocess.tex")

    # Remove \right
    def test_remove_right(self):
        file = open("doc_preprocess.tex", "w")
        file.write("\\begin{document}" + 
                        r"\right"+
                    r"\end{document}")
        # file.close()
        doc_preprocess("doc_preprocess.tex")
        f = open("doc_preprocess.tex", "r")
        output = f.read()
        self._docsEqual(output, r"\begin{document}\end{document}")
        os.remove("doc_preprocess.tex")

        file = open("doc_preprocess.tex", "w")
        file.write("\\begin{document}" + 
                        r"\right just testing this \right example"+
                    r"\end{document}")
        # file.close()
        doc_preprocess("doc_preprocess.tex")
        f = open("doc_preprocess.tex", "r")
        output = f.read()
        self._docsEqual(output, r"\begin{document}just testing this example\end{document}")
        os.remove("doc_preprocess.tex")

    # Remove extra \\
    def remove_double_backslash(self):
        file = open("doc_preprocess.tex", "w")
        file.write("\\begin{document}" + 
                        r"\\ test \\"+
                    r"\end{document}")
        # file.close()
        doc_preprocess("doc_preprocess.tex")
        f = open("doc_preprocess.tex", " test ")
        output = f.read()
        self._docsEqual(output, r"\begin{document}\end{document}")
        os.remove("doc_preprocess.tex")

    # Testing whether \def is replaced with \newcommand
    def replace_def_with_newcommand(self):
        file = open("doc_preprocess.tex", "w")
        file.write("\\begin{document}" + 
                        r"\def \NAS {National Academy of Science}"+
                    r"\end{document}")
        # file.close()
        doc_preprocess("doc_preprocess.tex")
        f = open("doc_preprocess.tex", " test ")
        output = f.read()
        self._docsEqual(output, r"\begin{document}\end{document}")
        os.remove("doc_preprocess.tex")

        file = open("doc_preprocess.tex", "w")
        file.write("\\begin{document}" + 
                        r"\def\foo #1(Hello, #1)"+
                    r"\end{document}")
        # file.close()
        doc_preprocess("doc_preprocess.tex")
        f = open("doc_preprocess.tex", " test ")
        output = f.read()
        self._docsEqual(output, r"\begin{document}\end{document}")
        os.remove("doc_preprocess.tex")