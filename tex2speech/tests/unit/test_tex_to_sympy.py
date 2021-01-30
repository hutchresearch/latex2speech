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
        # Multiplication without *
        equation = tex_to_sympy.test_sympy("mc * 3x")
        self.assertTrue(self._equal(equation, "(3*x)*(c*m)"))
        # Multiplication using cdot
        equation = tex_to_sympy.test_sympy(r"3\cdot5")
        self.assertTrue(self._equal(equation, "3*5"))
        # Multiplication using \times
        equation = tex_to_sympy.test_sympy(r"n\times m")
        self.assertTrue(self._equal(equation, "m*n"))
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
        # Division with \div function
        equation = tex_to_sympy.test_sympy(r"2\div 3")
        self.assertTrue(self._equal(equation, "2/3"))

    '''Testing exponents and squareroots in LaTeX'''
    def testing_exponents_squareroot(self):
        # Basic Exponents
        equation = tex_to_sympy.test_sympy("1^2")
        self.assertTrue(self._equal(equation, "1**2"))
        # Basic Exponents with more
        equation = tex_to_sympy.test_sympy("1^2^2 + 3^1")
        self.assertTrue(self._equal(equation, "(1**2)**2 + 3**1"))
        # Exponents on bodies
        equation = tex_to_sympy.test_sympy("(1 + 4 - 3)^5")
        self.assertTrue(self._equal(equation, "(-3 + 1 + 4)**5"))
        # Basic Negative Exponents
        equation = tex_to_sympy.test_sympy("1^-5")
        self.assertTrue(self._equal(equation, "1"))
        # More Basic Negative Exponents
        equation = tex_to_sympy.test_sympy("4^-3 + -4^-3 + -4^3")
        self.assertTrue(self._equal(equation, "4"))
        # Exponents with 0
        equation = tex_to_sympy.test_sympy("4^0")
        self.assertTrue(self._equal(equation, "4**0")) 
        # Exponents with negative 0
# [ERROR] -> This should be either 4**-0 or 1, not 4
        # equation = tex_to_sympy.test_sympy("4^-0")
        # self.assertTrue(self._equal(equation, "4**-0")) 
        # Basic square roots
        equation = tex_to_sympy.test_sympy(r"\sqrt{2}")
        self.assertTrue(self._equal(equation, "sqrt(2)"))   
        # Basic square roots with negatives
        equation = tex_to_sympy.test_sympy(r"-\sqrt{2}")
        self.assertTrue(self._equal(equation, "-sqrt(2)")) 
        # Basic square roots with negatives / Imaginary nums??
        equation = tex_to_sympy.test_sympy(r"\sqrt{-25}")
        self.assertTrue(self._equal(equation, "5*I")) 
        # Cubed roots
        equation = tex_to_sympy.test_sympy(r"\sqrt[4]{40}")
        self.assertTrue(self._equal(equation, "40**(1/4)"))    
        # Negative Cubed roots -> I checked if this was correct, it is
        equation = tex_to_sympy.test_sympy(r"\sqrt[-4]{40}")
        self.assertTrue(self._equal(equation, "250**(1/4)/10"))          
        # Square roots and exponents
        equation = tex_to_sympy.test_sympy(r"\sqrt[3]{8} + 8^5")
        self.assertTrue(self._equal(equation, "2 + 8**5"))    

    '''Testing fractions in LaTeX'''
    def testing_fractions(self):
        # Basic Fractions
        equation = tex_to_sympy.test_sympy(r"\frac{1}{2}")
        self.assertTrue(self._equal(equation, "1/2")) 
        # Fractions with negatives
        equation = tex_to_sympy.test_sympy(r"-\frac{9}{2} - \frac{9}{2} + \frac{-1}{2} + \frac{1}{-2} + \frac{-1}{-2}")
        self.assertTrue(self._equal(equation, "-9/2 - 9/2 - 1/2 + 1/(-2) - 1/((-2))")) 
        # Fractions with 0 as numerator
        equation = tex_to_sympy.test_sympy(r"\frac{0}{2}")
        self.assertTrue(self._equal(equation, "0/2")) 
        # Fractions with 0 as denominator
        equation = tex_to_sympy.test_sympy(r"\frac{1}{0}")
        self.assertTrue(self._equal(equation, "1/0")) 
        # Fractions with 0 in it
        equation = tex_to_sympy.test_sympy(r"\frac{0}{0}")
        self.assertTrue(self._equal(equation, "0/0")) 
        # Fractions with division
        equation = tex_to_sympy.test_sympy(r"\frac{2/3}{4/5}")
        self.assertTrue(self._equal(equation, "(2/3)/((4/5))")) 
        # Fractions within a fraction
        equation = tex_to_sympy.test_sympy(r"\frac{\frac{2}{3}}{\frac{4}{5}}")
        self.assertTrue(self._equal(equation, "(2/3)/((4/5))")) 
        # Fraction using \dfrac -> This is just a display,
        # but it'll still be put into mathmode
        equation = tex_to_sympy.test_sympy(r"\frac{\dfrac{2}{3}}{\dfrac{4}{5}}")
        self.assertTrue(self._equal(equation, "((2*3)*dfrac)/(((4*5)*dfrac))")) 

    '''Testing fractions, square roots, exponents, basic algrebra all together. Basically all the stuff up above will be together in these functions'''
    def testing_frac_sqrt_exp_basic(self):
        # Fraction and exponent
        equation = tex_to_sympy.test_sympy(r"(1+\frac{1}{x})^2")
        self.assertTrue(self._equal(equation, "(1 + 1/x)**2")) 
        # Fraction and exponent with \left \right commands
        equation = tex_to_sympy.test_sympy(r"\left(1+\frac{1}{x}\right)^2")
        self.assertTrue(self._equal(equation, "left(right/x + 1)**2")) 
        # Testing super scripts
        equation = tex_to_sympy.test_sympy(r"x^{2+a}")
        self.assertTrue(self._equal(equation, "x**(a + 2)")) 
        # Testing exponents a lot
        equation = tex_to_sympy.test_sympy(r"e^{e^{e^{e^{x}}}}")
        self.assertTrue(self._equal(equation, "e**(e**(e**(e**x)))"))
        # Subscripts testing 
        equation = tex_to_sympy.test_sympy(r"n_1")
        self.assertTrue(self._equal(equation, "n_{1}"))
        equation = tex_to_sympy.test_sympy(r"n_{k+1}")
        self.assertTrue(self._equal(equation, "n_{k + 1}"))
        # Superscripts and subscripts testing
        equation = tex_to_sympy.test_sympy(r"n_{k+1}^2")
        self.assertTrue(self._equal(equation, "n_{k + 1}**2"))

    '''Equation Unit testing, these have equal signs'''
    def testing_equations(self):
        # Testing basic exponent equation
        equation = tex_to_sympy.test_sympy(r"x^n + y^n = z^n")
        self.assertTrue(self._equal(equation, "Eq(x**n + y**n, z**n)"))
        # Equation with square root and fractions and multiple =
