import unittest
import tex_to_sympy

class TestTexToSympy(unittest.TestCase):

    def _equal(self, one, two):
        return str(one) == str(two)

    '''Testing basic addition/subtraction in LaTeX'''
    def testing_addition_subtraction(self):
        # Basic Addition
        equationOne = tex_to_sympy.test_sympy("1 + 2")
        self.assertTrue(self._equal(equationOne, "1 + 2"))
        # Basic Addition and Subtraction
        equationTwo = tex_to_sympy.test_sympy("1 + 2 - 3 + 4 - 1")
        self.assertTrue(self._equal(equationTwo, "-1 - 3 + 1 + 2 + 4"))
        # Basic Addition and Subtration with negative numbers
        equationThree = tex_to_sympy.test_sympy("-1 + 2 - -3 + -4 - 1")
        self.assertTrue(self._equal(equationThree, "-1 - 4 - 1 + 2 + 3"))
        # Basic Addition and Subtration with negative numbers with 0
        equationThree = tex_to_sympy.test_sympy("-1 - -0 + 2 + 0 - 0 - -3 + -4 - 1")
        self.assertTrue(self._equal(equationThree, "-1 - 4 - 1 + 2 + 3"))

    '''Testing basic multiplication/division in LaTeX'''
    def testing_multiplication_division(self):
        # Basic Multiplication
        equationOne = tex_to_sympy.test_sympy("1 * 2 * 4")
        self.assertTrue(self._equal(equationOne, "2*4"))
        # Basic Multiplication with 0
        equationTwo = tex_to_sympy.test_sympy("2 * 4 * 0 * 1000")
        self.assertTrue(self._equal(equationTwo, "1000*(0*(2*4))"))
        # Basic Multiplication with negative numbers
        equationThree = tex_to_sympy.test_sympy("2 * -4 * -1000")
        self.assertTrue(self._equal(equationThree, "(-1000)*(2*(-4))"))
        # Basic Division
        equationFour = tex_to_sympy.test_sympy("1 / 2")
        self.assertTrue(self._equal(equationFour, "1/2"))
        # Basic Division with 0
        equationFive = tex_to_sympy.test_sympy("1 / 0")
        self.assertTrue(self._equal(equationFive, "1/0"))
        # Basic Division with 0
        equationSix = tex_to_sympy.test_sympy("0 / 1")
        self.assertTrue(self._equal(equationSix, "0/1"))
        # Division with negative numbers
        equationSeven = tex_to_sympy.test_sympy("50 / -9 / -32")
        self.assertTrue(self._equal(equationSeven, "(50/((-9)))/((-32))"))

    '''Testing test_sympy() function'''
    def testing_test_sympy(self):
        # Function one test
        equation = tex_to_sympy.test_sympy("a_{n + 1} = (1 - S_n)c^2 + c(\\sqrt{(1 - S_n)^2c^2 + S_n(2-S_n)})")
        self.assertTrue(self._equal(equation, "Eq(a_{n + 1}, c**2*(1 - S_{n}) + c(sqrt(c**2*(1 - S_{n})**2 + S_{n}(2 - S_{n}))))"))

        # Function two test
        equationTwo = tex_to_sympy.test_sympy("\\frac{n!}{k!(n-k)!} = \\binom{n}{k}")
        self.assertTrue(self._equal(equationTwo, "Eq(factorial(n)/((factorial(k)*factorial(-k + n))), binom*(k*n))"))
        


if __name__ == "__main__":
    unittest.main()