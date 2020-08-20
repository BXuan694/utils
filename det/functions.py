import os
import sys
import csv
import shutil
import copy

def mixDS(lNames, lLabels):
    """
    lNames: list of list of str, names of datasets
    lLabels: list of list of list of 5-int box
    return: dict, k: str, filename.
                  v: list of 5-int box, all boxes in the image.
    """
    if len(lNames) != len(lLabels):
        print("lenth not matched({} vs {}), plz check!".format(len(lNames), len(lLabels)))
        sys.exit()
    dTot = dict()
    for i in range(len(lNames)):
        dSub = dict(zip(lNames[i], lLabels[i]))
        for k, v in dSub:
            if k in dTot:
                print("{} repeats in 2 ds, plz check!".format(k))
                sys.exit()
            else:
                dTot[k] = v
    return dTot

def copyFile(root, sourceTxt, destDir):
    """
    root: str, the prefix of file in sourceTxt: "/xxxx", "~".
    sourceTxt: str, the file names in root.
    destDir: str, play as root.
    """
    if not os.path.isdir(root):
        print("{} directory not exist, plz check!".format(root))
        sys.exit()
    if not os.path.isdir(destDir):
        while True:
            goOn = input("{} not found. Sure to make?[y/n]".format(destDir))
            if goOn == "n":
                print("stop making. please check.")
                sys.exit()
            elif goOn == "y":
                print("make {}".format(destDir))
                os.makedirs(destDir)
                break
    if len(os.listdir(destDir)) > 0:
        while True:
            goOn = input("{} files found in destin dir. Sure to copy?[y/n]".format(len(os.listdir(destDir))))
            if goOn == "n":
                print("stop copying. please check.")
                sys.exit()
            elif goOn == "y":
                print("go on copying.")
                break

    with open(sourceTxt, "r") as fin:
        for line in fin:
            fSoc = os.path.join(root, line.strip())
            if not os.path.isfile(fSoc):
                print("file not found: {}".format(fSoc))
                continue
            fDes = os.path.join(destDir, line.strip())
            fpathDes, _ = os.path.split(fDes)
            if not os.path.exists(fpathDes):
                os.makedirs(fpathDes)
            shutil.copyfile(fSoc, fDes)
            print("copy %s -> %s"%(fSoc, fDes))

def classifyByLabel(lBoxes):
    """
    lBoxes: list of list of 5-int box, all anno boxes.
    return: dict, k: int, label, 
                  v: list of list of 4-int box, all boxes.
    """
    d = dict()
    for boxes in lBoxes:
        for box in boxes:
            if box[4] not in d:
                d[box[4]] = list()
            d[box[4]].append(box[0:4])
    return d

def removeLabel(lBoxes, dLabel, delCls = []):
    """
    lBoxes: list of list of 5-int box, all anno boxes.
    dLabel: dict, k: int, label of No.
                  v: list of str, other items.
    delCls: list of ints, labels to delete.
    return: list of list of 5-int box, dict.
    """
    dLabel_del = copy.deepcopy(dLabel)
    for idx in delCls:
        if idx not in dLabel_del:
            print("label {} to remove not exist, plz check!".format(idx))
            sys.exit()
        else:
            del dLabel_del[idx]

    lBoxes_del = list()
    for boxes in lBoxes:
        l = list()
        for box in boxes:
            if box[4] not in delCls:
                l.append(box)
        lBoxes_del.append(l)

    return lBoxes_del, dLabel_del

def reOrganizeLabelFromN(lBoxes, dLabel, n = 1):
    """
    lBoxes: list of list of 5-int box, all anno boxes.
    dLabel: dict, k: int, label of No.
                  v: list of str, other items.
    n: int, beginning of the first label.
    return: list of list of 5-int box, dict.
    """
    dTransfer = dict()
    dLabel_reOrg = dict()
    i = n
    for k in dLabel:
        dTransfer[k] = i
        dLabel_reOrg[i] = dLabel[k]
        i += 1

    lBoxes_reOrg = copy.deepcopy(lBoxes)
    for boxes in lBoxes_reOrg:
        for box in boxes:
            box[4] = dTransfer[box[4]]

    return lBoxes_reOrg, dLabel_reOrg

def writeClsInCSV(d, csvName):
    """
    d: dict, k: int, label, 
             v: list of list of 4-int box, all boxes.
    csvName: str, csv filename to write        
    """
    with open(csvName, "w") as f:
        csvWriter = csv.writer(f, dialect = "excel")
        csvWriter.writerow(["label", "num", "avr", "median"])
        for label in d:
            if len(d[label]) > 0:
                a = list()
                l = list()
                for box in d[label]:
                    w = box[2] - box[0]
                    h = box[3] - box[1]
                    if w==0 or h==0:
                        print("strange box found: {}".format(box))
                    elif w<0 or h<0:
                        print("error @ box {}".format(box))
                        sys.exit()
                    a.append(w * h)
                    l.append([box[0], box[1], box[2], box[3]])
                a.sort()
                num = len(a)
                avr = sum(a)/num
                mid = num // 2
                median = (a[mid] + a[~mid])/2

                csvWriter.writerow([label, num, avr, median])

def drawBoxDistribution(d, saveFolder, mode = ""):
    """
    """
    import numpy as np  
    import matplotlib  
    matplotlib.use('Agg')  
    from matplotlib.pyplot import plot,savefig
    for label in d:
        if len(d[label]) > 0:
            lw = list()
            lh = list()
            for box in d[label]:
                w = box[2] - box[0]
                h = box[3] - box[1]
                if w<0 or h<0:
                    print("error @ box {}".format(box))
                    sys.exit()
                if w==0 or h==0:
                    print("strange box found: {}".format(box))
                lw.append(w)
                lh.append(h)

            plt.scatter(lw, lh, label = label)
            
