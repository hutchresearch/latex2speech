from sympy import *
import xml.etree.ElementTree as ET
from enum import Enum
import inflect
import re
from logger import logging, writelog

infl = inflect.engine()

class QuantityModes(Enum):
    NO_INDICATOR = 0
    QUANTITY = 1
    QUANTITY_NUMBERED = 2
    PARENTHESES = 3
    PARENTHESES_NUMBERED = 4

sympy_funcs_file = './static/sympy_funcs.xml' 


begin_str = '<prosody pitch=\"+25%\"><break time=\"0.3ms\"/>begin'
end_str = '<prosody pitch=\"+25%\"><break time=\"0.3ms\"/>end'
quantity_str = 'quantity</prosody><break time=\"0.3ms\"/>'
parentheses_str = 'parentheses</prosody><break time=\"0.3ms\"/>'

def ordinal_str(num):
    return infl.number_to_words(infl.ordinal(num))

def remove_extra_spaces(str):
    return " ".join(str.split())

'''
Convert SymPy object expr to english words.
Mode defines how quantities should be denoted.
'''
def convert_sympy_ssml(expr, mode):
    funcs_tree = ET.parse(sympy_funcs_file)
    s = _convert(expr, funcs_tree, mode, 1, True)
    s = remove_extra_spaces(s)
    # Hack to overcome the fact that sympy does not support 'plus or minus' or 'minus'
    s = s.replace('times pm times', 'plus or minus')
    s = s.replace('plus -', 'minus')
    # Infinity hack
    s = s.replace(' oo ', ' infinity ')
    return s
    
'''
Recursive conversion function.
User should call convert_sympy_ssml instead.
'''
def _convert(expr, funcs_tree, mode, quantity_index, is_initial):
    func_id = expr.__class__.__name__
    r = funcs_tree.getroot()
    func = r.find(func_id)
    
    s = str()
    
    if func is None:
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
                    s += _convert(expr.args[i], funcs_tree, mode, quantity_index, is_initial)
                elif len(expr.args[i].args) == 1 or mode == QuantityModes.NO_INDICATOR:
                    s += ' ' + _convert(expr.args[i], funcs_tree, mode, quantity_index, is_initial) + ' '
                elif is_initial:
                    s += ' ' + _convert(expr.args[i], funcs_tree, mode, quantity_index, is_initial) + ' '
                    is_initial = false
                else:
                    n_str = ''
                    if mode == QuantityModes.PARENTHESES or mode == QuantityModes.PARENTHESES_NUMBERED:
                        q_str = parentheses_str
                    if mode == QuantityModes.QUANTITY or mode == QuantityModes.QUANTITY_NUMBERED:
                        q_str = quantity_str
                    if mode == QuantityModes.QUANTITY_NUMBERED or mode == QuantityModes.PARENTHESES_NUMBERED:
                        n_str = ordinal_str(quantity_index)

                    s += ' ' + begin_str + ' ' + n_str + ' ' + q_str + \
                    _convert(expr.args[i], funcs_tree, mode, quantity_index + 1, is_initial) + \
                    end_str + ' ' + n_str + ' ' + q_str + ' ' 
                
                i_sub = 0
                i += 1
                j += 1
            
            elif func[j].tag == 'subarg':
                s += _convert(expr.args[i].args[i_sub], funcs_tree, mode, quantity_index, is_initial)
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

            elif func[j].tag == 'end':
                i = len(expr.args)

    return s