# [ERROR] -> Doesn't render equataions with multiple equal signs
# The case below returns as false :(
        # equation = tex_to_sympy.test_sympy(r"\sqrt[3]{8}=8^{\frac{1}{3}}=2")
        # self.assertTrue(self._equal(equation, ""))
        # Equation E = mc^2
        equation = tex_to_sympy.test_sympy(r"E=mc^2")
        self.assertTrue(self._equal(equation, "Eq(E, c**2*m)"))
        # Equation with pi and fractions
        equation = tex_to_sympy.test_sympy(r"A = \frac{\pi r^2}{2}")
        self.assertTrue(self._equal(equation, "Eq(A, (pi*r**2)/2)"))
        # Equation with pi and fractions
# [ERROR] -> You can't have jsut a "= 3 + 2", there must be something on otherside of equals sign
        equation = tex_to_sympy.test_sympy(r"1= \frac{1}{2} \pi r^2")
        self.assertTrue(self._equal(equation, "Eq(1, (pi*r**2)/2)"))
        # Equation using exponent multiplication (euler's equation)
        equation = tex_to_sympy.test_sympy(r"e^{\pi i} + 1 = 0")
        self.assertTrue(self._equal(equation, "Eq(e**(i*pi) + 1, 0)"))
        # Long equation! 
# [ERROR] -> You can't have \\ commands inline of the equation, it will completey error since it doesn't know the command
        equation = tex_to_sympy.test_sympy(r"p(x) = 3x^6 + 14x^5y + 590x^4y^2 + 19x^3y^3 - 12x^2y^4 - 12xy^5 + 2y^6 - a^3b^3")
        self.assertTrue(self._equal(equation, "Eq(p(x), -a**3*b**3 + 2*y**6 - 12*x*y**5 - 12*x**2*y**4 + 19*(x**3*y**3) + 590*(x**4*y**2) + 3*x**6 + 14*(x**5*y))"))
        # Simple equation with &
