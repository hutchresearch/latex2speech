import TexSoup

def safe_replace_child(parent, child, child_index, child_repl):
    '''
    Safely replace the desired child node of a parent. Required since 
    without modifying TexSoup, it will always delete the first child 
    of the parent that shares its name with the desired child.
    '''
    if not isinstance(parent, TexSoup.data.BraceGroup) and \
       not isinstance(parent, TexSoup.data.BracketGroup):
        parent.insert(child_index, child_repl)
        name = child.name
        temp_name_suffix = 'a'
        temp_names = []
        for delete_cand in parent.find_all(name):
            if delete_cand.position == child.position:
                child.delete()
                for temp_name in temp_names:
                    parent.find(temp_name).name = name
                break
            elif delete_cand.position < child.position:
                temp_name = name + temp_name_suffix
                while parent.find(temp_name):
                    temp_name_suffix += 'a'
                    temp_name = name + temp_name_suffix
                delete_cand.name = temp_name
                temp_names.append(temp_name)
            else:
                print('Expected node not found, moving on')
                break
    # TODO: Implement the above functionality in the args
    else:
        parent.remove(child)
        parent.insert(child_index, child_repl)

def get_effective_children(node):
    '''
    Since the children of a node include the children of its arguments, TexSoup
    effectively goes one recursive level too deep to effectively manipulate 
    the parse tree. This function solves that by including args as children
    '''
    children = []
    excl = []
    for arg in node.args:
        children.append(arg)
        excl.extend(arg.children)
    for child in node.children:
        if child not in excl:
            children.append(child)

    return children

def seperate_contents(node):
    '''
    Seperates the contents found in a node's arguments from other contents that
    happen to belong to a node. This is a fairly frequent occurence.
    '''
    arg_contents = []
    other_contents = []
    for arg in node.args:
        arg_contents.extend(arg.contents)
    for other in node.contents:
        if other not in arg_contents:
            other_contents.append(other)
    return (arg_contents, other_contents)

def expr_test(expr, expr_type):
    '''
    Whether an element of the TexSoup parse tree is a TexNode or a TexExpr
    is unknown, so a small test is needed to truly ensure you're getting
    what is asked for.
    '''
    expr_actual = expr
    if isinstance(expr, TexSoup.data.TexNode):
        expr_actual = expr.expr
    return isinstance(expr_actual, expr_type)