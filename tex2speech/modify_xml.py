import xml.etree.ElementTree as ET
import yaml

# Helper to modify under cmd
def modify_xml(family_tag, tagName, setAttr, setVal, mytree):
    for family in mytree.findall('cmd'):
        if family.attrib['family'] == family_tag:
            modifiable = family.find('modifiable')
            modifiable.tag = tagName

            for attr, val in zip(setAttr, setVal):
                modifiable.set(attr, val)

# Bold Tags -> family = 'bold'
#  \em \emph \textbf
def bold(contents, mytree):
    attr = []
    val = []

    if contents['BOLD']['CONFIG']['TYPE'] != 'None':
        type = contents['BOLD']['CONFIG']['TYPE']
        val = contents['BOLD']['CONFIG']['EMPHASIS']
    else:
        type = contents['BOLD']['DEFAULT']['TYPE']
        if (type == 'emphasis'):
            attr.append('level')
            val.append(contents['BOLD']['DEFAULT']['EMPHASIS'])
        elif (type == 'prosody'):
            attr = ['rate', 'pitch', 'volume']
            val.append(contents['BOLD']['DEFAULT']['PROSODY']['RATE'])
            val.append(contents['BOLD']['DEFAULT']['PROSODY']['PITCH'])
            val.append(contents['BOLD']['DEFAULT']['PROSODY']['VOLUME'])

    modify_xml('bold', type, attr, val, mytree)

def run_xml_modify():
    # Create tree
    mytree = ET.parse('./static/test.xml')
    myroot = mytree.getroot()

    # Read yaml contents
    config_file = open('app_config.yaml')
    contents = yaml.load(config_file, Loader=yaml.FullLoader)

    # Function calls
    bold(contents, mytree)

    # Write to output.xml
    mytree.write('./static/output.xml')