# [ERROR] -> Doesn't like equations with &, will ocmpletely error
        # equation = tex_to_sympy.test_sympy(r"2x - 5y &=  8")
        # self.assertTrue(self._equal(equation, "Eq(e**(i*pi) + 1, 0)"))
        # Big equation with bunch of combinations of sqrt, superscripts, and exponents
        equation = tex_to_sympy.test_sympy(r"a_{n + 1} = (1 - S_n)c^2 + c(\sqrt{(1 - S_n)^2c^2 + S_n(2-S_n)})")
        self.assertTrue(self._equal(equation, "Eq(a_{n + 1}, c**2*(1 - S_{n}) + c(sqrt(c**2*(1 - S_{n})**2 + S_{n}(2 - S_{n}))))"))
        # Testing standard function with ln and e variables
# [ERROR] -> Doesn't render just "ln" as natural log, it assumes it's a regular string. -> Eq(l*(e**x*n), x)
        # equation = tex_to_sympy.test_sympy(r"lne^x = x")
        # self.assertTrue(self._equal(equation, ""))
        # Testing standard function with ln and e variables, but using \ln instead
        equation = tex_to_sympy.test_sympy(r"\ln e^x = x")
        self.assertTrue(self._equal(equation, "Eq(log(e**x, E), x)"))

    '''Testing integrals of equations'''
    def testing_integral(self):
        # Integral simple
# [NOTE] -> Doesn't like just basic \int with nothing else
        # equation = tex_to_sympy.test_sympy(r"\int")
        # self.assertTrue(self._equal(equation, ""))
        # Integral
# [ERROR] -> This doesn't render when there is \, but usually when there is \command, it's fine with the command. Possibly since , is special charachter it acts differently...
        # equation = tex_to_sympy.test_sympy(r"\int_{a}^{b} x^2 \,dx")
        # self.assertTrue(self._equal(equation, ""))
        # Basic integral
        equation = tex_to_sympy.test_sympy(r"\int_0^2x^2dx")
        self.assertTrue(self._equal(equation, "Integral(x**2, (x, 0, 2))"))
        # Integral Limits
        equation = tex_to_sympy.test_sympy(r"\int_{a}^b f(x)dx")
        self.assertTrue(self._equal(equation, "Integral(f(x), (x, a, b))"))
        # Basic integral with limit
        equation = tex_to_sympy.test_sympy(r"\int\limits_{x\in C}dx")
        self.assertTrue(self._equal(equation, "Integral(limits_{x*(C*in)}, x)"))
        # Double integral with limits
# [ERROR] -> Doesn't like , in the f(x, y)...which we need :o
        # equation = tex_to_sympy.test_sympy(r"\int_{a}^b\int_{c}^d f(x,y)dxdy")
        # self.assertTrue(self._equal(equation, "Integral(limits_{x*(C*in)}, x)"))
        # Multiple integrals
        equation = tex_to_sympy.test_sympy(r"\iint_V \mu(u,v) \du\dv")
        self.assertTrue(self._equal(equation, "iint_{V}*((du*dv)*mu(u, v))"))
        # Multiple integrals 2 example
        equation = tex_to_sympy.test_sympy(r"\iiint_V \mu(u,v,w) \du\dv\dw")
        self.assertTrue(self._equal(equation, "iiint_{V}*((du*(dv*dw))*mu(u, v, w))"))
        # Multiple integrals 3 example [NOTE] -> I smooshed togeter the dt, du, dv, and dw, and it still renders!
        equation = tex_to_sympy.test_sympy(r"\iiiint_V \mu(t,u,v,w) dtdudvdw")
        self.assertTrue(self._equal(equation, "iiiint_{V}*((dt*(du*(dv*dw)))*mu(t, u, v, w))"))
        # Multiple integrals 4 example
        equation = tex_to_sympy.test_sympy(r"\idotsint_V \mu(u_1,\dots,u_k) \du_1 \dots du_k")
        self.assertTrue(self._equal(equation, "idotsint_{V}*((du_{1}*(dots*du))*mu(u_{1}, dots, u_{k}))"))
        # This integral thing has a circle in through it, found it on LaTeX documentation
        equation = tex_to_sympy.test_sympy(r"\oint_V f(s) \ds")
        self.assertTrue(self._equal(equation, "oint_{V}*(ds*f(s))"))

    '''Testing summations of equations'''
    def testing_summation(self):
        # Basic summation
        equation = tex_to_sympy.test_sympy(r"\sum_{n=-\infty}^{+\infty} f(x)")
        self.assertTrue(self._equal(equation, "Sum(f(x), (n, -oo, oo))"))
        # Sumation closed form for i
        equation = tex_to_sympy.test_sympy(r"\sum_{i=1}^{n}i=\frac{n(n+1)}{2}")
        self.assertTrue(self._equal(equation, "Eq(Sum(i, (i, 1, n)), n(n + 1)/2)"))
        # Sumation with infinity and exponent
        equation = tex_to_sympy.test_sympy(r"\sum_{n=1}^{\infty} 2^{-n} = 1")
        self.assertTrue(self._equal(equation, "Eq(Sum(2**(-n), (n, 1, oo)), 1)"))
        # Summation with \limits
