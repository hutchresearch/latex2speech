from sympy import *

def parse_ops_file(file_name):
    ops_f = open(file_name)
    ops = {}     
    
    for ln in ops_f:
        ln_lst = ln.split()
        op_name = ln_lst[0]
        ops[op_name] = list()
        for i in range(1, len(ln_lst)):
            ops[op_name].append(ln_lst[i])
    
    return ops

def op_structure(ops, op):
    return ops[str(op)] 

def convert(expr, ops):
    if len(expr.args) == 0:  
        return str(expr)
    else:
        structure = op_structure(ops, expr.__class__.__name__)
        r = ""
        for e in structure:
            if e.isdigit():
                r += convert(expr.args[int(e)], ops)
            else:
                r += e
    return r;

def basic_convert(expr):
    if len(expr.args) == 0:
        return str(expr)
    else:
        return basic_convert(expr.args[0]) + str(expr.__class__.__name__) + basic_convert(expr.args[1])

ops = parse_ops_file("operators")

x, y, n = symbols('x y n')
test_expr = Rational(1, 2) * x 
print_tree(test_expr, assumptions = False)
#test_ssml = basic_convert(test_expr)
test_ssml = convert(test_expr, ops)

print(test_ssml)
