# import unittest
import unittest
from app import app

class BasicTestCase(unittest.TestCase):
        '''This unit test checks if home page is functional'''
        def test_home(self):
                tester = app.test_client(self)
                pages = ['/']
                for page in pages:
                        response = tester.get(page, content_type='html/text')
                        self.assertEqual(response.status_code, 200)

        ''' Unit test ensures that if user tries going to random page
            will through error'''
        def test_other(self):
                tester = app.test_client(self)
                response = tester.get('test', content_type='html/text')
                self.assertEqual(response.status_code, 404)
                
if __name__ == '__main__':
    unittest.main()