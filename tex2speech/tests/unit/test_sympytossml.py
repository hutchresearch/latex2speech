from sympy import symbols
import unittest
from sympytossml import *

x, y, n, a, b = symbols('x y n a b')
f, g, h = Function('f'), Function('g'), Function('h')

# Writing test to get rid of extra spaces for testing purposes
def get_rid_of_extra_space(conversion):
    return " ".join(conversion.split())

def test_add():
    expr = a + b + x + y
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'a plus b plus x plus y'

def test_multiply():
    expr = a * b * x * y
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'a times b times x times y'

def test_power():
    expr = a ** b
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'a to the power of b'

def test_powmul():
    expr = a ** (a * b)
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'a to the power of <prosody pitch="+25%"><break time="0.3ms"/>begin quantity</prosody><break time="0.3ms"/> a times b <prosody pitch="+25%"><break time="0.3ms"/>end quantity</prosody><break time="0.3ms"/>'

def test_begin_end_quantity():
    expr = cos(x) + f(x) + g(x + y)
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'cosine of x plus f of x plus g of <prosody pitch="+25%"><break time="0.3ms"/>begin quantity</prosody><break time="0.3ms"/> x plus y <prosody pitch="+25%"><break time="0.3ms"/>end quantity</prosody><break time="0.3ms"/>'

def test_recursive_basic():
    expr = a * (x + (b * y)) ** b
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'a times <prosody pitch="+25%"><break time="0.3ms"/>begin quantity</prosody><break time="0.3ms"/> <prosody pitch="+25%"><break time="0.3ms"/>begin quantity</prosody><break time="0.3ms"/> x plus <prosody pitch="+25%"><break time="0.3ms"/>begin quantity</prosody><break time="0.3ms"/> b times y <prosody pitch="+25%"><break time="0.3ms"/>end quantity</prosody><break time="0.3ms"/> <prosody pitch="+25%"><break time="0.3ms"/>end quantity</prosody><break time="0.3ms"/> to the power of b <prosody pitch="+25%"><break time="0.3ms"/>end quantity</prosody><break time="0.3ms"/>'

def test_equality():
    expr = Eq(x, n)
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'x equals n'

def test_inequality():
    expr = LessThan(x, n)
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'x less than or equal to n'

def test_logic():
    expr = Or(And(x, y), Not(n))
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'not n or <prosody pitch="+25%"><break time="0.3ms"/>begin quantity</prosody><break time="0.3ms"/> x and y <prosody pitch="+25%"><break time="0.3ms"/>end quantity</prosody><break time="0.3ms"/>'

def test_function_notation():
    expr = f(g(h(x)))
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'f of g of h of x'

def test_sum():
    expr = Sum(x**2, (a, 1, n))
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'sum of <prosody pitch="+25%"><break time="0.3ms"/>begin quantity</prosody><break time="0.3ms"/> x to the power of 2 <prosody pitch="+25%"><break time="0.3ms"/>end quantity</prosody><break time="0.3ms"/> from a equals 1 to n'

def test_derivative():
    expr = Derivative(a, x)
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'the derivative of a with respect to x'

def test_integrals():
    expr = Integral(x, x)
    assert get_rid_of_extra_space(convert_sympy_ssml(expr, QuantityModes.QUANTITY)) == 'integral of x d x'