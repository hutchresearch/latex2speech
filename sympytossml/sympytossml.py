from sympy import *
import xml.etree.ElementTree as ET

quantity_start = 'begin quantity'
quantity_end = 'end quantity'

def convert(expr):
    #print_tree(test_expr, assumptions = False)
    funcs_tree = ET.parse('sympy_funcs.xml')
    return _convert(expr, funcs_tree)

def _convert(expr, funcs_tree):
    
    func_id = expr.__class__.__name__
    r = funcs_tree.getroot()
    func = r.find(func_id)
    
    s = str()
    if len(expr.args) == 0:
        s += str(expr)
    else:
        i = 0
        j = 0
        repeat_index = 0
        
        while i < len(expr.args):
            if j >= len(func):
                j = repeat_index

            if func[j].tag == 'arg':
                if isinstance(expr.args[i], Symbol):
                    s += _convert(expr.args[i], funcs_tree)
                else:
                    s += quantity_start + _convert(expr.args[i], funcs_tree) + quantity_end
                i += 1
                j += 1
            
            elif func[j].tag == 'text':
                s += str(func[j].text)
                j += 1
            
            elif func[j].tag == 'repeat':
                repeat_index = j
                j += 1
    return s
                 
