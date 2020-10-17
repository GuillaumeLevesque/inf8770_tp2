import math
import numpy as np


class image:

    def __init__(self):
        self.width = 0
        self.height = 0

    def size(self):
        return (self.width, self.height)

class rgbimage(image):

    def __init__(self):
        image.__init__(self)
        self.r = None
        self.g = None
        self.b = None

    def initfromimread(self, imread):
        self.height, self.width = imread.shape[0:2]
        self.r = imread[:, :, 0]
        self.g = imread[:, :, 1]
        self.b = imread[:, :, 2]

    def initfromyuvimage(self, yuvimage):
        self.width, self.height = yuvimage.size()
        g = yuvimage.y - ((yuvimage.u + yuvimage.v) / 4) # g = y - ((u + v) / 4)
        self.g = np.clip(g, 0, 255)
        self.r = yuvimage.v + self.g # r = v + g
        self.b = yuvimage.u + self.g # b = u + g
        self.r = self.r.astype(np.uint8)
        self.g = self.g.astype(np.uint8)
        self.b = self.b.astype(np.uint8)

    def getprintable(self):
        printable = np.empty((self.height, self.width, 3), np.uint8)
        for y, row in enumerate(printable):
            for x, pixel in enumerate(row):
                pixel[0] = self.r[y, x]
                pixel[1] = self.g[y, x]
                pixel[2] = self.b[y, x]
        return printable

class yuvimage(image):

    def __init__(self):
        image.__init__(self)
        self.y = None
        self.u = None
        self.v = None
    
    def initfromimread(self, imread):
        self.height, self.width = imread.shape[0:2]
        imread = imread.astype(np.float64)
        self.y = (imread[:, :, 0] + (2 * imread[:, :, 1]) + imread[:, :, 2]) / 4 # y = (r + 2g + b) / 4
        self.u = imread[:, :, 2] - imread[:, :, 1] # u = b - g
        self.v = imread[:, :, 0] - imread[:, :, 1] # v = r - g

    def initfromrgbimage(self, rgbimage):
        self.width, self.height = rgbimage.size()
        rgbimage.r = rgbimage.r.astype(np.float64)
        rgbimage.g = rgbimage.g.astype(np.float64)
        rgbimage.b = rgbimage.b.astype(np.float64)
        self.y = (rgbimage.r + (2 * rgbimage.g) + rgbimage.b) / 4 # y = (r + 2g + b) / 4
        self.u = rgbimage.b - rgbimage.g # u = b - g
        self.v = rgbimage.r - rgbimage.g # v = r - g

# class yuvsubsampled:
    # todo


# rgbpixel:     np.ndarray of shape = (3,) and dtype = np.uint8
#               first column is r value, second column is g value, third column is b value
#
# returns:      np.ndarray of shape = (3,) and dtype = np.float64
#               first column is y value, second column is u value, third column is v value
def rgbpixtoyuvpix(rgbpixel: np.ndarray):
    rgbpixel = rgbpixel.astype(np.float64)
    yuvpixel = np.empty((3,), np.float64)
    yuvpixel[0] = (rgbpixel[0] + (2 * rgbpixel[1]) + rgbpixel[2]) / 4 # y = (r + 2g + b) / 4
    yuvpixel[1] = rgbpixel[2] - rgbpixel[1] # u = b - g
    yuvpixel[2] = rgbpixel[0] - rgbpixel[1] # v = r - g
    return yuvpixel

# yuvpixel:     np.ndarray of shape = (3,) and dtype = np.float64
#               first column is y value, second column is u value, third column is v value
#
# returns:      np.ndarray of shape = (3,) and dtype = np.uint8
#               first column is r value, second column is g value, third column is b value
def yuvpixtorgbpix(yuvpixel: np.ndarray):
    rgbpixel = np.empty((3,), np.float64)
    g = yuvpixel[0] - ((yuvpixel[1] + yuvpixel[2]) / 4) # g = y - ((u + v) / 4)
    rgbpixel[1] = np.clip(g, 0, 255)
    rgbpixel[0] = yuvpixel[2] + rgbpixel[1] # r = v + g
    rgbpixel[2] = yuvpixel[1] + rgbpixel[1] # b = u + g
    return rgbpixel.astype(np.uint8)