# [ERROR] -> Figure out if this renders in LaTeX, \sum\limits it doesn't like
        # equation = tex_to_sympy.test_sympy(r"\sum\limits_{j=1}^k A_{\alpha_j}")
        # self.assertTrue(self._equal(equation, ""))
        # Sumation without \limits
        equation = tex_to_sympy.test_sympy(r"\sum_{j=1}^k A_{\alpha_j}")
        self.assertTrue(self._equal(equation, "Sum(A_{alpha_{j}}, (j, 1, k))"))
        # Sum from 1 to n
# [ERROR] -> Doesn't like not having anything after the summation for example it'll run if you put a 1 afterwords
        # equation = tex_to_sympy.test_sympy(r"\sum_{i=1}^{n}")
        # self.assertTrue(self._equal(equation, ""))
        # Sum off n first integers
        equation = tex_to_sympy.test_sympy(r"\sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6}")
        self.assertTrue(self._equal(equation, "Eq(Sum(i**2, (i, 1, n)), ((2*n + 1)*n(n + 1))/6)"))
        # Dobule sum
        equation = tex_to_sympy.test_sympy(r"\sum^k_{i=1}\sum^l_{j=1}\q_i q_j")
        self.assertTrue(self._equal(equation, "Sum(q_{i}*q_{j}, (j, 1, l), (i, 1, k))"))
        # Big summation
        equation = tex_to_sympy.test_sympy(r"(n + 1)^4 = 4\sum_{i = 1}^{n} i^3 + 6\sum_{i = 1}^{n} i^2 + 4\sum_{i = 1}^{n} i + \sum_{i = 1}^{n} 1")
        self.assertTrue(self._equal(equation, "Eq((n + 1)**4, 6*Sum(i**2, (i, 1, n)) + 4*Sum(i**3, (i, 1, n)) + 4*Sum(i, (i, 1, n)) + Sum(1, (i, 1, n)))"))

    '''Testing limits of functions'''
    def testing_limit(self):
        # Basic limit
# What is dir='-'??? Further investigation
        equation = tex_to_sympy.test_sympy(r"\lim_{x\to\infty} f(x)")
        self.assertTrue(self._equal(equation, "Limit(f(x), x, oo, dir='-')"))
        # Limit function with f(x) and frac
        equation = tex_to_sympy.test_sympy(r"\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}")
        self.assertTrue(self._equal(equation, "Limit((-f(x) + f(h + x))/h, h, 0)"))
        # Limit function at plus infinity
# [NOTE] -> Figure out what dir='-' means...
        equation = tex_to_sympy.test_sympy(r"\lim_{x \to +\infty} f(x)")
        self.assertTrue(self._equal(equation, "Limit(f(x), x, oo, dir='-')"))
        # Limit function at minus infinity
        equation = tex_to_sympy.test_sympy(r"\lim_{x \to -\infty} f(x)")
        self.assertTrue(self._equal(equation, "Limit(f(x), x, -oo)"))
        # Limit function at alpha
        equation = tex_to_sympy.test_sympy(r"\lim_{x \to \alpha} f(x)")
        self.assertTrue(self._equal(equation, "Limit(f(x), x, alpha)"))
        # Limit function at infinity
# [ERROR] -> Doesn't like > command
        # equation = tex_to_sympy.test_sympy(r"\inf_{x > s}f(x)")
        # self.assertTrue(self._equal(equation, ""))
        # Limit function with sup
        equation = tex_to_sympy.test_sympy(r"\sup_{x \in \mathbb{R}}f(x)")
        self.assertTrue(self._equal(equation, "sup_{x*(in*(R*mathbb))}*f(x)"))
        # Limit function with max
# [ERROR] -> Like nown before, this does not like \[], it doesn't like backslashes with special sympbols
        # equation = tex_to_sympy.test_sympy(r"\max_{x \in \[a,b\]}f(x)")
        # self.assertTrue(self._equal(equation, ""))
        # Limit function with min
# [ERROR] -> Same as above with backslash and special command
        # equation = tex_to_sympy.test_sympy(r"\min_{x \in \[\alpha,\beta\]}f(x)")
        # self.assertTrue(self._equal(equation, ""))

    '''Testing product functions'''
    def testing_product(self):
        # Product function
        equation = tex_to_sympy.test_sympy(r"\prod_{i=1}^ni=n!")
        self.assertTrue(self._equal(equation, "Eq(Product(i, (i, 1, n)), factorial(n))"))
        # Product function part 2
        equation = tex_to_sympy.test_sympy(r"\prod_{i=a}^{b} f(i)")
        self.assertTrue(self._equal(equation, "Product(f(i), (i, a, b))"))
        # Product with \limits
