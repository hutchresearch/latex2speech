import unittest
import app

class BasicTestCase(unittest.TestCase):
        '''Test basic home / download pages'''
        def test_home(self):
                tester = app.test_client(self)
                pages = ['/', 'download']
                for page in pages:
                        response = tester.get(page, content_type='html/text')
                        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()