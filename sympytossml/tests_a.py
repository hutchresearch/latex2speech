from sympy import *
import pytest
from sympytossml import *

x, y, n, a, b = symbols('x y n a b')

def test_add():
    expr = a + b + x + y
    assert convert(expr) == 'a plus b plus x plus y'

def test_multiply():
    expr = a * b * x * y
    assert convert(expr) == 'a times b times x times y'

def test_power():
    expr = a ** b
    assert convert(expr) == 'a to the power of b'

def test_powmul():
    expr = a ** (a * b)
    assert convert(expr) == 'a to the power of begin quantity a times b end quantity'

def test_recursive_basic():
    expr = a * (x + (b * y)) ** b
    assert convert(expr) == 'a times begin quantity x plus begin quantity b times y end quantity end quantity to the power of b'
