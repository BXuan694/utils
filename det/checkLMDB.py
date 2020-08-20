import os
import sys
import lmdb
import numpy as np
from PIL import Image
from caffe.proto import caffe_pb2

path=""
if not os.path.dirname(path):
    print("path not exist, please check!")
    sys.exit()

def readFromLmdb(lmdbPath, savePath):
    lmdbEnv = lmdb.open(lmdbPath)
    lmdbTxn = lmdbEnv.begin()
    lmdbCursor = lmdbTxn.cursor()
    datum = caffe_pb2.Datum()

    datumIdx=0
    for key,value in lmdbCursor:
        print("key: ",end=" ")
        print(key)

        datum.ParseFromString(value)
        label=datum.label
        data=datum.data
        channel=datum.channels
        print("Label: %d" %label)
        print("Data length: %d" %len(data))
        print("Channels: %d" %channel)
        print("Data width: %d" %datum.width)
        print("Data height: %d" %datum.height)

        size = datum.width*datum.height

        pixels1 = datum.data[0:size]
        pixels2 = datum.data[size:2*size]
        pixels3 = datum.data[2*size:3*size]

        image1 = Image.frombytes('L', (datum.width,datum.height), pixels1)
        image2 = Image.frombytes('L', (datum.width,datum.height), pixels2)
        image3 = Image.frombytes('L', (datum.width,datum.height), pixels3)

        image4=Image.merge("RGB", (image3,image2,image1))
        image4.save(savePath+str(key)+'.jpg')
        datumIdx+=1
        print("extracted")
    print("all extracted")
    lmdbEnv.close()

readFromLmdb(path,'pic')
    





