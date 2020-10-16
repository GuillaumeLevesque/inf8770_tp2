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


def yuv2rgb(yuv):
    rgb = np.empty_like(yuv)
    for i, line in enumerate(yuv):
        for j, pixel in enumerate(line):
            y = pixel[0]
            u = pixel[1]
            v = pixel[2]
            g = y-(u+v)/4
            rgb[i][j][0] = np.int(v+g)
            rgb[i][j][1] = np.int(g)
            rgb[i][j][2] = np.int(u+g)
    return rgb


def chromasubsampling(scheme, yuv):
    if len(yuv) % 2 != 0 or len(yuv[0]) % 2 != 0:
        print("dims", len(yuv), len(yuv[0]))
        print("please use image with even dimensions")
        exit(1)
    y = np.zeros((len(yuv), len(yuv[0])))
    u = np.zeros((len(yuv), len(yuv[0])))
    v = np.zeros((len(yuv), len(yuv[0])))
    for i, line in enumerate(yuv):
        for j, pixel in enumerate(line):
            y[i][j] = (pixel[0])
            u[i][j] = (pixel[1])
            v[i][j] = (pixel[2])
    # https://medium.com/@sddkal/chroma-subsampling-in-numpy-47bf2bb5af83
    if scheme == 420:
        u[1::2, :] = u[::2, :]
        u[:, 1::2] = u[:, ::2]
        v[1::2, :] = v[::2, :]
        v[:, 1::2] = v[:, ::2]
    elif scheme == 422:
        u[:, 1::2] = u[:, ::2]
        v[:, 1::2] = v[:, ::2]
    elif scheme == 410:
        u[1::2, :] = u[::2, :]
        v[1::2, :] = v[::2, :]
    elif scheme == 444:
        print("444 scheme, no subsampling")
    else:
        print("wrong value of subsampling scheme")
        exit(-1)
    for i, line in enumerate(yuv):
        for j, pixel in enumerate(line):
            yuv[i][j][1] = u[i][j]
            yuv[i][j][2] = v[i][j]
    return yuv


# ----------------------------------------------------------------
# --------------------------- MAIN -------------------------------
# ----------------------------------------------------------------
# step 0: load image in float values
image = py.imread('cageSmall.jpeg')
py.imshow(image)
py.show()

# step 1.1: RGB -> YUV
YUV = rgb2yuv(image.astype(np.float))
# tests
py.imshow(yuv2rgb(YUV.copy()).astype("uint8"))
py.show()
Gray = YUV.copy()
for line in Gray:
    for pixel in line:
        pixel[1] = pixel[0]
        pixel[2] = pixel[0]
py.imshow(Gray.astype("uint8"))
py.show()


# step 1.2: chroma subsampling
subsamplingScheme = 420
YUV = chromasubsampling(subsamplingScheme, YUV)
# test
GraySubSample = chromasubsampling(subsamplingScheme, Gray)
py.imshow(GraySubSample.astype("uint8"))
py.show()
