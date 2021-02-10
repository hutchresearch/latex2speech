import unittest
from app import app
from pathlib import Path

import aws_polly_render

class BasicTestCase(unittest.TestCase):
        
        def _docsEqual(self, doc1, doc2):
                # print(str(doc1 + " \n\n\n" + str(doc2)))
                return str(doc1) == str(doc2)

        '''
        TESTS HERE CONTAIN FLASK INTERFACE ACTIONS
        '''

        '''This unit test checks if home page is functional'''
        def test_home(self):
                tester = app.test_client(self)
                pages = ['/']
                for page in pages:
                        response = tester.get(page, content_type='html/text')
                        self.assertEqual(response.status_code, 200)

        '''Unit test will ensure downloads html page will work'''
        def test_download(self):
                print("Not workingg yet")
                # tester = app.test_client(self)
                # response = tester.post('/download',
                #         follow_redirects=True
                # )
                # self.assertIn(b'you are logged in', response.data)

        ''' Unit test ensures that if user tries going to random page
            will through error'''
        def test_other(self):
                tester = app.test_client(self)
                response = tester.get('test', content_type='html/text')
                self.assertEqual(response.status_code, 404)

        '''
        TESTS HERE CONTAIN AWS POLLY RENDER FILE
        '''

        '''Tests for getting correct contents of file
           when given test document'''
        def test_get_text_file(self):
                path = Path(__file__).parent / "../../random_latex_reference/sample.tex"

                testdata = aws_polly_render.get_text_file(open(path))

                self.assertTrue(self._docsEqual(testdata, r"\documentclass{article}\usepackage{epsfig}\usepackage{hyperref}\begin{document}This is a sample file in the text formatter \LaTeX.I require you to use it for the following reasons:\end{document}"))

if __name__ == '__main__':
    unittest.main()