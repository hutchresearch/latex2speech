import TexSoup

'''
Safely replace the desired child node of a parent. Required since 
  without modifying TexSoup, it will always delete the first child 
  of the parent that shares its name with the desired child.
'''
def safeReplaceChild(parent, child, childIndex, childRepl):
    if not isinstance(parent, TexSoup.data.BraceGroup) and \
       not isinstance(parent, TexSoup.data.BracketGroup):
        parent.insert(childIndex, childRepl)
        name = child.name
        tempNameSuffix = 'a'
        tempNames = []
        for deleteCand in parent.find_all(name):
            if deleteCand.position == child.position:
                child.delete()
                for tempName in tempNames:
                    parent.find(tempName).name = name
                break
            elif deleteCand.position < child.position:
                tempName = name + tempNameSuffix
                while parent.find(tempName):
                    tempNameSuffix += 'a'
                    tempName = name + tempNameSuffix
                deleteCand.name = tempName
                tempNames.append(tempName)
            else:
                print('Expected node not found, moving on')
                break
    # TODO: Implement the above functionality in the args
    else:
        parent.remove(child)
        parent.insert(childIndex, childRepl)

'''
Since the children of a node include the children of its arguments, TexSoup
  effectively goes one recursive level too deep to effectively manipulate 
  the parse tree. This function solves that by including args as children
'''
def getEffectiveChildren(node):
    children = []
    excl = []
    for arg in node.args:
        children.append(arg)
        excl.extend(arg.children)
    for child in node.children:
        if child not in excl:
            children.append(child)

    return children

'''
Seperates the contents found in a node's arguments from other contents that
  happen to belong to a node. This is a fairly frequent occurence.
'''
def seperateContents(node):
    argContents = []
    otherContents = []
    for arg in node.args:
        argContents.extend(arg.contents)
    for other in node.contents:
        if other not in argContents:
            otherContents.append(other)
    return (argContents, otherContents)

'''
Whether an element of the TexSoup parse tree is a TexNode or a TexExpr
  is unknown, so a small test is needed to truly ensure you're getting
  what is asked for.
'''
def exprTest(expr, exprType):
    exprActual = expr
    if isinstance(expr, TexSoup.data.TexNode):
        exprActual = expr.expr
    return isinstance(exprActual, exprType)