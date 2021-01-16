'''
Safely replace the desired child node of a parent. Required since 
  without modifying TexSoup, it will always delete the first child 
  of the parent that shares its name with the desired child.
'''
def safeReplaceChild(parent, child, childIndex, childRepl):
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