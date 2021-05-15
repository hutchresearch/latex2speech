import xml.etree.ElementTree as ET
import yaml
  
mytree = ET.parse('./static/test.xml')
myroot = mytree.getroot()

config_file = open('app_config.yaml')
contents = yaml.load(config_file, Loader=yaml.FullLoader)

# Helper to modify under cmd
def modify_xml(family_tag, tagName, setAttr, setVal):
    for family in mytree.findall('cmd'):
        if family.attrib['family'] == family_tag:
            modifiable = family.find(tagName)
            modifiable.set(setAttr, setVal)

# Bold Tags -> family = 'bold'
#  \em \emph \textbf
attr = ''

if contents['BOLD']['CONFIG']['TYPE'] != 'None':
    type = contents['BOLD']['CONFIG']['TYPE']
    val = contents['BOLD']['CONFIG']['EMPHASIS']
else:
    type = contents['BOLD']['DEFAULT']['TYPE']
    val = contents['BOLD']['DEFAULT']['EMPHASIS']

if (type == 'emphasis'):
    attr = 'level'

modify_xml('bold', type, attr, val)

mytree.write('./static/output.xml')