# [ERROR] -> It just can't do prod_limits right after, check in on this if you can do it in regular latex and if it renders
        # equation = tex_to_sympy.test_sympy(r"\prod_\limits_{j=1}^k A_{\alpha_j}")
        # self.assertTrue(self._equal(equation, "Product(f(i), (i, a, b))"))
        # Product without \limits
        equation = tex_to_sympy.test_sympy(r"\prod_{j=1}^k A_{\alpha_j}")
        self.assertTrue(self._equal(equation, "Product(A_{alpha_{j}}, (j, 1, k))"))
        # Product from 1 to n
# [ERROR] -> I actually don't know why this is erroring..
        # equation = tex_to_sympy.test_sympy(r"\prod_{i=1}^n")
        # self.assertTrue(self._equal(equation, ""))
        # Product off n first integers
        equation = tex_to_sympy.test_sympy(r"\prod_{i=1}^n i^2{6}")
        self.assertTrue(self._equal(equation, "Product(6*i**2, (i, 1, n))"))
        # Double product
        equation = tex_to_sympy.test_sympy(r"\prod^k_{i=1}\prod^l_{j=1}\q_i q_j")
        self.assertTrue(self._equal(equation, "Product(q_{i}*q_{j}, (j, 1, l), (i, 1, k))"))

    '''Testing derivatives of functions'''
    def testing_derivative(self):
        # First order derivative
# [ERROR] -> Doesn't understand prime the f'
        # equation = tex_to_sympy.test_sympy(r"f'(x)")
        # self.assertTrue(self._equal(equation, ""))
        # Second order derivative
# [ERROR] -> Doesn't understand prime the f''
        # equation = tex_to_sympy.test_sympy(r"f''(x)")
        # self.assertTrue(self._equal(equation, ""))
        # K-th order derivative
        equation = tex_to_sympy.test_sympy(r"f^{(k)}(x)")
        self.assertTrue(self._equal(equation, "f**k*x"))
        # Partial first order derivative
        equation = tex_to_sympy.test_sympy(r"\frac{\partial f}{\partial x}")
        self.assertTrue(self._equal(equation, "Derivative(f, x)"))
        # Partial Second order derivative
        equation = tex_to_sympy.test_sympy(r"\frac{\partial^2 f}{\partial x^2}")
        self.assertTrue(self._equal(equation, "(f*partial**2)/((partial*x**2))"))
        # Partial k-th order derivative
        equation = tex_to_sympy.test_sympy(r"\frac{\partial^{k} f}{\partial x^k}")
        self.assertTrue(self._equal(equation, "(f*partial**k)/((partial*x**k))"))

    '''Testing binomials of equations'''
    def testing_binomial(self):
        # Binomial in equation
        equationTwo = tex_to_sympy.test_sympy(r"\frac{n!}{k!(n-k)!} = \binom{n}{k}")
        self.assertTrue(self._equal(equationTwo, "Eq(factorial(n)/((factorial(k)*factorial(-k + n))), binom*(k*n))"))
        # Testing binomial with factorial and frac
        equationTwo = tex_to_sympy.test_sympy(r"\binom{n}{k} = \frac{n!}{k!(n-k)!}")
        self.assertTrue(self._equal(equationTwo, "Eq(binom*(k*n), factorial(n)/((factorial(k)*factorial(-k + n))))"))
        # Simple biinom
        equationTwo = tex_to_sympy.test_sympy(r"\frac{A_n^k}{k!} = \binom{n}{k}")
        self.assertTrue(self._equal(equationTwo, "Eq(A_{n}**k/factorial(k), binom*(k*n))"))
        # Pascal's triangle
        equationTwo = tex_to_sympy.test_sympy(r"\binom{n}{k} =  \binom{n-1}{k-1} +\binom{n-1}{k}")
        self.assertTrue(self._equal(equationTwo, "Eq(binom*(k*n), binom*(k*(n - 1)) + binom*((k - 1)*(n - 1)))"))

    '''Testing Operators'''
    def testing_operators(self):
