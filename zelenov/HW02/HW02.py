import xml.etree as etree
import xml.etree.ElementTree as et

tree = et.parse('banks/bank (1).xml')
root = tree.getroot()


for child in root.iter('table'):
    sub = et.SubElement(child,'column')
    sub.text = 'SomeThings!!'
    sub.set('name', 'author')

txt = et.tostring(root,encoding='UTF-8')
f = open('filename.xml','wb')
f.write(txt)
f.close()