import TexSoup
from tex_soup_utils import safeReplaceChild, getEffectiveChildren, exprTest, seperateContents

class Macro:
    '''Helper function for getting the string representing an arg's contents'''
    def _argToString(self, arg):
        string = ''
        for val in arg.all:
            string += str(val)
        return string

    '''Normalizes the macro so it is defined only in terms of itself'''
    def _normalize(self, searchTarget, prevMacros: dict, exprType):
        children = getEffectiveChildren(searchTarget)
        for i, child in enumerate(children):
            self._normalize(child, prevMacros, exprType)
            if exprTest(child, exprType):
                try:
                    macro = prevMacros[child.name]
                    searchTarget.insert(i, macro.expandMacro(child))
                    searchTarget.remove(child)
                except KeyError:
                    pass

    '''Function for generic macro expansion as the rules are shared between different types of macros'''
    def _expandMacroDefn(self, defn: str, defaultArg: str, args: int, macro):
        expansion = defn
        refArg = 0
        targArg = 1
        if defaultArg:
            expansion = expansion.partition('#1')
            if len(macro.args) > 0 and isinstance(macro.args[0], TexSoup.data.BracketGroup):
                expansion = expansion[0] + self._argToString(macro.args[refArg]) + expansion[2]
                refArg += 1
            else:
                expansion = expansion[0] + defaultArg + expansion[2]
            targArg += 1
        for arg in range(targArg, args + 1):
            expansion = expansion.partition('#' + str(arg))
            if refArg < len(macro.args):
                expansion = expansion[0] + self._argToString(macro.args[refArg]) + expansion[2]
                refArg += 1
            # Covers both the case that the arg isn't found or it was and needs to be replaced
            else:
                expansion = expansion[0] + expansion[2]
        return expansion

    '''External functionality all macro's provide'''
    def expandMacro(self, macro):
        pass

'''
Represents a macro defined by either newcommand or renewcommand.
    Depends on createMacroBindings for proper constructor initialization.
'''
class CmdMacro(Macro):
    def __init__(self, macroDefn, cmdMacros: dict, envMacros: dict):
        self.name = macroDefn.args[0].contents[0].name
        if self.name in cmdMacros:
            cmdMacros.pop(self.name)
        
        self._normalize(macroDefn, cmdMacros, TexSoup.data.TexCmd)
        self._normalize(macroDefn, envMacros, TexSoup.data.TexEnv)
        
        self.args = 0
        self.default = None
        if isinstance(macroDefn.args[1], TexSoup.data.BracketGroup):
            self.args = int(macroDefn.args[1].contents[0])
            if isinstance(macroDefn.args[2], TexSoup.data.BracketGroup):
                self.default = self._argToString(macroDefn.args[2])
        self.defn = self._argToString(macroDefn.args[-1])
        self.position = macroDefn.position

    def expandMacro(self, macro):
        expansion = None
        if self.name == macro.name and exprTest(macro, TexSoup.data.TexCmd):
            expansion = self._expandMacroDefn(self.defn, self.default, self.args, macro)
        return expansion

'''
Represents a macro defined by either newenvironment or renewenvironment.
    Depends on createMacroBindings for proper constructor initialization.
'''
class EnvMacro(Macro):
    def __init__(self, macroDefn, cmdMacros: dict, envMacros: dict):
        self.name = macroDefn.args[0].contents[0]
        if self.name in envMacros:
            envMacros.pop(self.name)
        
        self._normalize(macroDefn, cmdMacros, TexSoup.data.TexCmd)
        self._normalize(macroDefn, envMacros, TexSoup.data.TexEnv)
        
        self.args = 0
        self.default = None
        if isinstance(macroDefn.args[1], TexSoup.data.BracketGroup):
            self.args = int(macroDefn.args[1].contents[0])
            if isinstance(macroDefn.args[2], TexSoup.data.BracketGroup):
                self.default = self._argToString(macroDefn.args[2])
        self.begDefn = self._argToString(macroDefn.args[-2])
        self.endDefn = self._argToString(macroDefn.args[-1])
        self.position = macroDefn.position

    def expandMacro(self, macro):
        expansion = None
        if self.name == macro.name and exprTest(macro, TexSoup.data.TexEnv):
            expansion = self._expandMacroDefn(self.begDefn, self.default, self.args, macro)
            _, contents = seperateContents(macro)
            for child in contents:
                expansion += str(child)
            expansion += self._expandMacroDefn(self.endDefn, self.default, self.args, macro)
        return expansion



