import unittest
from app import app 

import tex2speech.aws_polly_render, tex2speech.conversion_parser

class TestTables(unittest.TestCase):
    def _docsEqual(self, doc1, doc2):
        return set(str(doc1).split(' ')) == set(str(doc2).split(' '))

    '''Unit test for basic table elements'''
    def testing_basic_tables(self):
        # Testing basic table in LaTeX
        doc = ("\\begin{tabular}{ c c c }\n"
                "a & b & c \n"+
                "d & e & f \n"+
               "\\end{tabular}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        self.assertTrue(self._docsEqual(expand, r'<speak> Table Contents: <break time="40ms"/>   New Row:  , Column 1, Value: a  , Column 2, Value:  b  , Column 3, Value:  c  New Row:  , Column 1, Value: d  , Column 2, Value:  e  , Column 3, Value:  f <break time="40ms"/>    </speak>'))

        # Basic table with \hline command
        doc = (r"\begin{center}"+
                    "\\begin{tabular}{ |c|c|c| } \n"+
                        "\\hline \n"+
                        "oranges & apples & pears \n "+
                        "red & green & blue \n"+
                        "lettuce & carrot & brocoli \n"+
                        "\\hline \n"+
                    "\\end{tabular} \n"+
                "\\end{center}\n")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        self.assertTrue(self._docsEqual(expand, r'<speak>  <p> Table Contents: <break time="40ms"/>   New Row:  , Column 1, Value: oranges  , Column 2, Value:  apples  , Column 3, Value:  pears  New Row:  , Column 1, Value:  red  , Column 2, Value:  green  , Column 3, Value:  blue  New Row:  , Column 1, Value: lettuce  , Column 2, Value:  carrot  , Column 3, Value:  brocoli <break time="40ms"/>    </p>  </speak>'))

        # Basic table with \hline command 2
        doc = ("\\begin{center}\n"+
                    "\\begin{tabular}{ |c|c|c| } \n"+
                        "\\hline \n"+
                        "yes & no & maybe \n "+
                        "so & testing & more in one cell \n "+
                        "this has a lot of words in it & too many words for the table & i cant take it any longer! \n "+
                        "\\hline \n"+
                    "\\end{tabular} \n"+
                "\\end{center}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        self.assertTrue(self._docsEqual(expand, r'<speak>  <p> Table Contents: <break time="40ms"/>   New Row:  , Column 1, Value: yes  , Column 2, Value:  no  , Column 3, Value:  maybe  New Row:  , Column 1, Value:  so  , Column 2, Value:  testing  , Column 3, Value:  more in one cell  New Row:  , Column 1, Value:  this has a lot of words in it  , Column 2, Value:  too many words for the table  , Column 3, Value:  i cant take it any longer! <break time="40ms"/>    </p>  </speak>'))

    def testing_tables_with_extra_commands(self):
        # Checking to see if the extra commands get parsed
        doc = ("\\begin{center} \n"+
                    "\\begin{tabular}{ | m{5em} | m{1cm}| m{1cm} | } \n"+
                        "\\hline \n"+
                        "cell1 dummy text dummy text dummy text& cell2 & cell3 \n "+
                        "\\hline \n"+
                        "cell1 dummy text dummy text dummy text & cell5 & cell6 \n "+
                        "\\hline \n"+
                        "cell7 & cell8 & cell9 \n "+
                        "\\hline \n"+
                    "\\end{tabular} \n"+
                "\\end{center}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        self.assertTrue(self._docsEqual(expand, r'<speak>  <p> Table Contents: <break time="40ms"/>   New Row:  , Column 1, Value: cell1 dummy text dummy text dummy text , Column 2, Value:  cell2  , Column 3, Value:  cell3  New Row:  , Column 1, Value:    New Row:  , Column 1, Value: cell1 dummy text dummy text dummy text  , Column 2, Value:  cell5  , Column 3, Value:  cell6  New Row:  , Column 1, Value:    New Row:  , Column 1, Value: cell7  , Column 2, Value:  cell8  , Column 3, Value:  cell9 <break time="40ms"/>    </p>  </speak>'))

        # This table uses tabularx and a bunch of random stuff, testing to see if this gets parsed/passed
# [ERROR] -> Doesn't render tabularx
# Output: <speak> item 11 &amp; item 12 &amp; item 13 \\ item 21  &amp; item 22  &amp; item 23  \\ </speak>
        doc = (r"\begin{tabularx}{0.8\textwidth} { "+
            r" | >{\raggedright\arraybackslash}X "+
            r" | >{\centering\arraybackslash}X "+
            r" | >{\raggedleft\arraybackslash}X | }"+
                r"\hline"+
                "item 11 & item 12 & item 13 \n"+
                "\\hline \n"+
                "item 21  & item 22  & item 23  \n"+
                "\\hline \n"+
            r"\end{tabularx}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        # self.assertTrue(self._docsEqual(expand, r""))

        # Different table layout, testing to see if it parses there
# [ERROR] -> This gets rendered really really weirdly
        doc = (r"\begin{tabular}{ |p{3cm}||p{3cm}|p{3cm}|p{3cm}|  }"+
                r"\hline"+
                r"\multicolumn{4}{|c|}{Country List} \\"+
                r"\hline"+
                r"Country Name     or Area Name& ISO ALPHA 2 Code &ISO ALPHA 3 Code&ISO numeric Code\\"+
                r"\hline"+
                r"Afghanistan   & AF    &AFG&   004\\"+
                r"Aland Islands&   AX  & ALA   &248\\"+
                r"Albania &AL & ALB&  008\\"+
                r"Algeria    &DZ & DZA&  012\\"+
                r"American Samoa&   AS  & ASM&016\\"+
                r"Andorra& AD  & AND   &020\\"+
                r"Angola& AO  & AGO&024\\"+
                r"\hline"+
            r"\end{tabular}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        # self.assertTrue(self._docsEqual(expand, r""))

        # Testing with different format, has two \hline and 0.5ex in the way
# [ERROR] -> [0.5ex] these ruin the render
        doc = (r"\begin{table}[h!]"+
            r"\centering"+
                "\\begin{tabular}{||c c c c||} \n"+
                    "\\hline \n"+
                    "Col1 & Col2 & Col2 & Col3 \\ [0.5ex] \n"+
                    "\\hline\hline \n"+
                    "1 & 6 & 87837 & 787 \\ \n"+
                    "2 & 7 & 78 & 5415 \\ \n"+
                    "3 & 545 & 778 & 7507 \\ \n"+
                    "4 & 545 & 18744 & 7560 \\ \n"+
                    "5 & 88 & 788 & 6344 \\ [1ex] \n"+
                    " \\hline"+
                "\\end{tabular}"+
            r"\end{table}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        # self.assertTrue(self._docsEqual(expand, r""))

        # Testing big table function
# [ERROR] -> Same as before, doesn't render properly
        doc = (r"\begin{tabular}{ |p{3cm}|p{3cm}|p{3cm}|  }"+
                r"\hline"+
                r"\multicolumn{3}{|c|}{Country List} \\"+
                r"\hline"+
                r"Country Name     or Area Name& ISO ALPHA 2 Code &ISO ALPHA 3 \\"+
                r"\hline"+
                r"Afghanistan & AF &AFG \\"+
                r"Aland Islands & AX   & ALA \\"+
                r"Albania &AL & ALB \\"+
                r"Algeria    &DZ & DZA \\"+
                r"American Samoa & AS & ASM \\"+
                r"Andorra & AD & AND   \\"+
                r"Angola & AO & AGO \\"+
                r"\hline"+
            r"\end{tabular}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        # self.assertTrue(self._docsEqual(expand, r""))

    def testing_multiple_row(self):
        # Multiple rows in table
# [NOTE] -> This table is raed fine even with different columns and what not!
        doc = ("\\begin{center}"+
                "\\begin{tabular}{ |c|c|c|c| } \n"+
                "\\hline \n"+
                "col1 & col2 & col3 \n"+
                "\\hline \n"+
                "\\multirow{3}{4em}{Multiple row} & cell2 & cell3 \n"+
                "& cell5 & cell6 \n "+
                "& cell8 & cell9 \n "+
                "\\hline \n"+
                "\\end{tabular} \n"+
                "\\end{center}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        # self.assertTrue(self._docsEqual(expand, r""))        

    '''Unit test for testing captions in a table, and table name'''
    def testing_captions_table_name(self):
        # Testing basic caption here
# [NOTE] -> This renders incorrectly, well it reads the caption,
# but it says End Table right before the caption being read
        doc = (r"\begin{table}[h!]"+
            r"\centering"+
                "\\begin{tabular}{c c c} \n"+
                    "a & b & c \n "+
                    "d & e & f \n"+
                "\\end{tabular} \n"+
            "\\caption{Table to test captions and labels} \n"+
            r"\label{table:1}"+
            r"\end{table}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        self.assertTrue(self._docsEqual(expand, r'<speak> Begin Table: <break time="0.3s"/>   Table Contents: <break time="40ms"/>   New Row:  , Column 1, Value: a  , Column 2, Value:  b  , Column 3, Value:  c  New Row:  , Column 1, Value:  d  , Column 2, Value:  e  , Column 3, Value:  f <break time="40ms"/>   Caption: <break time="0.3s"/>   Table to test captions and labels <break time="0.5s"/>    <break time="0.3s"/>    </speak>'))  

        # Testing caption at top
        doc = (r"\begin{table}[h!]"+
                r" \begin{center}"+
                    r"\caption{Your first table.}"+
                    r"\label{tab:table1}"+
                    "\\begin{tabular}{c c c} \n"+
                        "a & b & c \n "+
                        "d & e & f \n"+
                    "\\end{tabular} \n"+
                r"\end{center}"+
                r"\end{table}"+
                r"\end{document}")

        expand = tex2speech.aws_polly_render.start_conversion(doc)
        self.assertTrue(self._docsEqual(expand, r'<speak> Begin Table: <break time="0.3s"/>    <p> Caption: <break time="0.3s"/>   Your first table. <break time="0.5s"/>   Table Contents: <break time="40ms"/>   New Row:  , Column 1, Value: a  , Column 2, Value:  b  , Column 3, Value:  c  New Row:  , Column 1, Value:  d  , Column 2, Value:  e  , Column 3, Value:  f <break time="40ms"/>    </p>  <break time="0.3s"/>    </speak>'))  