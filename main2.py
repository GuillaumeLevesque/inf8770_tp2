import numpy as np
import matplotlib.pyplot as py


def rgb2yuv(rgb):
    yuv = np.empty_like(rgb)
    for i, line in enumerate(rgb):
        for j, pixel in enumerate(line):
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            yuv[i][j][0] = np.float64((r+2*g+b)/4)
            yuv[i][j][1] = np.float64((b-g))
            yuv[i][j][2] = np.float64((r-g))
    return yuv


imagelue = py.imread('cageSmall.jpeg').astype(np.float)
print("rgb", imagelue[0][0])

imageYUV = rgb2yuv(imagelue)
print("yuv", imageYUV[0][0])
# py.imshow(imageYUV)
# py.show()




