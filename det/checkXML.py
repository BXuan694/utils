# This to draw lines from .xml on the original images.
import os
import sys
from PIL import Image
import numpy as np
import random
from xml.etree import ElementTree as ET

rootFolder = ""
fn=open("test.txt",'r')
targetIdx=random.randint(0,3014)
for idx,line in enumerate(fn):
    if(idx==targetIdx):
        line=line.strip().split(' ')
        img=line[0]
        des=line[1]
        break

print(img)
pic=Image.open(os.path.join(rootFolder,img))
pic=np.array(pic)
print("shape: "+str(pic.shape))
print(des)

ymin=list()
ymax=list()
xmin=list()
xmax=list()

with open(os.path.join(rootFolder,des),'r') as f:
    strXML=f.read()
    treeRoot=ET.XML(strXML)
    for it in treeRoot.iter("xmin"):
        xmin.append(int(it.text))
        print(it.tag,it.text)
    for it in treeRoot.iter("ymin"):
        ymin.append(int(it.text))
        print(it.tag,it.text)
    for it in treeRoot.iter("xmax"):
        xmax.append(int(it.text))
        print(it.tag,it.text)
    for it in treeRoot.iter("ymax"):
        ymax.append(int(it.text))
        print(it.tag,it.text)

for i in range(len(xmin)):
    print("bbox "+str(i)+": ",end=' ')
    print(xmin[i],ymin[i],xmax[i],ymax[i])

for num in range(len(xmin)):
    for i in range(xmin[num],xmax[num]+1):
        pic[ymin[num],i]=255
        pic[ymax[num],i]=255
    for i in range(ymin[num],ymax[num]+1):
        pic[i,xmin[num]]=255
        pic[i,xmax[num]]=255

pic=Image.fromarray(pic)
pic.save(str(targetIdx)+".JPEG")