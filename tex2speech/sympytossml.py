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


begin_str = '<prosody pitch=\"+25%\"><break time=\"0.3ms\"/>begin'
end_str = '<prosody pitch=\"+25%\"><break time=\"0.3ms\"/>end'
quantity_str = 'quantity</prosody><break time=\"0.3ms\"/>'
parentheses_str = 'parentheses</prosody><break time=\"0.3ms\"/>'

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
    '''
    Convert SymPy object expr to english words.
    Mode defines how quantities should be denoted.
    '''
    funcs_tree = ET.parse(sympy_funcs_file)
    s = _convert(expr, funcs_tree, mode, 1)
    s = remove_extra_spaces(s)
    return s
    
def _convert(expr, funcs_tree, mode, quantity_index):
    '''
    Recursive conversion function.
    User should call convert_sympy_ssml instead.
    '''
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
                    s += _convert(expr.args[i], funcs_tree, mode, quantity_index + 1)
                    # s += ' ' + str(expr.args[i]) + ' '
                elif len(expr.args[i].args) == 1:
                    s += ' ' + _convert(expr.args[i], funcs_tree, mode, quantity_index + 1) + ' '
                else:
                    n_str = ''
                    if mode == Quantity_Modes.PARENTHESES or mode == Quantity_Modes.PARENTHESES_NUMBERED:
                        q_str = parentheses_str
                    if mode == Quantity_Modes.QUANTITY or mode == Quantity_Modes.QUANTITY_NUMBERED:
                        q_str = quantity_str
                    if mode == Quantity_Modes.QUANTITY_NUMBERED or mode == Quantity_Modes.PARENTHESES_NUMBERED:
                        n_str = ordinal_str(quantity_index)

                    s += ' ' + begin_str + ' ' + n_str + ' ' + q_str + \
                    _convert(expr.args[i], funcs_tree, mode, quantity_index + 1) + \
                    end_str + ' ' + n_str + ' ' + q_str + ' ' 
                
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

            elif func[j].tag == 'end':
                i = len(expr.args)

    return s
                 
