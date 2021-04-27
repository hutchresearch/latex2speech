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
from expand_macros import expand_doc_macros

from sympytossml import convert_sympy_ssml, QuantityModes
from tex_soup_utils import expr_test, seperate_contents
from tex_to_sympy import run_sympy

is_dbg = True

class ConversionParser:
    '''
    Main parsing class. Parses TexSoup parse trees into SSMLElementNode
    trees for future output. The conversion rules for every command 
    and environment found in the tree is determined by the database
    the class is initialized with.
    '''
    def __init__(self, db: ConversionDB):
        self.db = db
        self.env_stack = []
        self.index = 0

        if is_dbg:
            self.parse_env = 0
            self.res_env = 0
            self.parse_cmd = 0
            self.res_cmd = 0
            self.parse_nodes = 0

            self.prefix = ""

    def _appendText(self, text, left_child, parent):
        if left_child:
            left_child.appendTailText(text)
        else:
            parent.appendHeadText(text)

    def _parseTableContents(self, contents_node, elem_list_parent, left_child=None):
        '''
        Function that will take in new table contents, and parse
        each column
        '''
        # if is_dbg:
        #     print(">{}Parse Table Contents".format(self.prefix))

        split = str(contents_node).split("\n")
        # Go through each row
        for row in split:
            self._appendText("New Row: ", left_child, elem_list_parent)

            inner_split = row.split('&')
            column = 1

            # Go through each value in the row
            for word in inner_split: 
                if word != "&":
                    text = ", Column " + str(column) + ", Value: " + word

                    self._appendText(text, left_child, elem_list_parent)

                    column += 1
            
        # if is_dbg:
        #     print("<{}Parse Table Contents".format(self.prefix))

    def _parseTableNode(self, contents):
        '''
        This function strips out unnecessary environments from table node
        TexSoup doesn't delete \begin{tabular} or \end{tabular} tags
        so this is what this function will do before passing contents
        to parseTableContents function
        '''
        table_contents = str(contents).replace('\hline', '')
        table_contents = table_contents[table_contents.find('\n'):]
        table_contents = table_contents.lstrip()
        table_contents = table_contents.split("\end{tabular}", 1)[0]
        table_contents = table_contents.rstrip()
        return table_contents

    def _getArg(self, node, arg_elem):
        '''
        Retrieves the correct argument node's list of arguments with respect to 
        the format of the ArgElement class.
        '''
        # if is_dbg:
        #     print(">{}Get Arg".format(self.prefix))

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

        # if is_dbg:
        #     print("<{}Get Arg".format(self.prefix))

        return arg

    def _envContentsToString(self, env):
        string = ''
        for val in env.all:
            string += str(val)
        return string

    def _resolveEnvironmentElements(self, env_node, elem_list_parent, elem_list, left_child):
        '''
        Recursively resolves non-node SSMLElements within elem_list with respect to 
        env_node. Also manages the env_stack.
        '''
        if is_dbg:
            self.res_env += 1
            # print(">{}Resolve Environment Elements #{}".format(self.prefix, self.res_env))
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
                        _, parse_target = seperate_contents(env_node)
                    elif isinstance(elem, TextElement):
                        text = elem.getHeadText()
                        self._appendText(text, left_child, elem_list_parent)
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")
                        
                    # TODO: Should args within an environment's arguments reference the environment
                    # If not, stack operations should only occur in ContentElement
                    if parse_target:
                        definition = self.db.getEnvDefinition(env_node.name)

                        if definition:
                            if 'mathmode' in definition and definition['mathmode'] == True:
                                output = run_sympy(self._envContentsToString(env_node))
                                self._appendText(str(output), left_child, elem_list_parent)
                            elif 'readTable' in definition and definition['readTable'] == True:
                                self._parseTableContents(self._parseTableNode(env_node), elem_list_parent, left_child=left_child)
                            else:
                                self.env_stack.append(definition)
                                new_ind = self._parseNodes(parse_target, elem_list_parent, elem_list, insert_index=i, left_child=left_child)
                                self.env_stack.pop()
                        else:
                            new_ind = self._parseNodes(parse_target, elem_list_parent, elem_list, insert_index=i, left_child=left_child)
                    
                    next_offset += new_ind - i
                    offset += next_offset

                    # In all cases, we must preserve tail text of the placeholder SSMLElement
                    self._appendText(elem.getTailText(), left_child, elem_list_parent)
                else:
                    self._resolveEnvironmentElements(env_node, elem_list[i], elem_list[i].children, None)

                i = (k + 1) + offset
                if i > 0:
                    left_child = elem_list[i-1]
        if is_dbg:
            # print("<{}Resolve Environment Elements #{}".format(self.prefix, self.res_env))
            self.res_env -= 1

    def _parseEnvironment(self, env_node, ssml_parent, left_child):
        '''
        Handles environment parsing, returning the result of its parsing or 
        or none of no appropriate definition is found.
        '''
        # if is_dbg:
        #     print(">{}Parse Environment".format(self.prefix))
        #     print("-{}  Environment Name : {}".format(self.prefix, env_node.name))

        args, contents = seperate_contents(env_node)

        elem_list = self.db.getEnvConversion(env_node.name)

        # print("-{}Parse Environment: Got element list {}".format(self.prefix, elem_list))
        if not elem_list:
            elem_list = []
            self._parseNodes(contents, ssml_parent, elem_list, left_child=left_child)
        else:
            self._resolveEnvironmentElements(env_node, ssml_parent, elem_list, left_child)

        # if is_dbg:
        #     print("<{}Parse Environment".format(self.prefix))

        return elem_list

    def _resolveCmdElements(self, cmd_node, elem_list_parent, elem_list, left_child):
        '''
        Recursively resolves non-node SSMLElements within elem_list with respect to 
        env_node.
        '''
        if is_dbg:
            self.res_cmd += 1
            # print(">{}Resolve Command Elements #{}".format(self.prefix, self.res_cmd))
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
                            new_ind = self._parseNodes(arg.contents, elem_list_parent, elem_list, insert_index=i, left_child=left_child)
                    elif isinstance(elem, TextElement):
                        text = elem.getHeadText()

                        # Handle \item command
                        if (str(cmd_node)[:5] == r'\item'):
                            text = str(cmd_node)[5:]

                        self._appendText(text, left_child, elem_list_parent)
                    else:
                        raise RuntimeError("Unhandled non-node SSML Element encountered")

                    next_offset += new_ind - i
                    offset += next_offset

                    # In all cases, we must preserve tail text of the placeholder SSMLElement
                    self._appendText(elem.getTailText(), left_child, elem_list_parent)
                else:
                    self._resolveCmdElements(cmd_node, elem_list[i], elem_list[i].children, None)
                i = (k + 1) + offset
                if i > 0:
                    left_child = elem_list[i-1]
        if is_dbg:
            # print("<{}Resolve Command Elements #{}".format(self.prefix, self.res_cmd))
            self.res_cmd -= 1

    def _parseCommand(self, cmd_node, ssml_parent, left_child):
        '''
        Handles command parsing, returning the result of its parsing or 
        or none of no appropriate definition is found.
        '''
        # if is_dbg:
        #     print(">{}Parse Command".format(self.prefix))
        #     print("-{}  Command Name : {}".format(self.prefix, cmd_node.name))

        args, _ = seperate_contents(cmd_node)
        
        elem_list = None
        if len(self.env_stack) > 0 and cmd_node.name in self.env_stack[-1]:
            elem_list = self.env_stack[-1][cmd_node.name]
        else:
            elem_list = self.db.getCmdConversion(cmd_node.name)
        
        if elem_list:
            self._resolveCmdElements(cmd_node, ssml_parent, elem_list, left_child)

        # if is_dbg:
            # print("<{}Parse Command".format(self.prefix))

        return elem_list

    def _parseNodes(self, tex_nodes: list, ssml_parent: SSMLElementNode, ssml_children, insert_index=0, left_child=None):
        '''
        Main entry point to all parsing. Parses wih respect to a list of TexSoup
        nodes, a parent SSMLElementNode and its children. The children don't 
        necessarily correspond to the parent's actual list of children in 
        order to facilitate processing seperate lists of nodes.
        '''
        if is_dbg:
            self.parse_nodes += 1
            self.prefix = "\t" * (self.parse_nodes-1)
            # print(">{}Parse Nodes #{}".format(self.prefix, self.parse_nodes))
            # print(">{}  with children {}".format(self.prefix, ssml_children))
            # print(">{}  and insert index {}".format(self.prefix, insert_index))
        for texNode in tex_nodes:
            parseOut = None
            if insert_index > 0:
                left_child = ssml_children[insert_index-1]
            if expr_test(texNode, TexSoup.data.TexEnv):
                parseOut = self._parseEnvironment(texNode, ssml_parent, left_child)
            elif expr_test(texNode, TexSoup.data.TexCmd):
                parseOut = self._parseCommand(texNode, ssml_parent, left_child)
            elif expr_test(texNode, TexSoup.data.Token):
                text = str(texNode)
                self._appendText(text, left_child, ssml_parent)
            if parseOut:
                # print("-{}Parse Nodes #{}: Inserting parsed contents {}".format(self.prefix, self.parse_nodes, parseOut))
                # print("-{}   into {}".format(self.prefix, ssml_children))
                # print("-{}   at index {}".format(self.prefix, insert_index))
                for ssmlChild in parseOut:
                    ssml_children.insert(insert_index, ssmlChild)
                    insert_index += 1
                # print("-{}Result: {}".format(self.prefix, ssml_children))
                # print("-{}  with an index of {}".format(self.prefix, insert_index))

            if insert_index > 0:
                left_child = ssml_children[insert_index-1]
        
        if is_dbg:
            self.prefix = "\t" * (self.parse_nodes-1)
            # print("<{}Parse Nodes #{}".format(self.prefix, self.parse_nodes))
            self.parse_nodes -= 1
            if self.parse_nodes >= 0:
                self.prefix = "\t" * (self.parse_nodes-1)

        return insert_index

    def _printTreeSub(self, tree, level, level_arr, at_index, parent_index):
        if len(level_arr) == level:
            level_arr.append([])
        level_arr[level].append(str(parent_index) + ' -> ' + str(tree))
        for i, child in enumerate(tree.children):
            self._printTreeSub(child, level+1, level_arr, i, at_index)


    def printTree(self, tree):
        '''
        Basic print method to see whats happening within the tree
        '''
        level_arr = []
        self._printTreeSub(tree, 0, level_arr, 0, -1)
        for level in level_arr:
            print(level)

    
    def parse(self, doc, test=False):
        '''
        Parse doc with respect to the database the parser was initialized with.
        '''
        tree = RootElement()
        
        # if is_dbg:
        #     print("!!!Input Tex Document!!!")
        #     print("Pre Macro-Expansion:")
        #     print(doc)
        doc = expand_doc_macros(doc)
        # if is_dbg:
        #     print("Post Macro-Expansion:")
        #     print(doc)
        #     print('==========================================')
        self._parseNodes(doc.contents, tree, tree.children)

        if not test:
            return tree.getString()
        else:
            return tree
