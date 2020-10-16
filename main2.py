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


def chroma_subsampling(scheme, yuv):
    if len(yuv) % 2 != 0 or len(yuv[0]) % 2 != 0:
        print("dims", len(yuv), len(yuv[0]))
        print("please use image with even dimensions")
        exit(1)
    u = np.zeros((len(yuv), len(yuv[0])))
    v = np.zeros((len(yuv), len(yuv[0])))
    for i, line in enumerate(yuv):
        for j, pixel in enumerate(line):
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


def dwt(yuv, nb_recursion):
    if nb_recursion == 0:
        return yuv
    else:
        y = np.zeros((len(yuv), len(yuv[0])))
        u = np.zeros((len(yuv), len(yuv[0])))
        v = np.zeros((len(yuv), len(yuv[0])))
        for i, line in enumerate(yuv):
            for j, pixel in enumerate(line):
                y[i][j] = (pixel[0])
                u[i][j] = (pixel[1])
                v[i][j] = (pixel[2])

        # f1
        yf1 = (y[:, ::2] + y[:, 1::2])/2
        uf1 = (u[:, ::2] + u[:, 1::2])/2
        vf1 = (v[:, ::2] + v[:, 1::2])/2

        # fh
        yfh = (y[:, ::2] - y[:, 1::2])/2
        ufh = (u[:, ::2] - u[:, 1::2])/2
        vfh = (v[:, ::2] - v[:, 1::2])/2

        # f11
        yf11 = (yf1[::2, :] + yf1[1::2, :])/2
        uf11 = (uf1[::2, :] + uf1[1::2, :])/2
        vf11 = (vf1[::2, :] + vf1[1::2, :])/2

        # f1h
        yf1h = (yf1[::2, :] - yf1[1::2, :])/2
        uf1h = (uf1[::2, :] - uf1[1::2, :])/2
        vf1h = (vf1[::2, :] - vf1[1::2, :])/2

        # fh1
        yfh1 = (yfh[::2, :] + yfh[1::2, :])/2
        ufh1 = (ufh[::2, :] + ufh[1::2, :])/2
        vfh1 = (vfh[::2, :] + vfh[1::2, :])/2

        # fhh
        yfhh = (yfh[::2, :] - yfh[1::2, :])/2
        ufhh = (ufh[::2, :] - ufh[1::2, :])/2
        vfhh = (vfh[::2, :] - vfh[1::2, :])/2

        # next recursion
        yuv_f11 = np.zeros((len(yf11), len(yf11[0]), 3))
        for i, line in enumerate(yf11):
            for j, pixel in enumerate(yf11[0]):
                yuv_f11[i][j][0] = yf11[i][j]
                yuv_f11[i][j][1] = uf11[i][j]
                yuv_f11[i][j][2] = vf11[i][j]
        yuv_f11 = dwt(yuv_f11, nb_recursion - 1)

        # rebuild complete image after recursions
        for i, line in enumerate(yuv_f11):
            for j, pixel in enumerate(yuv_f11[0]):
                yf11[i][j] = yuv_f11[i][j][0]
                uf11[i][j] = yuv_f11[i][j][1]
                vf11[i][j] = yuv_f11[i][j][2]
        y = np.concatenate((np.concatenate((yf11, yfh1)), np.concatenate((yf1h, yfhh))), axis=1)
        u = np.concatenate((np.concatenate((uf11, ufh1)), np.concatenate((uf1h, ufhh))), axis=1)
        v = np.concatenate((np.concatenate((vf11, vfh1)), np.concatenate((vf1h, vfhh))), axis=1)
        for i, line in enumerate(yuv):
            for j, pixel in enumerate(yuv[0]):
                yuv[i][j][0] = y[i][j]
                yuv[i][j][1] = u[i][j]
                yuv[i][j][2] = v[i][j]
        return np.array(yuv)


def dwt_inverse():
    # TODO
    print("dwt inverse!")


# ----------------------------------------------------------------
# --------------------------- MAIN -------------------------------
# ----------------------------------------------------------------
# step 0: load image in float values
image = py.imread('cage2.jpg')
py.imshow(image)
py.show()

# step 1.1: RGB -> YUV
YUV = rgb2yuv(image.astype(np.float))
# tests
py.imshow(yuv2rgb(YUV.copy()).astype("uint8"))
py.show()
gray_test = YUV.copy()
for line in gray_test:
    for pixel in line:
        pixel[1] = pixel[0]
        pixel[2] = pixel[0]
py.imshow(gray_test.astype("uint8"))
py.show()


# step 1.2: chroma subsampling
subsampling_scheme = 420
YUV = chroma_subsampling(subsampling_scheme, YUV)
# test
gray_test = chroma_subsampling(subsampling_scheme, gray_test)
py.imshow(gray_test.astype("uint8"))
py.show()

# step 2: DWT
nb_recursion = 2
YUV = dwt(YUV, nb_recursion)
# test
gray_test = dwt(gray_test, nb_recursion)
py.imshow(gray_test.astype("uint8"))
py.show()
