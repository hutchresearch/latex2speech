from sympy import *
import pytest
import sympytossml

def test_basic():
    x, y, n, a, b = symbols('x y n a b')
    expr1 = x + y ** (a * b)
    assert convert(expr1) == 'x plus y to the power of a times b'

def tests():
    test_basic()


tests()
