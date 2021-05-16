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
def bold_helper(conf_def, contents):
    attr = []
    val = []

    type = contents['BOLD'][conf_def]['TYPE']
    if (type == 'emphasis'):
        attr.append('level')
        val.append(contents['BOLD'][conf_def]['EMPHASIS'])
    elif (type == 'prosody'):
        attr = ['rate', 'pitch', 'volume']
        val.append(contents['BOLD'][conf_def]['PROSODY']['RATE'])
        val.append(contents['BOLD'][conf_def]['PROSODY']['PITCH'])
        val.append(contents['BOLD'][conf_def]['PROSODY']['VOLUME'])

    return type, attr, val

def bold(contents, mytree):
    if contents['BOLD']['CONFIG']['TYPE'] != 'None':
        type, attr, val = bold_helper('CONFIG', contents)
    else:
        type, attr, val = bold_helper('DEFAULT', contents)

    modify_xml('bold', type, attr, val, mytree)

def run_xml_modify():
    # Create tree
    mytree = ET.parse('./static/test.xml')
    myroot = mytree.getroot()

    # Read yaml contents
    config_file = open('temporary.yaml')
    contents = yaml.load(config_file, Loader=yaml.FullLoader)

    # Function calls
    bold(contents, mytree)

    # Write to output.xml
    mytree.write('./static/output.xml')