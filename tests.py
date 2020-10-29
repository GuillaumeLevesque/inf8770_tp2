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
# imread = py.imread("power.jpg")

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


# # test yuvsubsampled
# imread = py.imread("cageSmall.jpeg")

# yuvimage = mylib.yuvimage()
# yuvimage.initfromimread(imread)

# yuvsubsampled = mylib.yuvsubsampled((4,2,2))
# yuvsubsampled.initfromyuvimage(yuvimage)


# # test yuvdwted
# imread = py.imread("power.jpg")

# yuvimage = mylib.yuvimage()
# yuvimage.initfromimread(imread)

# yuvsubsampled = mylib.yuvsubsampled()
# yuvsubsampled.initfromyuvimage(yuvimage)

# yuvdwted = mylib.yuvdwted()
# yuvdwted.initfromyuvsubsampled(yuvsubsampled, 3)

# print("recursion level: ", yuvdwted.recursionlevel)
# print("reconstructiondata size: ", len(yuvdwted.reconstructiondata))
# print("y shape: ", yuvdwted.y.shape)


# test quantifiedyuvdwted
imread = py.imread("power.jpg")

yuvimage = mylib.yuvimage()
yuvimage.initfromimread(imread)

yuvsubsampled = mylib.yuvsubsampled()
yuvsubsampled.initfromyuvimage(yuvimage)

yuvdwted = mylib.yuvdwted()
yuvdwted.initfromyuvsubsampled(yuvsubsampled, 3)

quantifiedyuvdwted = mylib.quantifiedyuvdwted()
quantifiedyuvdwted.initfromyuvdwted(yuvdwted, 8, 1)

print("yuvdwted.y: ", yuvdwted.y[0, 0:5])
print("quantifiedyuvdwted.y: ", quantifiedyuvdwted.y[0:5])