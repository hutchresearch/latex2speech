import re

import TexSoup

from tex_soup_utils import safe_replace_child, get_effective_children, expr_test, seperate_contents

class Macro:
    def _arg_to_string(self, arg):
        '''
        Helper function for getting the string representing an arg's contents
        '''
        string = ''
        for val in arg.all:
            string += str(val)
        return string

    def _normalize(self, search_target, prev_macros: dict, expr_type):
        '''
        Normalizes the macro so it is defined only in terms of itself
        '''
        children = get_effective_children(search_target)
        for i, child in enumerate(children):
            self._normalize(child, prev_macros, expr_type)
            if expr_test(child, expr_type):
                try:
                    macro = prev_macros[child.name]
                    search_target.insert(i, macro.expand_macro(child))
                    search_target.remove(child)
                except KeyError:
                    pass

    def _expand_macro_defn(self, defn: str, default_arg: str, args: int, macro):
        '''
        Function for generic macro expansion as the rules are shared between different types of macros
        '''
        expansion = defn
        ref_arg = 0
        targ_arg = 1
        if default_arg:
            expansion = expansion.partition('#1')
            if len(macro.args) > 0 and isinstance(macro.args[0], TexSoup.data.BracketGroup):
                expansion = expansion[0] + self._arg_to_string(macro.args[ref_arg]) + expansion[2]
                ref_arg += 1
            else:
                expansion = expansion[0] + default_arg + expansion[2]
            targ_arg += 1
        for arg in range(targ_arg, args + 1):
            expansion = expansion.partition('#' + str(arg))
            if ref_arg < len(macro.args):
                expansion = expansion[0] + self._arg_to_string(macro.args[ref_arg]) + expansion[2]
                ref_arg += 1
            # Covers both the case that the arg isn't found or it was and needs to be replaced
            else:
                expansion = expansion[0] + expansion[2]
        return expansion

    def expand_macro(self, macro):
        '''External functionality all macro's provide'''
        pass

class CmdMacro(Macro):
    '''
    Represents a macro defined by either newcommand or renewcommand.
    Depends on create_macro_bindings for proper constructor initialization.
    '''
    def __init__(self, macro_defn, cmd_macros: dict, env_macros: dict):
        self.name = macro_defn.args[0].contents[0].name
        if self.name in cmd_macros:
            cmd_macros.pop(self.name)
        
        self._normalize(macro_defn, cmd_macros, TexSoup.data.TexCmd)
        self._normalize(macro_defn, env_macros, TexSoup.data.TexEnv)
        
        self.args = 0
        self.default = None
        if isinstance(macro_defn.args[1], TexSoup.data.BracketGroup):
            self.args = int(macro_defn.args[1].contents[0])
            if isinstance(macro_defn.args[2], TexSoup.data.BracketGroup):
                self.default = self._arg_to_string(macro_defn.args[2])
        self.defn = self._arg_to_string(macro_defn.args[-1])
        self.position = macro_defn.position

    def expand_macro(self, macro):
        expansion = None
        if self.name == macro.name and expr_test(macro, TexSoup.data.TexCmd):
            expansion = self._expand_macro_defn(self.defn, self.default, self.args, macro)
        return expansion

class EnvMacro(Macro):
    '''
    Represents a macro defined by either newenvironment or renewenvironment.
    Depends on create_macro_bindings for proper constructor initialization.
    '''
    def __init__(self, macro_defn, cmd_macros: dict, env_macros: dict):
        self.name = macro_defn.args[0].contents[0]
        if self.name in env_macros:
            env_macros.pop(self.name)
        
        self._normalize(macro_defn, cmd_macros, TexSoup.data.TexCmd)
        self._normalize(macro_defn, env_macros, TexSoup.data.TexEnv)
        
        self.args = 0
        self.default = None
        if isinstance(macro_defn.args[1], TexSoup.data.BracketGroup):
            self.args = int(macro_defn.args[1].contents[0])
            if isinstance(macro_defn.args[2], TexSoup.data.BracketGroup):
                self.default = self._arg_to_string(macro_defn.args[2])
        self.beg_defn = self._arg_to_string(macro_defn.args[-2])
        self.end_defn = self._arg_to_string(macro_defn.args[-1])
        self.position = macro_defn.position

    def expand_macro(self, macro):
        expansion = None
        if self.name == macro.name and expr_test(macro, TexSoup.data.TexEnv):
            expansion = self._expand_macro_defn(self.beg_defn, self.default, self.args, macro)
            _, contents = seperate_contents(macro)
            for child in contents:
                expansion += str(child)
            expansion += self._expand_macro_defn(self.end_defn, self.default, self.args, macro)
        return expansion


