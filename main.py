import numpy as np
import matplotlib.pyplot as py

import libinf8770 as mylib


imread = py.imread("power.jpg")

py.figure()
py.imshow(imread)

compressedimage = mylib.compressedimage(imread, yuvsubsamp = (4,2,0), dwtrecurslevel = 3, quantizdeadzone = 2, quantizstep = 2)

print("Uncompressed size:\t", compressedimage.getuncompressedsize(), " kb")
print("Compressed size:\t", compressedimage.getcompressedsize(), " kb")

printable = compressedimage.getprintable()
py.figure()
py.imshow(printable)

py.show()