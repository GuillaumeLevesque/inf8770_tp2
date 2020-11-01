import numpy as np
import matplotlib.pyplot as py

import libinf8770 as mylib

# compressedimage
imread = py.imread("cage2.jpg")
print("original size:\t", (len(imread) * len(imread[0] * 3 * 8))/1000, " kilobits")
py.figure()
py.imshow(imread)

compressedimage = mylib.compressedimage(imread, (4,2,0), 3, 4)

printable = compressedimage.getprintable()
py.figure()
py.imshow(printable)

py.show()