def normalize_doc_macros(text: str):
    if not isinstance(text, str):
        text = str(text)
    def def_to_newcommand(match):
        out = r'\newcommand{' + match.group('name') + r'}'
        if match.group('args'):
            max_arg = 1
            for c in match.group('args'):
                try:
                    arg = int(c)
                    if arg > max_arg:
                        max_arg = arg
                except ValueError:
                    pass
            out += r'[{}]'.format(max_arg)
        out += match.group('repl')
        print()
        print(out)
        return out


    text = re.sub(
        r'\\def[\s]*(?P<name>\\[a-zA-Z]+)[\s]*(?P<args>(\[?#[0-9]\]?)*)[\s]*(?P<repl>\{.*\})',
        def_to_newcommand,
        text
    )
    return TexSoup.TexSoup(text)

def expand_doc_macros(doc):
    '''
    Returns a TexSoup node representing doc with all macros defined with newcommand, 
    renewcommand, newenvironment and renewenvironment expanded out accross the entire
    document. The nested functions are there for organizational purposes and to 
    reduce the number of arguments needed in each function.
    '''
    doc = normalize_doc_macros(doc)

    def create_macro_bindings():
        '''
        Create all the macro objects for the document and store them in their
        respective binding lists. Required initialization for later expansion.
        '''
        defnBindings = {}
        for macro_defn in doc.find_all('newcommand'):
            defnBindings[macro_defn.position] = macro_defn
        for macro_defn in doc.find_all('renewcommand'):
            defnBindings[macro_defn.position] = macro_defn
        for macro_defn in doc.find_all('newenvironment'):
            defnBindings[macro_defn.position] = macro_defn
        for macro_defn in doc.find_all('renewenvironment'):
            defnBindings[macro_defn.position] = macro_defn

        bindingOrder = list(defnBindings.keys())
        bindingOrder.sort()

        nonlocal cmdBindings
        nonlocal envBindings
        activeCmdBindings = {}
        activeEnvBindings = {}
        for pos in bindingOrder:
            defn = defnBindings[pos]
            if expr_test(defn, TexSoup.data.TexCmd) and \
                (defn.name == 'newcommand' or defn.name == 'renewcommand'):
                macro = CmdMacro(defn, activeCmdBindings, activeEnvBindings)
                activeCmdBindings[macro.name] = macro
                if macro.name in cmdBindings:
                    cmdBindings[macro.name].append(macro)
                else:
                    cmdBindings[macro.name] = [macro]
            elif expr_test(defn, TexSoup.data.TexCmd) and \
                (defn.name == 'newenvironment' or defn.name == 'renewenvironment'):
                macro = EnvMacro(defn, activeCmdBindings, activeEnvBindings)
                activeEnvBindings[macro.name] = macro
                if macro.name in envBindings:
                    envBindings[macro.name].append(macro)
                else:
                    envBindings[macro.name] = [macro]

    def expand_doc_macros_sub(node): 
        '''
        Recursively expands all the macro instances in a given TexNode [sic?].
        This function relies on the fact that an edited TexSoup parse tree
        never updates the position attribute even if modified, meaning the 
        saved position of a macro's definition can be used to determine 
        the current active binding.
        '''
        nonlocal cmdBindings
        nonlocal envBindings
        if node.name != 'newcommand' and node.name != 'renewcommand' and \
            node.name != 'newenvironment' and node.name != 'renewenvironment':
            children = get_effective_children(node)
            for i, child in enumerate(children):
                expand_doc_macros_sub(child)
                bindingList = None
                try:
                    if expr_test(child, TexSoup.data.TexCmd):
                        bindingList = cmdBindings[child.name]
                    elif expr_test(child, TexSoup.data.TexEnv):
                        bindingList = envBindings[child.name]
                except KeyError:
                    pass

                if bindingList:
                    binding = -1
                    while binding+1 < len(bindingList) and bindingList[binding+1].position < child.position:
                        binding += 1
                    if binding >= 0:
                        safe_replace_child(node, child, i, bindingList[binding].expand_macro(child))

    cmdBindings = {}
    envBindings = {}
    create_macro_bindings()
    expand_doc_macros_sub(doc)
    return TexSoup.TexSoup(str(doc))