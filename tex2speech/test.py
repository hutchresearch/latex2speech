from tests import *
import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)

# from tests import expand_macros_test
# import unittest

# unittest.main()