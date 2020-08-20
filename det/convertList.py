import xml.etree.ElementTree as ET
import os
import sys

dataRoot = "/。。。/data/ILSVRC2012"
txtRoot = "/。。。/caffe_ssd/data/ILSVRC12det"
testTXT = "test.txt"
trainTXT = "trainval.txt"
dic = dict() #保存类别 dic={'n00000000':'shoes'}
dic = {"n03047690": "shoes", "n03680355": "shoes", "n04120489": "shoes", "n04133789": "shoes"}

for txtFile in (testTXT, trainTXT):
    phase = txtFile.split(".")[0]
    f = open(os.path.join(txtRoot, txtFile))
    for line in f:
        line = line.strip().split(' ')[1]
        xmlFile = os.path.join(dataRoot, line)
        if not os.path.isfile(xmlFile):
            print("file not exit: ", xmlFile)
            sys.exit()
        tree = ET.ElementTree(file=xmlFile)
        root = tree.getroot()
        for child in root:
            if child.tag == 'object':
                for subChild in child:
                    if subChild.tag == 'name':
                        subChild.text = dic[subChild.text]
        targetDir = dataRoot+'/new/'+phase
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        tree.write(os.path.join(targetDir, line.split('/')[-1]))

