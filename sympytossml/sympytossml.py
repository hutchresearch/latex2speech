from sympy import *
import xml.etree.ElementTree as ET

class sympytossml:
def convert(expr):
    #print_tree(test_expr, assumptions = False)
    
    funcs_tree = ET.parse('sympy_funcs.xml')
    func_id = expr.__class__.__name__
    r = funcs_tree.getroot()
    func = r.find(func_id)
    return _convert(expr, func)

def _convert(expr, func):
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
                s += _convert(expr.args[i], func)
                i += 1
                j += 1
            
            elif func[j].tag == 'text':
                s += str(func[j].text)
                j += 1
            
            elif func[j].tag == 'repeat':
                repeat_index = j
                j += 1
    return s
         