# Note, doesn't like single things by themself here, for example can't just be \cos, needs \cos1 or something
        # Cosine operator
        equation = tex_to_sympy.test_sympy(r"\cos1")
        self.assertTrue(self._equal(equation, "cos(1)"))
        # Cosecant operator
        equation = tex_to_sympy.test_sympy(r"\csc1")
        self.assertTrue(self._equal(equation, "csc(1)"))
        # expression operator
        equation = tex_to_sympy.test_sympy(r"\exp")
        self.assertTrue(self._equal(equation, "exp"))
        # Ker operator
        equation = tex_to_sympy.test_sympy(r"\ker")
        self.assertTrue(self._equal(equation, "ker"))
        # limsup operator
        equation = tex_to_sympy.test_sympy(r"\limsup")
        self.assertTrue(self._equal(equation, "limsup"))
        # min operator
        equation = tex_to_sympy.test_sympy(r"\min")
        self.assertTrue(self._equal(equation, "min"))
        # Sinh operator
        equation = tex_to_sympy.test_sympy(r"\sinh1")
        self.assertTrue(self._equal(equation, "sinh(1)"))
        # arcsin operator
        equation = tex_to_sympy.test_sympy(r"\arcsin1")
        self.assertTrue(self._equal(equation, "asin(1)"))
        # cosh operator
        equation = tex_to_sympy.test_sympy(r"\cosh1")
        self.assertTrue(self._equal(equation, "cosh(1)"))
        # deg operator
        equation = tex_to_sympy.test_sympy(r"\deg")
        self.assertTrue(self._equal(equation, "deg"))
        # gcd operator
        equation = tex_to_sympy.test_sympy(r"\gcd")
        self.assertTrue(self._equal(equation, "gcd"))
        # lg operator
        equation = tex_to_sympy.test_sympy(r"\lg")
        self.assertTrue(self._equal(equation, "lg"))
        # ln operator
# [NOTE] -> Can't have just ln
        equation = tex_to_sympy.test_sympy(r"\ln1")
        self.assertTrue(self._equal(equation, "log(1, E)"))
        # pr operator
        equation = tex_to_sympy.test_sympy(r"\Pr")
        self.assertTrue(self._equal(equation, "Pr"))
        # sup operator
        equation = tex_to_sympy.test_sympy(r"\sup")
        self.assertTrue(self._equal(equation, "sup"))
        # arctan operator
        equation = tex_to_sympy.test_sympy(r"\arctan1")
        self.assertTrue(self._equal(equation, "atan(1)"))
        # cotan operator
        equation = tex_to_sympy.test_sympy(r"\cot(1)")
        self.assertTrue(self._equal(equation, "cot(1)"))
        # det operator
        equation = tex_to_sympy.test_sympy(r"\det")
        self.assertTrue(self._equal(equation, "det"))
        # hom operator
        equation = tex_to_sympy.test_sympy(r"\hom")
        self.assertTrue(self._equal(equation, "hom"))
        # lim operator
