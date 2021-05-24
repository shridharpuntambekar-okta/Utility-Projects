import xml.etree.ElementTree as ET
import sys
def readOffsets():
    with open("offset.txt", "r") as f:
        return list(map( int ,f.readline().split(',')))

def writeOffsets(start,end):
    with open("offset.txt", "w") as f:
        f.write(f"{start},{end}")

def write_new_packagexml(incoming_members_list):
    packageXmlToWrite_path = "../manifest/package.xml"

    baseXml = """<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
    <name>Report</name>
    </types>
    <version>48.0</version>
    </Package>
    """
    
    ET.register_namespace('','http://soap.sforce.com/2006/04/metadata')
    root = ET.fromstring(baseXml)
    #print(root)
    types = root[0]
    #print(len(incoming_members_list))
    for eachMemValue in incoming_members_list:
        ET.SubElement(types, "members").text = eachMemValue
    treeToWrite = ET.ElementTree(root)
    treeToWrite.write(packageXmlToWrite_path)
    with open(packageXmlToWrite_path, 'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'+content)


    

if __name__ == "__main__":
    start,endIndex = readOffsets()
    intervalMargin = endIndex - start
    print(start,endIndex,intervalMargin)
    tree = ET.parse('GetReportsXML/folderNames.xml')
    root = tree.getroot()
    print(root.tag)
    elementChildCount = len(root[0]) - 1
    endIndex = elementChildCount if (endIndex>=elementChildCount) else endIndex
    
    memberTexts = []
    for eachEle in root[0][start:endIndex]:
        memberTexts.append(eachEle.text)    

    #print(len(memberTexts))
    #print(memberTexts)
    
    write_new_packagexml(memberTexts)
    start += intervalMargin
    endIndex += intervalMargin
    writeOffsets(start,endIndex)
        
