import TexSoup
import sympy
import xml.etree.ElementTree as ET

from conversion_db import ConversionDB
from SSMLParsing.arg_element import ArgElement
from SSMLParsing.break_element import BreakElement
from SSMLParsing.content_element import ContentElement
from SSMLParsing.emphasis_element import EmphasisElement
from SSMLParsing.prosody_element import ProsodyElement
from SSMLParsing.root_element import RootElement
from SSMLParsing.ssml_element_node import SSMLElementNode
from SSMLParsing.ssml_element import SSMLElement
from SSMLParsing.text_element import TextElement

from sympytossml import convert_sympy_ssml, QuantityModes
from tex_soup_utils import exprTest, seperateContents
from tex_to_sympy import run_sympy

'''
Main parsing class. Parses TexSoup parse trees into SSMLElementNode
    trees for future output. The conversion rules for every command 
    and environment found in the tree is determined by the database
    the class is initialized with.
'''
class ConversionParser:
    def __init__(self, db: ConversionDB):
        self.db = db
        self.env_stack = []

    '''Function that will take in new table contents, and parse
    each column'''
    def _parseTableContents(self, contents_node, elem_list_parent, left_child=None):
        split = str(contents_node).split("\n")
        # Go through each row
        for row in split:
            if left_child:
                left_child.appendTailText("New Row: ")
            else:
                elem_list_parent.appendHeadText("New Row: ")

            inner_split = row.split('&')
            column = 1

            # Go through each value in the row
            for word in inner_split: 
                if word != "&":
                    text = ", Column " + str(column) + ", Value: " + word;

                    if left_child:
                        left_child.appendTailText(text)
                    else:
                        elem_list_parent.appendHeadText(text)

                    column += 1

    '''This function strips out unnecessary environments from table node
        TexSoup doesn't delete \begin{tabular} or \end{tabular} tags
        so this is what this function will do before passing contents
        to parseTableContents function
    '''
    def _parseTableNode(self, contents):
        table_contents = str(contents).replace('\hline', '')
        table_contents = table_contents[table_contents.find('\n'):]
        table_contents = table_contents.lstrip()
        table_contents = table_contents.split("\end{tabular}", 1)[0]
        table_contents = table_contents.rstrip()
        return table_contents

    '''
    Retrieves the correct argument node's list of arguments with respect to 
        the format of the ArgElement class.
    '''
    def _getArg(self, node, arg_elem):
        target_type = TexSoup.data.BraceGroup
        if arg_elem.getArgType() == 'bracket':
            target_type = TexSoup.data.BracketGroup
        
        i = -1
        num = 0
        arg = None
        while num < arg_elem.getArgNum() and i+1 < len(node.args):
            i += 1
            if isinstance(node.args[i], target_type):
                num += 1

        if num == arg_elem.getArgNum():
            arg = node.args[i]

        return arg

    def _envContentsToString(self, env):
        string = ''
        for val in env.all:
            string += str(val)
        return string

    '''
    Recursively resolves non-node SSMLElements within elem_list with respect to 
        env_node. Also manages the env_stack.
    '''
    def _resolveEnvironmentElements(self, env_node, elem_list_parent, elem_list, left_child):
        if len(elem_list) > 0:
            offset = 0
            i = 0
            for k in range(len(elem_list)):
                if not isinstance(elem_list[i], SSMLElementNode):
                    elem = elem_list.pop(i)
                    next_offset = -1
                    new_ind = i
                    parse_target = None
                    if isinstance(elem, ArgElement):
                        arg = self._getArg(env_node, elem)
                        if arg:
                            parse_target = arg.contents
                    elif isinstance(elem, ContentElement):
                        _, parse_target = seperateContents(env_node)
                    elif isinstance(elem, TextElement):
                        text = elem.getHeadText()
                        if left_child:
                            left_child.appendTailText(text)
                        else:
                            elem_list_parent.appendHeadText(text)
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                        
                    # TODO: Should args within an environment's arguments reference the environment
                    # If not, stack operations should only occur in ContentElement
                    if parse_target:
                        definition = self.db.getEnvDefinition(env_node.name)

                        if definition:
                            if 'mathmode' in definition and definition['mathmode'] == True:
                                output = run_sympy(self._envContentsToString(env_node))
                                print("MATHMODE OUTPUT: " + output)
                                if left_child:
                                    left_child.appendTailText(str(output))
                                else:
                                    elem_list_parent.appendHeadText(str(output))
                            elif 'readTable' in definition and definition['readTable'] == True:
                                self._parseTableContents(self._parseTableNode(env_node), elem_list_parent, left_child)
                            else:
                                self.env_stack.append(definition)
                                new_ind = self._parseNodes(parse_target, elem_list_parent, ssml_children=elem_list, insert_index=i, left_child=left_child)
                                self.env_stack.pop()
                        else:
                            new_ind = self._parseNodes(parse_target, elem_list_parent, ssml_children=elem_list, insert_index=i, left_child=left_child)
                    
                    next_offset += new_ind - i
                    offset += next_offset
                else:
                    self._resolveEnvironmentElements(env_node, elem_list[i], elem_list[i].children, None)

                i = (k + 1) + offset
                if i > 0:
                    left_child = elem_list[i-1]

    '''
    Handles environment parsing, returning the result of its parsing or 
        or none of no appropriate definition is found.
    '''
    def _parseEnvironment(self, env_node, ssml_parent, left_child):
        args, contents = seperateContents(env_node)

        elem_list = self.db.getEnvConversion(env_node.name)
        if not elem_list:
            self._parseNodes(contents, ssml_parent, left_child=left_child)
        else:
            self._resolveEnvironmentElements(env_node, ssml_parent, elem_list, left_child)

        return elem_list

    '''
    Recursively resolves non-node SSMLElements within elem_list with respect to 
        env_node.
    '''
    def _resolveCmdElements(self, cmd_node, elem_list_parent, elem_list, left_child):
        if len(elem_list) > 0:
            offset = 0
            i = 0
            for k in range(len(elem_list)):
                if not isinstance(elem_list[i], SSMLElementNode):
                    elem = elem_list.pop(i)
                    next_offset = -1
                    new_ind = i
                    if isinstance(elem, ArgElement):
                        arg = self._getArg(cmd_node, elem)
                        if arg:
                            parse_target = arg.contents
                            new_ind = self._parseNodes(arg.contents, elem_list_parent, ssml_children=elem_list, insert_index=i, left_child=left_child)
                    elif isinstance(elem, TextElement):
                        text = elem.getHeadText()
                        if left_child:
                            left_child.appendTailText(text)
                        else:
                            elem_list_parent.appendHeadText(text)
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")

                    next_offset += new_ind - i
                    offset += next_offset
                else:
                    self._resolveCmdElements(cmd_node, elem_list[i], elem_list[i].children, None)
                
                i = (k + 1) + offset
                if i > 0:
                    left_child = elem_list[i-1]

    '''
    Handles command parsing, returning the result of its parsing or 
        or none of no appropriate definition is found.
    '''
    def _parseCommand(self, cmd_node, ssml_parent, left_child):
        args, _ = seperateContents(cmd_node)
        
        elem_list = None
        if len(self.env_stack) > 0 and cmd_node.name in self.env_stack[-1]:
            elem_list = self.env_stack[-1][cmd_node.name]
        else:
            elem_list = self.db.getCmdConversion(cmd_node.name)
        
        if elem_list:
            self._resolveCmdElements(cmd_node, ssml_parent, elem_list, left_child)

        return elem_list

    '''
    Main entry point to all parsing. Parses wih respect to a list of TexSoup
        nodes, a parent SSMLElementNode and its children. The children don't 
        necessarily correspond to the parent's actual list of children in 
        order to facilitate processing seperate lists of nodes.
    '''
    def _parseNodes(self, tex_nodes: list, ssml_parent: SSMLElementNode, ssml_children=None, insert_index=0, left_child=None):
        if ssml_children is None:
            ssml_children = ssml_parent.children
        for texNode in tex_nodes:
            parseOut = None
            if insert_index > 0:
                left_child = ssml_children[insert_index-1]

            if exprTest(texNode, TexSoup.data.TexEnv):
                parseOut = self._parseEnvironment(texNode, ssml_parent, left_child)
            elif exprTest(texNode, TexSoup.data.TexCmd):
                parseOut = self._parseCommand(texNode, ssml_parent, left_child)
            elif exprTest(texNode, TexSoup.data.Token):
                text = str(texNode)

                if left_child:
                    left_child.appendTailText(text)
                else:
                    ssml_parent.appendHeadText(text)

            if parseOut:
                for ssmlChild in parseOut:
                    ssml_children.insert(insert_index, ssmlChild)
                    insert_index += 1

            if insert_index > 0:
                left_child = ssml_children[insert_index-1]

        return insert_index

    def _printTreeSub(self, tree, level, level_arr, at_index, parent_index):
        if len(level_arr) == level:
            level_arr.append([])
        level_arr[level].append(str(parent_index) + ' -> ' + str(tree))
        for i, child in enumerate(tree.children):
            self._printTreeSub(child, level+1, level_arr, i, at_index)

    '''
    Basic print method to see whats happening within the tree
    '''
    def printTree(self, tree):
        level_arr = []
        self._printTreeSub(tree, 0, level_arr, 0, -1)
        for level in level_arr:
            print(level)

    '''
    Parse doc with respect to the database the parser was initialized with.
    '''
    def parse(self, doc: TexSoup.data.TexNode, test=False):
        tree = RootElement()
        if isinstance(doc, str):
            doc = TexSoup.TexSoup(doc)
        self._parseNodes(doc.contents, tree)

        if not test:
            return tree.getString()
        else:
            return tree