'''
Returns a TexSoup node representing doc with all macros defined with newcommand, 
  renewcommand, newenvironment and renewenvironment expanded out accross the entire
  document. The nested functions are there for organizational purposes and to 
  reduce the number of arguments needed in each function.
'''
def expandDocMacros(doc):    
    '''
    Create all the macro objects for the document and store them in their
        respective binding lists. Required initialization for later expansion.
    '''
    def createMacroBindings():
        defnBindings = {}
        for macroDefn in doc.find_all('newcommand'):
            defnBindings[macroDefn.position] = macroDefn
        for macroDefn in doc.find_all('renewcommand'):
            defnBindings[macroDefn.position] = macroDefn
        for macroDefn in doc.find_all('newenvironment'):
            defnBindings[macroDefn.position] = macroDefn
        for macroDefn in doc.find_all('renewenvironment'):
            defnBindings[macroDefn.position] = macroDefn

        bindingOrder = list(defnBindings.keys())
        bindingOrder.sort()

        nonlocal cmdBindings
        nonlocal envBindings
        activeCmdBindings = {}
        activeEnvBindings = {}
        for pos in bindingOrder:
            defn = defnBindings[pos]
            if exprTest(defn, TexSoup.data.TexCmd) and \
                (defn.name == 'newcommand' or defn.name == 'renewcommand'):
                macro = CmdMacro(defn, activeCmdBindings, activeEnvBindings)
                activeCmdBindings[macro.name] = macro
                if macro.name in cmdBindings:
                    cmdBindings[macro.name].append(macro)
                else:
                    cmdBindings[macro.name] = [macro]
            elif exprTest(defn, TexSoup.data.TexCmd) and \
                (defn.name == 'newenvironment' or defn.name == 'renewenvironment'):
                macro = EnvMacro(defn, activeCmdBindings, activeEnvBindings)
                activeEnvBindings[macro.name] = macro
                if macro.name in envBindings:
                    envBindings[macro.name].append(macro)
                else:
                    envBindings[macro.name] = [macro]

    '''
    Recursively expands all the macro instances in a given TexNode [sic?].
        This function relies on the fact that an edited TexSoup parse tree
        never updates the position attribute even if modified, meaning the 
        saved position of a macro's definition can be used to determine 
        the current active binding.
    '''
    def expandDocMacrosSub(node):
        nonlocal cmdBindings
        nonlocal envBindings
        if node.name != 'newcommand' and node.name != 'renewcommand' and \
            node.name != 'newenvironment' and node.name != 'renewenvironment':
            children = getEffectiveChildren(node)
            for i, child in enumerate(children):
                expandDocMacrosSub(child)
                bindingList = None
                try:
                    if exprTest(child, TexSoup.data.TexCmd):
                        bindingList = cmdBindings[child.name]
                    elif exprTest(child, TexSoup.data.TexEnv):
                        bindingList = envBindings[child.name]
                except KeyError:
                    pass

                if bindingList:
                    binding = -1
                    while binding+1 < len(bindingList) and bindingList[binding+1].position < child.position:
                        binding += 1
                    if binding >= 0:
                        safeReplaceChild(node, child, i, bindingList[binding].expandMacro(child))

    cmdBindings = {}
    envBindings = {}
    createMacroBindings()
    expandDocMacrosSub(doc)
    return TexSoup.TexSoup(str(doc))