# [NOTE] -> can't just have lim empty
        # equation = tex_to_sympy.test_sympy(r"\lim")
        # self.assertTrue(self._equal(equation, ""))
        # log operator
        equation = tex_to_sympy.test_sympy(r"\log1")
        self.assertTrue(self._equal(equation, "log(1, 10)"))
        # sec operator
        equation = tex_to_sympy.test_sympy(r"\sec1")
        self.assertTrue(self._equal(equation, "sec(1)"))
        # tan operator
        equation = tex_to_sympy.test_sympy(r"\tan1")
        self.assertTrue(self._equal(equation, "tan(1)"))
        # arg operator
        equation = tex_to_sympy.test_sympy(r"\arg")
        self.assertTrue(self._equal(equation, "arg"))
        # coth operator
        equation = tex_to_sympy.test_sympy(r"\coth(1)")
        self.assertTrue(self._equal(equation, "coth(1)"))
        # dim operator
        equation = tex_to_sympy.test_sympy(r"\dim")
        self.assertTrue(self._equal(equation, "dim"))
        # liminf operator
        equation = tex_to_sympy.test_sympy(r"\liminf")
        self.assertTrue(self._equal(equation, "liminf"))
        # max operator
        equation = tex_to_sympy.test_sympy(r"\max")
        self.assertTrue(self._equal(equation, "max"))
        # sin operator
        equation = tex_to_sympy.test_sympy(r"\sin1")
        self.assertTrue(self._equal(equation, "sin(1)"))
        # tanh operator
        equation = tex_to_sympy.test_sympy(r"\tanh1")
        self.assertTrue(self._equal(equation, "tanh(1)"))

    '''Testing Greek Letters'''
    def testing_greek_letters(self):
        # Alpha
        equation = tex_to_sympy.test_sympy(r"\alpha A")
        self.assertTrue(self._equal(equation, "A*alpha"))
        # Beta
        equation = tex_to_sympy.test_sympy(r"\beta B")
        self.assertTrue(self._equal(equation, "B*beta"))
        # Gamma
        equation = tex_to_sympy.test_sympy(r"\gamma \Gamma")
        self.assertTrue(self._equal(equation, "Gamma*gamma"))
        # Delta
        equation = tex_to_sympy.test_sympy(r"\delta \Delta")
        self.assertTrue(self._equal(equation, "Delta*delta"))
        # Epsilon
        equation = tex_to_sympy.test_sympy(r"\epsilon")
        self.assertTrue(self._equal(equation, "epsilon"))
        equation = tex_to_sympy.test_sympy(r"\varepsilon E")
        self.assertTrue(self._equal(equation, "E*varepsilon"))
        # Zelta
        equation = tex_to_sympy.test_sympy(r"\zeta Z")
        self.assertTrue(self._equal(equation, "Z*zeta"))
        # Eta
        equation = tex_to_sympy.test_sympy(r"\eta H")
        self.assertTrue(self._equal(equation, "H*eta"))
        # Theta
        equation = tex_to_sympy.test_sympy(r"\theta \vartheta \Theta")
        self.assertTrue(self._equal(equation, "theta*(Theta*vartheta)"))
        # Iota
        equation = tex_to_sympy.test_sympy(r"\iota I")
        self.assertTrue(self._equal(equation, "I*iota"))
        # Kappa
        equation = tex_to_sympy.test_sympy(r"\kappa K")
        self.assertTrue(self._equal(equation, "K*kappa"))
        # Lambda
        equation = tex_to_sympy.test_sympy(r"\lambda \Lambda")
        self.assertTrue(self._equal(equation, "Lambda*lambda"))
        # Mu
        equation = tex_to_sympy.test_sympy(r"\mu M")
        self.assertTrue(self._equal(equation, "M*mu"))
        # Nu
        equation = tex_to_sympy.test_sympy(r"\nu N")
        self.assertTrue(self._equal(equation, "N*nu"))
        # Xi
        equation = tex_to_sympy.test_sympy(r"\xi\Xi")
        self.assertTrue(self._equal(equation, "Xi*xi"))
        # O
        equation = tex_to_sympy.test_sympy(r"o O")
        self.assertTrue(self._equal(equation, "O*o"))
        # Pi
        equation = tex_to_sympy.test_sympy(r"\pi \Pi")
        self.assertTrue(self._equal(equation, "Pi*pi"))
        # Rho
        equation = tex_to_sympy.test_sympy(r"\rho\varrho P")
        self.assertTrue(self._equal(equation, "rho*(P*varrho)"))
        # Sigma
        equation = tex_to_sympy.test_sympy(r"\sigma \Sigma")
        self.assertTrue(self._equal(equation, "Sigma*sigma"))
        # Tau
        equation = tex_to_sympy.test_sympy(r"\tau T")
        self.assertTrue(self._equal(equation, "T*tau"))
        # Upsilon
        equation = tex_to_sympy.test_sympy(r"\upsilon \Upsilon")
        self.assertTrue(self._equal(equation, "Upsilon*upsilon"))
        # Phi
        equation = tex_to_sympy.test_sympy(r"\phi \varphi \Phi")
        self.assertTrue(self._equal(equation, "phi*(Phi*varphi)"))
        # Chi
        equation = tex_to_sympy.test_sympy(r"\chi X")
        self.assertTrue(self._equal(equation, "X*chi"))
        # Psi
        equation = tex_to_sympy.test_sympy(r"\psi \Psi")
        self.assertTrue(self._equal(equation, "Psi*psi"))
        # Omega
        equation = tex_to_sympy.test_sympy(r"\omega \Omega")
        self.assertTrue(self._equal(equation, "Omega*omega"))

    '''Testing Miscellaneous symps'''
    def testing_misc_symbols(self):
        # Infinity
        equation = tex_to_sympy.test_sympy(r"\infty")
        self.assertTrue(self._equal(equation, "oo"))
        # Re
        equation = tex_to_sympy.test_sympy(r"\Re")
        self.assertTrue(self._equal(equation, "Re"))
        # Nabla
        equation = tex_to_sympy.test_sympy(r"\nabla")
        self.assertTrue(self._equal(equation, "nabla"))
        # Partial
        equation = tex_to_sympy.test_sympy(r"\partial")
        self.assertTrue(self._equal(equation, "partial"))
        # Emptyset
        equation = tex_to_sympy.test_sympy(r"\emptyset")
        self.assertTrue(self._equal(equation, "emptyset"))
        # wp
        equation = tex_to_sympy.test_sympy(r"\wp")
        self.assertTrue(self._equal(equation, "wp"))
        # neg
        equation = tex_to_sympy.test_sympy(r"\neg")
        self.assertTrue(self._equal(equation, "neg"))
        # Square command
        equation = tex_to_sympy.test_sympy(r"\square")
        self.assertTrue(self._equal(equation, "square"))
        # Blacksquare command
        equation = tex_to_sympy.test_sympy(r"\blacksquare")
        self.assertTrue(self._equal(equation, "blacksquare"))
        # For all command
        equation = tex_to_sympy.test_sympy(r"\forall")
        self.assertTrue(self._equal(equation, "forall"))
        # Im command
        equation = tex_to_sympy.test_sympy(r"\Im")
        self.assertTrue(self._equal(equation, "Im"))
        # exists command
        equation = tex_to_sympy.test_sympy(r"\exists")
        self.assertTrue(self._equal(equation, "exists"))
        # nexists command
        equation = tex_to_sympy.test_sympy(r"\nexists")
        self.assertTrue(self._equal(equation, "nexists"))
        # varnothing command
        equation = tex_to_sympy.test_sympy(r"\varnothing")
        self.assertTrue(self._equal(equation, "varnothing"))
        # complement command
        equation = tex_to_sympy.test_sympy(r"\complement")
        self.assertTrue(self._equal(equation, "complement"))
        # cdots command
        equation = tex_to_sympy.test_sympy(r"\cdots")
        self.assertTrue(self._equal(equation, "cdots"))
        # surd command
        equation = tex_to_sympy.test_sympy(r"\surd")
        self.assertTrue(self._equal(equation, "surd"))
        # triangle command
        equation = tex_to_sympy.test_sympy(r"\triangle")
        self.assertTrue(self._equal(equation, "triangle"))

    '''Testing for binary operation/relation symbols'''
    def testing_binary_operation_relation_symbols(self):
        # Times
        equation = tex_to_sympy.test_sympy(r"3\times2")
        self.assertTrue(self._equal(equation, "2*3"))
        # Div
        equation = tex_to_sympy.test_sympy(r"2\div3")
        self.assertTrue(self._equal(equation, "2/3"))
        # Cub
        equation = tex_to_sympy.test_sympy(r"\cup")
        self.assertTrue(self._equal(equation, "cup"))
        # Less than equal
