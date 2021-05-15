from logger import logging, writelog

import re

'''
A final dummy clean function that simply removes all illegal 
instances of <, > and & from an xml string. Absolutely does 
NOT ensure broken xml will be made valid, but ensures
valid xml won't break.
'''
def cleanxml_string(xml_str):
    illegal_amp_pat = r'(?:&(?!amp;|lt;|gt;|quot;|apos;))' # Finds all & that don't denote a legal entity reference
    illegal_lt_pat = r'(<)[^<>]*<' # Finds all < that appear before another <
    illegal_lt_pat_trailing = r'(<)[^>]*$' # Finds all < that are unmatched at the end of the text
    illegal_gt_pat = r'>[^<>]*(>)' # Finds all > that appear after another >
    illegal_gt_pat_leading = r'^[^<]*(>)' # Finds all > that are unmatched at the beginning of the text
    
    amp_split = re.split(illegal_amp_pat, xml_str)
    xml_str = ''
    for s in amp_split[:-1]:
        xml_str += s + r'&amp;'
    xml_str += amp_split[-1]

    match = re.search(illegal_lt_pat, xml_str)
    while match:
        xml_str = xml_str[0:match.start(1)] + '&lt;' + xml_str[match.end(1):]
        match = re.search(illegal_lt_pat, xml_str)
    
    match = re.search(illegal_lt_pat_trailing, xml_str)
    while match:
        xml_str = xml_str[0:match.start(1)] + '&lt;' + xml_str[match.end(1):]
        match = re.search(illegal_lt_pat_trailing, xml_str)

    match = re.search(illegal_gt_pat, xml_str)
    while match:
        xml_str = xml_str[0:match.start(1)] + '&gt;' + xml_str[match.end(1):]
        match = re.search(illegal_gt_pat, xml_str)

    match = re.search(illegal_gt_pat_leading, xml_str)
    while match:
        xml_str = xml_str[0:match.start(1)] + '&gt;' + xml_str[match.end(1):]
        match = re.search(illegal_gt_pat_leading, xml_str)

    return xml_str

if __name__ == '__main__':
    print(cleanxml_string(r'<>>>><&haha&amp;'))
    print(cleanxml_string(r'<whats < the deal > with> xml tags! &&&&&&&&&amp; <  kjlsdkf <<, < jklj > <<<<>>>>>> messed up man'))
