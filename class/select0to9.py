import os
import sys
from fileIO import *

d=readFile("/Users/bxwang/file/train.txt", [".JPEG"])
d_new = dict()
for k in d:
    if d[k]<10:
        d_new[k] = d[k]

writeFile(d_new, "/Users/bxwang/file/train_new.txt")