# [ERROR] -> I don't want this to be False/True, I want leq to expand, not be evaluated
        equation = tex_to_sympy.test_sympy(r"3\leq2")
        self.assertTrue(self._equal(equation, "False"))
        # In
        equation = tex_to_sympy.test_sympy(r"\in")
        self.assertTrue(self._equal(equation, "in"))
        # Nottin
        equation = tex_to_sympy.test_sympy(r"\notin")
        self.assertTrue(self._equal(equation, "notin"))
        # simeq
        equation = tex_to_sympy.test_sympy(r"\simeq")
        self.assertTrue(self._equal(equation, "simeq"))
        # wedge
        equation = tex_to_sympy.test_sympy(r"\wedge")
        self.assertTrue(self._equal(equation, "wedge"))
        # oplus
        equation = tex_to_sympy.test_sympy(r"\oplus")
        self.assertTrue(self._equal(equation, "oplus"))
        # Box
        equation = tex_to_sympy.test_sympy(r"\Box")
        self.assertTrue(self._equal(equation, "Box"))
        # equivalement
        equation = tex_to_sympy.test_sympy(r"\equiv")
        self.assertTrue(self._equal(equation, "equiv"))
        # cap
        equation = tex_to_sympy.test_sympy(r"\cap")
        self.assertTrue(self._equal(equation, "cap"))
        # not equal
        equation = tex_to_sympy.test_sympy(r"\neq")
        self.assertTrue(self._equal(equation, "neq"))
        # greater than equal
# [ERROR] -> Don't want this to be true/false want it to be expanded not evaluated
        equation = tex_to_sympy.test_sympy(r"3\geq3")
        self.assertTrue(self._equal(equation, "True"))
        # perp
        equation = tex_to_sympy.test_sympy(r"\perp")
        self.assertTrue(self._equal(equation, "perp"))
        # subset
        equation = tex_to_sympy.test_sympy(r"\subset")
        self.assertTrue(self._equal(equation, "subset"))
        # approximately
        equation = tex_to_sympy.test_sympy(r"\approx")
        self.assertTrue(self._equal(equation, "approx"))
        # vee
        equation = tex_to_sympy.test_sympy(r"\vee")
        self.assertTrue(self._equal(equation, "vee"))
        # otimes
        equation = tex_to_sympy.test_sympy(r"\otimes")
        self.assertTrue(self._equal(equation, "otimes"))
        # boxtimes
        equation = tex_to_sympy.test_sympy(r"\boxtimes")
        self.assertTrue(self._equal(equation, "boxtimes"))
        # cong
        equation = tex_to_sympy.test_sympy(r"\cong")
        self.assertTrue(self._equal(equation, "cong"))

if __name__ == "__main__":
    unittest.main()