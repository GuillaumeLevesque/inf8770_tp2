import numpy as np
import matplotlib.pyplot as py

import libinf8770 as mylib


# # test rgbpixtoyuvpix and yuvpixtorgbpix
# inimage = py.imread('cageSmall.jpeg')

# yuvimage = np.empty(inimage.shape, np.float64)
# rgbimage = np.empty_like(inimage)

# for x, row in enumerate(inimage):
#     for y, pixel in enumerate(row):
#         yuvimage[x, y] = mylib.rgbpixtoyuvpix(pixel)

# for x, row in enumerate(yuvimage):
#     for y, pixel in enumerate(row):
#         rgbimage[x, y] = mylib.yuvpixtorgbpix(pixel)

# py.figure()
# py.imshow(inimage)
# py.figure()
# py.imshow(rgbimage)
# py.show()


# # test rgbimage and yuvimage
# imread = py.imread("cageSmall.jpeg")

# rgbimage = mylib.rgbimage()
# rgbimage.initfromimread(imread)
# printable = rgbimage.getprintable()
# py.figure()
# py.imshow(printable)

# yuvimage = mylib.yuvimage()
# yuvimage.initfromimread(imread)
# rgbimage.initfromyuvimage(yuvimage)
# printable = rgbimage.getprintable()
# py.figure()
# py.imshow(printable)

# yuvimage.initfromrgbimage(rgbimage)
# rgbimage.initfromyuvimage(yuvimage)
# printable = rgbimage.getprintable()
# py.figure()
# py.imshow(printable)

# py.show()