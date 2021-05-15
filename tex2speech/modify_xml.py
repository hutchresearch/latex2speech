import xml.etree.ElementTree as ET
  
mytree = ET.parse('test.xmt')
myroot = mytree.getroot()