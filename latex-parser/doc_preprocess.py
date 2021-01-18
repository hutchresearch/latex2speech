import TexSoup
import os

'''
Expand newcommand and renewcommand
Expand labels/refs
Expand citations
'''

'''
Returns a TexSoup node representing doc with all macros defined with newcommand 
  and renewcommand expanded. Handles recursive definitions and all that jazz. 
  doc itself is modified as a side effect and so should not be used after invocation
  of this function.
'''
def expandDocMacros(doc):
    # class Macro:
    #     def __init__(self, macroDefn, prevMacros):
    #         if macroDefn.name == 'newcommand' or macroDefn.name == 'renewcommand':
    #             self.name = macroDefn.args[0].contents[0].name
    #             if self.name in prevMacros:
    #                 prevMacros.pop(self.name)
                
    #             if len(prevMacros) > 0:
    #                 self._normalize(macroDefn, prevMacros.values())
                
    #             self.args = 0
    #             self.default = None
    #             if isinstance(macroDefn.args[1], TexSoup.data.BracketGroup):
    #                 self.args = int(macroDefn.args[1].contents[0])
    #                 if isinstance(macroDefn.args[2], TexSoup.data.BracketGroup):
    #                     self.default = self._argToString(macroDefn.args[2])
    #             self.defn = self._argToString(macroDefn.args[-1])
    #             self.position = macroDefn.position

    #     def _argToString(self, arg):
    #         string = ''
    #         for val in arg.all:
    #             string += str(val)
    #         return string

    #     '''Normalizes the macro so it is defined only in terms of itself'''
    #     def _normalize(self, searchTarget, prevMacros):
    #         excl = []
    #         for arg in searchTarget.args:
    #             self._normalize(arg, prevMacros)
    #             excl.extend(arg.children)
    #         for i, child in enumerate(searchTarget.children):
    #             if child not in excl:
    #                 if isinstance(child, TexSoup.data.TexEnv):
    #                     self._normalize(child, prevMacros)
    #                 else:
    #                     for macro in prevMacros:
    #                         if child.name == macro.name:
    #                             self._normalize(child, prevMacros)
    #                             searchTarget.insert(i, macro.expandMacro(child))
    #                             searchTarget.remove(child)

    #     '''Returns a string representing the expansion of an invocation of this macro'''
    #     def expandMacro(self, macro):
    #         expansion = self.defn
    #         if self.name == macro.name:
    #             refArg = 0
    #             targArg = 1
    #             if self.default:
    #                 expansion = expansion.partition('#1')
    #                 if len(macro.args) > 0 and isinstance(macro.args[0], TexSoup.data.BracketGroup):
    #                     expansion = expansion[0] + self._argToString(macro.args[refArg]) + expansion[2]
    #                     refArg += 1
    #                 else:
    #                     expansion = expansion[0] + self.default + expansion[2]
    #                 targArg += 1
    #             for arg in range(targArg, self.args + 1):
    #                 expansion = expansion.partition('#' + str(arg))
    #                 if refArg < len(macro.args):
    #                     expansion = expansion[0] + self._argToString(macro.args[refArg]) + expansion[2]
    #                     refArg += 1
    #                 # Covers both the case that the arg isn't found or it was and needs to be replaced
    #                 else:
    #                     expansion = expansion[0] + expansion[2]
    #         return expansion

    # def createMacroBindings():
    #     defnBindings = {}
    #     for macroDefn in doc.find_all('newcommand'):
    #         defnBindings[macroDefn.args[0].position] = macroDefn
    #     for macroDefn in doc.find_all('renewcommand'):
    #         defnBindings[macroDefn.args[0].position] = macroDefn

    #     bindingOrder = list(defnBindings.keys())
    #     bindingOrder.sort()

    #     # Expand the bindings relative to one another
    #     nonlocal macroBindings
    #     activeBindings = {}
    #     for pos in bindingOrder:
    #         macro = Macro(defnBindings[pos], activeBindings)
    #         activeBindings[macro.name] = macro
    #         if macro.name in macroBindings:
    #             macroBindings[macro.name].append(macro)
    #         else:
    #             macroBindings[macro.name] = [macro]

    # def expandDocMacrosSub(node):
    #     nonlocal macroBindings
    #     excl = []
    #     for arg in node.args:
    #         expandDocMacrosSub(arg)
    #         excl.extend(arg.children)
    #     for i, child in enumerate(node.children):
    #         if child not in excl:
    #             if isinstance(child, TexSoup.data.TexEnv):
    #                 expandDocMacrosSub(child)
    #             else:
    #                 for name in macroBindings.keys():
    #                     if child.name == name:
    #                         macro = -1
    #                         # child.position is valid since the position field of TexNode's remain unchanged even if the doc is modified
    #                         while macro+1 < len(macroBindings[name]) and macroBindings[name][macro+1].position < child.position:
    #                             macro += 1
    #                         if macro >= 0:
    #                             # It makes me so unbelievably sad that this code is necessary, but no matter what I do, deleting a specific
    #                             #   child instead deletes the first instance of a node with the same name as the child. To fix this, all
    #                             #   children before the desired node to be deleted must be given temporary, unique names and changed back
    #                             #   afterwards.
    #                             node.insert(i, macroBindings[name][macro].expandMacro(child))
    #                             tempNameSuffix = 'a'
    #                             tempNames = []
    #                             for deleteCand in node.find_all(name):
    #                                 if deleteCand.position == child.position:
    #                                     child.delete()
    #                                     for tempName in tempNames:
    #                                         node.find(tempName).name = name
    #                                     break
    #                                 elif deleteCand.position < child.position:
    #                                     tempName = name + tempNameSuffix
    #                                     while node.find(tempName):
    #                                         tempNameSuffix += 'a'
    #                                         tempName = name + tempNameSuffix
    #                                     deleteCand.name = tempName
    #                                     tempNames.append(tempName)
    #                                 else:
    #                                     print('Expected node not found, moving on')
    #                                     break

    # Function that will travers aux file for \newlabel
    # Create a hashtable to store in these values
    #   Input: .aux file to corresponding .tex file
    #   Output: Hashtable for \newlabel
    def auxFileHashTable(auxFile):
        hash = {}
        for line in auxFile:
            if (line[0:9] == "\\newlabel"):
                hashObject = {}
                count = 1
                name = ""

                # Grabbing key name of hashtable
                for char in line[10:]:
                    count += 1
                    if (char != "}"):
                        name += char
                    else:
                        count += 10
                        break;

                obj = 1
                page = ""
                section = ""
                caption = ""
                labelType = ""

                # Adding .aux information to corresponding
                # object type
                for char in line[count:]:
                    if (char == '{') {
                        obj += 1
                    } else if (char == '}') {
                    } else if (obj == 1) {
                        page += char
                    } else if (obj == 2) {
                        section += char
                    } else if (obj == 3) {
                        caption = += char
                    } else if (obj == 4) {
                        labelType += char
                    }

                # Adding object information to hash array object 
                hashObject.append(page)
                hashObject.append(section)
                hashObject.append(caption)
                hashObject.append(labelType)

                # Adding to hashtable
                hash[name] = hashObject

    def expandDocNewLabels(doc):
        # TODO
        # Get appropriate .aux file to corresponding document
        split_string = doc.name.split(".tex", 1)
        docName = split_string[0] + ".aux"

        # 1. Open .aux file (Assuming it's been generated)
        # 2. Traverse .aux file, create hashtable for commands -> vallues
        auxFile = open(docName, "r")
        myHash = auxFileHashTable(auxFile)
        # 3. Traverse doc file, replacing them, by looking into hashtable
        # 4. Delete .pdf, .out, .log, and .aux file

    expandDocNewLabels(doc)
    # macroBindings = {}
    # createMacroBindings()
    # expandDocMacrosSub(doc)
    # return TexSoup.TexSoup(str(doc))

file = open("sample.tex", "r")
expandDocMacros(file)