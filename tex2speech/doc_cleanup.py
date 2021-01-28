import re

def cleanXMLString(xmlStr):
    illegalAmpPat = r'(?:&(?!amp;|lt;|gt;|quot;|apos;))' # Finds all & that don't denote a legal entity reference
    illegalLtPat = r'(<)[^<>]*<' # Finds all < that appear before another <
    illegalLtPatTrailing = r'(<)[^>]*$' # Finds all < that are unmatched at the end of the text
    illegalGtPat = r'>[^<>]*(>)' # Finds all > that appear after another >
    illegalGtPatLeading = r'^[^<]*(>)' # Finds all > that are unmatched at the beginning of the text
    
    ampSplit = re.split(illegalAmpPat, xmlStr)
    xmlStr = ''
    for s in ampSplit[:-1]:
        xmlStr += s + r'&amp;'
    xmlStr += ampSplit[-1]

    match = re.search(illegalLtPat, xmlStr)
    while match:
        xmlStr = xmlStr[0:match.start(1)] + '&lt;' + xmlStr[match.end(1):]
        match = re.search(illegalLtPat, xmlStr)
    
    match = re.search(illegalLtPatTrailing, xmlStr)
    while match:
        xmlStr = xmlStr[0:match.start(1)] + '&lt;' + xmlStr[match.end(1):]
        match = re.search(illegalLtPatTrailing, xmlStr)

    match = re.search(illegalGtPat, xmlStr)
    while match:
        xmlStr = xmlStr[0:match.start(1)] + '&gt;' + xmlStr[match.end(1):]
        match = re.search(illegalGtPat, xmlStr)

    match = re.search(illegalGtPatLeading, xmlStr)
    while match:
        xmlStr = xmlStr[0:match.start(1)] + '&gt;' + xmlStr[match.end(1):]
        match = re.search(illegalGtPatLeading, xmlStr)

    return xmlStr

if __name__ == '__main__':
    print(cleanXMLString(r'<>>>><&haha&amp;'))
    print(cleanXMLString(r'<whats < the deal > with> xml tags! &&&&&&&&&amp; <  kjlsdkf <<, < jklj > <<<<>>>>>> messed up man'))
