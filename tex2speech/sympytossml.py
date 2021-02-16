from sympy import *
import xml.etree.ElementTree as ET
from enum import Enum
import inflect
import re

infl = inflect.engine()

class Quantity_Modes(Enum):
    NO_INDICATOR = 0
    QUANTITY = 1
    QUANTITY_NUMBERED = 2
    PARENTHESES = 3
    PARENTHESES_NUMBERED = 4

sympy_funcs_file = './static/sympy_funcs.xml' 

begin_str = 'begin'
end_str = 'end'
quantity_str = 'quantity'
parentheses_str = 'parentheses'

def ordinal_str(num):
    return infl.number_to_words(infl.ordinal(num))

def remove_extra_spaces(str):
    re.sub(' +', ' ', str)
    if str[0] == ' ':
        str = str[1:]
    if str[len(str) - 1] == ' ':
        str = str[:(len(str) - 1)]
    return str

def convert_sympy_ssml(expr, mode):
    #print_tree(expr, assumptions = False)
    funcs_tree = ET.parse(sympy_funcs_file)
    s = _convert(expr, funcs_tree, mode, 1)
    s = remove_extra_spaces(s)
    return s
    
def _convert(expr, funcs_tree, mode, quantity_index):
    
    func_id = expr.__class__.__name__
    r = funcs_tree.getroot()
    func = r.find(func_id)
    
    s = str()
    
    if func == None:
        func = r.find('userFunction')
        
    if len(expr.args) == 0:
        s += ' ' + str(expr) + ' '
    else:
        i = 0
        i_sub = 0
        j = 0
        repeat_index = 0
        
        while i < len(expr.args):
            if j >= len(func):
                j = repeat_index
            
            if func[j].tag == 'arg':
                if isinstance(expr.args[i], Atom): 
                    s += _convert(expr.args[i], funcs_tree, mode, quantity_index)
                elif len(expr.args[i].args) == 1:
                    s += ' ' + _convert(expr.args[i], funcs_tree, mode, quantity_index) + ' '
                else:
                    if mode == Quantity_Modes.PARENTHESES:
                        s += ' ' + begin_str + ' ' + \
                        parentheses_str + _convert(expr.args[i], funcs_tree, mode, quantity_index + 1) + \
                        end_str + ' ' + parentheses_str + ' '

                    if mode == Quantity_Modes.QUANTITY:
                        print("Yo " + str(expr.args[i]))
                        s += ' ' + begin_str + ' ' + \
                        quantity_str +  _convert(expr.args[i], funcs_tree, mode, quantity_index + 1) + \
                        end_str + ' ' +  quantity_str + ' '

                    if mode == Quantity_Modes.PARENTHESES_NUMBERED:
                        s += ' ' + begin_str + ' ' + ordinal_str(quantity_index) + ' ' + \
                        parentheses_str + _convert(expr.args[i], funcs_tree, mode, quantity_index + 1) + \
                            end_str + ' ' + ordinal_str(quantity_index) + ' ' + parentheses_str + ' '

                    if mode == Quantity_Modes.QUANTITY_NUMBERED:
                        s += ' ' + begin_str + ' ' + ordinal_str(quantity_index) + ' ' + \
                        quantity_str + _convert(expr.args[i], funcs_tree, mode, quantity_index + 1) + \
                        end_str + ' ' + ordinal_str(quantity_index) + ' ' + quantity_str + ' ' 
                
                quantity_index += 1
                i_sub = 0
                i += 1
                j += 1
            
            elif func[j].tag == 'subarg':
                s += _convert(expr.args[i].args[i_sub], funcs_tree, mode, quantity_index)
                i_sub += 1
                if i_sub == len(expr.args[i].args):
                    i += 1
                j += i

            elif func[j].tag == 'funcname':
                s += ' ' + func_id + ' '
                j += 1

            elif func[j].tag == 'text':
                s += str(func[j].text)
                j += 1
            
            elif func[j].tag == 'repeat':
                repeat_index = j
                j += 1
    return s
                 
