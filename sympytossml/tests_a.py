from sympy import *
import pytest
from sympytossml import *

x, y, n, a, b = symbols('x y n a b')

def test_add():
    expr = a + b + x + y
    assert convert_sympy_ssml(expr) == 'a plus b plus x plus y'

def test_multiply():
    expr = a * b * x * y
    assert convert_sympy_ssml(expr) == 'a times b times x times y'

def test_power():
    expr = a ** b
    assert convert_sympy_ssml(expr) == 'a to the power of b'

def test_powmul():
    expr = a ** (a * b)
    assert convert_sympy_ssml(expr) == 'a to the power of begin quantity a times b end quantity'

def test_recursive_basic():
    expr = a * (x + (b * y)) ** b
    assert convert_sympy_ssml(expr) == 'a times begin quantity begin quantity x plus begin quantity b times y end quantity end quantity to the power of b end quantity'
def test_equals():
    expr = x = n * a ** 2
    assert convert_sympy_ssml(expr) == 'x equals begin quantity n times begin quantity a to the power of 2 end quantity end quantity'
