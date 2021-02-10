from sympy import symbols
import pytest
from sympytossml import *

x, y, n, a, b = symbols('x y n a b')
f, g, h = Function('f'), Function('g'), Function('h')

def test_add():
    expr = a + b + x + y
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'a plus b plus x plus y'

def test_multiply():
    expr = a * b * x * y
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'a times b times x times y'

def test_power():
    expr = a ** b
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'a to the power of b'

def test_powmul():
    expr = a ** (a * b)
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'a to the power of begin quantity a times b end quantity'

def test_begin_end_quantity():
    expr = cos(x) + f(x) + g(x + y)
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'cosine of x plus f of x plus g of begin quantity x plus y end quantity'

def test_recursive_basic():
    expr = a * (x + (b * y)) ** b
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'a times begin quantity begin quantity x plus begin quantity b times y end quantity end quantity to the power of b end quantity'

def test_equality():
    expr = Eq(x, n)
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'x equals n'

def test_inequality():
    expr = LessThan(x, n)
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'x less than or equal to n'

def test_logic():
    expr = Or(And(x, y), Not(n))
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'not n or begin quantity x and y end quantity'

def test_function_notation():
    expr = f(g(h(x)))
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'f of g of h of x'

def test_sum():
    expr = Sum(x**2, (a, 1, n))
    assert convert_sympy_ssml(expr, Quantity_Modes.QUANTITY) == 'sum of begin quantity x to the power of 2 end quantity from a equals 1 to n'
