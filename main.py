import numpy as np
import matplotlib.pyplot as py


def rgb2gray(rgb):
    return np.dot(rgb[:, :], [0.299, 0.587, 0.114])


def rgb2yuv(rgb):
    yuv = []
    for i, line in enumerate(rgb):
        yuv.append([])
        for j, pixel in enumerate(line):
            yuv[i].append([])
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            yuv[i][j].append(float((r+2*g+b)/4))
            yuv[i][j].append(float(r-g))
            yuv[i][j].append(float(b-g))
    return yuv


def yuv2rgb(yuv):
    rgb = []
    for i, line in enumerate(yuv):
        rgb.append([])
        for j, pixel in enumerate(line):
            rgb[i].append([])
            y = pixel[0]
            u = pixel[1]
            v = pixel[2]
            g = int(y - ((u+v)/4))
            r = int(v+g)
            b = int(u+g)
            rgb[i][j].append(r)
            rgb[i][j].append(g)
            rgb[i][j].append(b)
    return rgb


def toprintable(baseimage):
    printable = np.clip(baseimage, 0, 255)
    for i, line in enumerate(printable):
        for j, pixel in enumerate(line):
            printable[i][j][0] = pixel[0] / 255
            printable[i][j][1] = pixel[1] / 255
            printable[i][j][2] = pixel[2] / 255
    return printable


# fig1 = py.figure(figsize=(10, 10))
imagelue = py.imread('cageSmall.jpeg')
image = imagelue.astype('int')
# imageFloat = image.astype('float')
py.imshow(image)
py.show()

# imageGray = rgb2gray(image)
imageYUV = rgb2yuv(image)
imageRGB = yuv2rgb(imageYUV)
printableYUV = toprintable(imageYUV)
# print(imageGray)
# print(imageYUV)
# imageout=imageYUV.astype('double')
# imageout = np.clip(imageYUV, 0, 255)
# imageout = imageout.astype('uint8')
# py.imshow(imageout, cmap=py.get_cmap('rgb'))
py.imshow(printableYUV)
py.show()
py.imshow(imageRGB)
py.show()
