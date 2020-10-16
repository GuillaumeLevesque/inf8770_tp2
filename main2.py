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


def chromasubsampling(scheme, yuv):
    if len(yuv) % 2 != 0 or len(yuv[0]) % 2 != 0:
        print("dims", len(yuv), len(yuv[0]))
        print("please use image with even dimensions")
        exit(1)
    y = np.zeros((len(yuv), len(yuv[0])))
    u = np.zeros((len(yuv), len(yuv[0])))
    v = np.zeros((len(yuv), len(yuv[0])))
    for i, line in enumerate(yuv):
        for j, triplet in enumerate(line):
            y[i][j] = (triplet[0])
            u[i][j] = (triplet[1])
            v[i][j] = (triplet[2])
    print("--")
    print("u avant", u[0][0], u[0][1], u[0][2], u[0][3], u[0][4], u[0][5], u[0][6], u[0][7])
    print("u avant", u[1][0], u[1][1], u[1][2], u[1][3], u[1][4], u[1][5], u[1][6], u[1][7])
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
    print("u apres", u[0][0], u[0][1], u[0][2], u[0][3], u[0][4], u[0][5], u[0][6], u[0][7])
    print("u apres", u[1][0], u[1][1], u[1][2], u[1][3], u[1][4], u[1][5], u[1][6], u[1][7])
    print("--")
    for i, line in enumerate(yuv):
        for j, pixel in enumerate(line):
            yuv[i][j][0] = y[i][j]
            yuv[i][j][1] = u[i][j]
            yuv[i][j][2] = v[i][j]
    return yuv


# step 0: load image in float values
image = py.imread('cageSmall.jpeg')
print("rgb", image[0][0])
py.imshow(image)
py.show()

# step 1.1: RGB -> YUV
YUV = rgb2yuv(image.astype(np.float))
print("yuv", YUV[0][0])


# step 1.2: chroma subsampling
YUV = chromasubsampling(420, YUV)
