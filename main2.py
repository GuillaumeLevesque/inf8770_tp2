import numpy as np
import matplotlib.pyplot as py


def rgb2yuv(rgb):
    yuv = np.empty_like(rgb)
    for i, line in enumerate(rgb):
        for j, pixel in enumerate(line):
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            yuv[i][j][0] = (np.float64((r+2*g+b)/4)/255)
            yuv[i][j][1] = (np.float64((r-g)/255))
            yuv[i][j][2] = (np.float64((b-g)/255))
    print("yuv", yuv)
    return yuv


imagelue = py.imread('cageSmall.jpeg')
print(type(imagelue[0][0][0]))
print("lue", imagelue)
image = imagelue.astype(np.float)
print(type(image[0][0][0]))
print("asFloat", image)

imageYUV = rgb2yuv(image)

imageout = image.astype(np.uint8)
print(type(imageYUV[0][0][0]))
print("asUint8", imageout)

py.imshow(imageout)
py.show()

# imageYUV = imageYUV.astype(np.uint8)
print(type(imageYUV[0][0][0]))
print("asUint8", imageout)
py.imshow(imageYUV)
py.show()




