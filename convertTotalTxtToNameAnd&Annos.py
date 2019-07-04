# the input file format: "{image name} "{nums of objs}" "{5 * num_obj}"
import sys
import os
import random

def readfile(fname, rate_tr_over_te, show):
    """
    fname: str
    rate_tr_over_te: int
    """
    dname_tr = dict() 
    dname_te = dict()
    danno_tr = dict()
    danno_te = dict()
    f = open(fname, "r")
    i = 0
    for line in f:
        i += 1

        if line.strip()=="":
            continue

        if line.find(".jpeg") > 0:
            name = line.split(".jpeg")[0] + ".jpeg"
            anno = line.split(".jpeg")[1].strip().split(" ")
        elif line.find(".jpg") > 0:
            name = line.split(".jpg")[0] + ".jpg"
            anno = line.split(".jpg")[1].strip().split(" ")
        else:
            print("image format error! please check line {}: {}".format(i, line))
            sys.exit()
        
        roinum = int(anno[0])
        if roinum * 5 != len(anno) - 1:
            print("annotation error! please check line {}: {}".format(i, line))
            sys.exit()

        if random.uniform(0, rate_tr_over_te + 1) > 1:
            dname_tr[name] = roinum
            rois = list()
            for roiIdx in range(roinum):
                roi = anno[5 * roiIdx + 1: 5 * roiIdx + 6]
                rois.append(roi)
            danno_tr[name] = rois
        else:
            dname_te[name] = roinum
            rois = list()
            for roiIdx in range(roinum):
                roi = anno[4 * roiIdx + 1: 4 * roiIdx + 6]
                rois.append(roi)
            danno_te[name] = rois

    f.close()
    return dname_tr, dname_te, danno_tr, danno_te

def writefile(dname, danno, fname, fanno, ds, show):
    if (len(dname) != len(danno)):
        print("matching error: please check name number and anno number!")
    nameFile = open(fname, "w")
    annoFile = open(fanno, "w")
    for name in dname:
        nameFile.write("{}\n".format(name))
        annoFile.write("{} ".format(dname[name]))
        for annos in danno[name]:
            for anno in annos:
                annoFile.write("{} ".format(anno))

        annoFile.write("{} \n".format(ds))
    nameFile.close()
    annoFile.close()

if __name__ == "__main__":
    dname_tr0, dname_te0, danno_tr0, danno_te0 = readfile("A/image.txt", 22, 1)
    dname_tr1, dname_te1, danno_tr1, danno_te1 = readfile("B/image.txt", 22, 1)
    writefile(dname_tr0, danno_tr0, "A_train_image.txt", "A_train_anno.txt", "", 1)
    writefile(dname_te0, danno_te0, "A_test_image.txt", "A_test_anno.txt", "", 1)
    writefile(dname_tr1, danno_tr1, "B_train_image.txt", "B_train_anno.txt", "", 1)
    writefile(dname_te1, danno_te1, "B_test_image.txt", "B_test_anno.txt", "", 1)




        
        
