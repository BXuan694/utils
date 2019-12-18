import os
import sys
# To read/write detection related txt flies.
# The currency are:
# list of names, list of list of 5-int box, list of int;
# dict of (name, list of list of 5-int box), (label, other items blabla).

def readFile(fname = "image.txt", tails = [".jpeg", ".jpg"]):
    """
    fname: str, filename with total image&anno.
    tails: list of str, image formats in fname.
    return: dict, k: str, filename.
                  v: list of 5-int box, all boxes in the image.
    """
    d = dict()
    repeat = 0

    with open(fname, "r") as f:
        for line in f:
            if line.strip() == "":
                continue

            for tail in tails:
                if line.find(tail) > 0:
                    name = line.split(tail)[0] + tail
                    anno = line.split(tail)[1].strip().split(" ")
                    break

            boxNum = int(anno[0])
            if boxNum * 5 != len(anno) - 1:
                print("anno error @ line:\n{}".format(line))
                sys.exit()

            boxesPerImg = list()
            for boxIdx in range(boxNum):
                box = [int(x) for x in anno[5 * boxIdx + 1: 5 * boxIdx + 6]]
                boxesPerImg.append(box)

            if name in d:
                repeat += 1
                print("warning: repeated img found: {}".format(name))
            d[name] = boxesPerImg
    print("{}: {} unrepeated imgs and {} repeated imgs".format(fname, len(d), repeat))
    return d

def readImage(fname):
    """
    fname: str, filename with imgs.
    return: list of str, all imgs.
    """
    l = list()
    with open(fname, "r") as f:
        for line in f:
            line0 = line.strip()
            l.append(line0)
    print("{}: {} imgs".format(fname, len(l)))
    return l

def readAnno(fname, hasDS = 0):
    """
    fname: str, filename with annos.
    hasDS: 0/1, if dsinfo exist.
    return: list of list of 5-int box, all boxes of each image.
    """
    l = list()
    ds = list()
    with open(fname, "r") as f:
        numImg = int(next(f))
        for line in f:
            anno = line.strip().split(" ")
            boxNum = int(anno[0])
            if boxNum * 5 != len(anno) - (2 if hasDS else 1):
                print("anno error @ line:\n{}".format(line))
                sys.exit()

            boxesPerImg = list()
            for boxIdx in range(boxNum):
                box = [int(x) for x in anno[5 * boxIdx + 1: 5 * boxIdx + 6]]
                boxesPerImg.append(box)
            if hasDS:
                ds.append(int(anno[-1]))
            l.append(boxesPerImg)

    print("{} boxes received.".format(sum([len(i) for i in l])))

    if numImg == len(l):
        print("{} imgs received.".format(numImg))
        if hasDS:
            return l, ds
        else:
            return l
    else:
        print("anno num not matched between 1st line({}) and number of line({})".format(numImg, len(l)))
        sys.exit()

def readLable(fname = "label.txt"):
    """
    fname: str, filename.
    return: dict, k: int, label of No.
                  v: list of str, other items
    """
    d = dict()
    with open(fname, "r") as f:
        for line in f:
            line0 = line.strip().split(" ")
            if len(line0) > 1:
                index = int(line0[0])
                d[index] = line0[1:]
    print("{} labels received.".format(len(d)))
    return d

def writeFile(d, outFile = "image.txt"):
    """
    d: dict, k: str, filename.
             v: list of 5-int box, all boxes in the image.
    """
    if os.path.isfile(outFile):
        print("{} exists, plz check!".format(outFile))
        sys.exit()
    with open(outFile, "w") as f:
        for name in d:
            f.write(name + " ")
            f.write("{}".format(len(d[name])))
            for box in d[name]:
                f.write(" {} {} {} {} {}".format(box[0], box[1], box[2], box[3], box[4]))
            f.write("\n")

def writeImage(l, outImage):
    """
    l: list of str, image names.
    outImage: str, filename with image.
    """
    if os.path.isfile(outImage):
        print("{} exists, plz check!".format(outImage))
        sys.exit()
    with open(outImage, "w") as f:
        for img in l:
            f.write(img + "\n")

def writeAnno(l, outAnno, ds = [], hasDS = 0):
    """
    l: list of list of 5-int box.
    outAnno: str, filename with annos.
    """
    if os.path.isfile(outAnno):
        print("{} exists, plz check!".format(outAnno))
        sys.exit()
    if hasDS:
        if len(l) != len(ds):
            print("length of ds({}) and label({}) not matched, plz check!".format(len(ds), len(l)))
            sys.exit()
        i = 0

    with open(outAnno, "w") as f:
        f.write("{}\n".format(len(l)))
        for boxes in l:
            f.write("{}".format(len(boxes)))
            for box in boxes:
                f.write(" {} {} {} {} {}".format(box[0], box[1], box[2], box[3], box[4]))
            if hasDS:
                f.write(" {}".format(ds[i]))
                i += 1
            f.write("\n")

def writeLabel(d, outLabel = "label.txt"):
    """
    d: dict, k: int, label of No.
             v: list of str, other items.
    outLabel: str, filename with labels.
    """
    if os.path.isfile(outLabel):
        print("{} exists, plz check!".format(outLabel))
        sys.exit()
    with open(outLabel, "w") as f:
        for k in d:
            string = ""
            for s in d[k]:
                string += (" " + s)
            f.write("{}{}\n".format(k, string))
