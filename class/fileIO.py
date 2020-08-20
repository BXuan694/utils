import os
import sys

def readFile(fname = "image.txt", tails = [".jpeg", ".jpg"]):
    """
    fname: str, filename with total image&anno.
    tails: list of str, image formats in fname.
    return: dict, k: str, filename.
                  v: int, label.
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
                    anno = line.split(tail)[1].strip()
                    break

            if name in d:
                repeat += 1
                print("warning: repeated img found: {}".format(name))
            d[name] = int(anno)
    print("{}: {} unrepeated imgs and {} repeated imgs".format(fname, len(d), repeat))
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
            f.write("{}".format(d[name]))
            f.write("\n")
