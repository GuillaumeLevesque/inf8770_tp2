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


# step 0 : load image in float values
image = py.imread('cageSmall.jpeg').astype(np.float)
print("rgb", image[0][0])

# step 1 : RGB -> YUV, 4:2:0
YUV = rgb2yuv(image)
print("yuv", YUV[0][0])




