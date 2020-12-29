import TexSoup

'''
Expand newcommand and renewcommand
Expand labels/refs
Expand citations
'''

'''
'''
def expandDocMacros(doc):
    def argToString(arg):
        string = ''
        for val in arg.all:
            string += str(val)
        return string

    class Macro:
        def __init__(self, macroDefn):
            if macroDefn.name == 'newcommand' or macroDefn.name == 'renewcommand':
                self.name = macroDefn.args[0].contents[0].name
                self.args = 0
                self.default = None
                if isinstance(macroDefn.args[1], TexSoup.data.BracketGroup):
                    self.args = int(macroDefn.args[1].contents[0])
                    if isinstance(macroDefn.args[2], TexSoup.data.BracketGroup):
                        self.default = argToString(macroDefn.args[2])
                self.defn = argToString(macroDefn.args[-1])

        def expandMacro(self, macro):
            expansion = self.defn
            if self.name == macro.name:
                refArg = 0
                targArg = 1
                if self.default:
                    targArg += 1
                    expansion = expansion.partition('#1')
                    if len(macro.args) > 0 and isinstance(macro.args[0], TexSoup.data.BracketGroup):
                        refArg += 1
                        expansion = expansion[0] + argToString(macro.args[0]) + expansion[2]
                    else:
                        expansion = expansion[0] + self.default + expansion[2]
                for arg in range(targArg, self.args + 1):
                    expansion = expansion.partition('#' + str(arg))
                    if refArg < len(macro.args):
                        expansion = expansion[0] + argToString(macro.args[refArg]) + expansion[2]
                        refArg += 1
                    # Covers both the case that the arg isn't found or it was and needs to be replaced
                    else:
                        expansion = expansion[0] + expansion[2]
            return expansion
    
    obj = Macro(doc.newcommand)
    print(obj.expandMacro(doc.a))

expandDocMacros(TexSoup.TexSoup(r'\newcommand{\a}[2][d]{\b #1 #2}\a{c}'))
    # bindings = {}
    # positions = {}
    # for macro in doc.find_all('newcommand'):
    #     bindings[macro.args[0].name] = [macro]
    #     positions[macro.position] = macro
    # for macro in doc.find_all('renewcommand'):
    #     if bindings[macro.args[0].name]:
    #         bindings[macro.args[0].name].append(macro)
    #     else:
    #         bindings[macro.args[0].name] = [macro]
    #     positions[macro.position] = macro

    # # Expand the bindings relative to one another
    # bindingOrder = list(positions.keys())
    # bindingOrder.sort()
    # with [] as activeBindings:
    #     for pos in bindingOrder:
            

    # # Expand bindings within the text
    # for name in bindings.keys():
    #     activeBinding = -1
    #     for macro in doc.find_all(name):
    #         while activeBinding + 1 < len(bindings[name]) and bindings[name][activeBinding + 1].position < macro.position:
    #             activeBinding += 1 
