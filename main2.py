import numpy as np
import matplotlib.pyplot as py


def rgb2yuv(rgb):
    yuv = np.empty_like(rgb)
    for i, line in enumerate(rgb):
        for j, pixel in enumerate(line):
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            yuv[i][j][0] = np.clip(np.float64((r+2*g+b)/4), 0, 255)
            yuv[i][j][1] = np.clip(np.float64((b-g)), 0, 255)
            yuv[i][j][2] = np.clip(np.float64((r-g)), 0, 255)
    return yuv


imagelue = py.imread('cageSmall.jpeg')
print("rgb", imagelue[110][110])

imageYUV = rgb2yuv(imagelue.astype(np.float)).astype(np.uint8)
print("yuv", imageYUV[110][110])
# py.imshow(imageYUV)
# py.show()




