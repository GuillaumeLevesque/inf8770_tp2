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

class yuvsubsampled:

    _supportedsubsampling = [(4, 2, 0), (4, 2, 2)]
    
    def __init__(self, subsampling: tuple = (4, 2, 0)):
        if subsampling not in yuvsubsampled._supportedsubsampling:
            raise ValueError("Unsupported subsampling", subsampling, "supported subsampling: ", yuvsubsampled._supportedsubsampling)

        self.subsampling = subsampling
        self.y = None
        self.u = None
        self.v = None

    def initfromyuvimage(self, yuvimage):
        self.y = yuvimage.y
        if self.subsampling == (4, 2, 0):
            self.u = yuvimage.u[::2, ::2] # keep 1 row in 2 and 1 element in 2 from each row
            self.v = yuvimage.v[::2, ::2]
        elif self.subsampling == (4, 2, 2):
            self.u = yuvimage.u[:, ::2] # keep every row and 1 element in 2 from each row
            self.v = yuvimage.v[:, ::2]
        else:
            print("This was not supposed to happen...")

class yuvdwted:

    def __init__(self):
        self.recursionlevel = 1
        self.y = None
        self.u = None
        self.v = None
        self.reconstructiondata = []

    def initfromyuvsubsampled(self, yuvsubsampled, recursionlevel):
        self.y = yuvsubsampled.y.copy()
        self.u = yuvsubsampled.u.copy()
        self.v = yuvsubsampled.v.copy()
        self.recursionlevel = recursionlevel

        for _ in range(recursionlevel):
            ylx = yuvdwted._filter(self.y, "lowpass", 'x')
            ulx = yuvdwted._filter(self.u, "lowpass", 'x')
            vlx = yuvdwted._filter(self.v, "lowpass", 'x')

            yhx = yuvdwted._filter(self.y, "highpass", 'x')
            uhx = yuvdwted._filter(self.u, "highpass", 'x')
            vhx = yuvdwted._filter(self.v, "highpass", 'x')

            ylxly = yuvdwted._filter(ylx, "lowpass", 'y')
            ulxly = yuvdwted._filter(ulx, "lowpass", 'y')
            vlxly = yuvdwted._filter(vlx, "lowpass", 'y')

            ylxhy = yuvdwted._filter(ylx, "highpass", 'y')
            ulxhy = yuvdwted._filter(ulx, "highpass", 'y')
            vlxhy = yuvdwted._filter(vlx, "highpass", 'y')

            yhxly = yuvdwted._filter(yhx, "lowpass", 'y')
            uhxly = yuvdwted._filter(uhx, "lowpass", 'y')
            vhxly = yuvdwted._filter(vhx, "lowpass", 'y')

            yhxhy = yuvdwted._filter(yhx, "highpass", 'y')
            uhxhy = yuvdwted._filter(uhx, "highpass", 'y')
            vhxhy = yuvdwted._filter(vhx, "highpass", 'y')

            self.y = ylxly
            self.u = ulxly
            self.v = vlxly
            self.reconstructiondata.append({
                "ylxhy": ylxhy,
                "yhxly": yhxly,
                "yhxhy": yhxhy,
                "ulxhy": ulxhy,
                "uhxly": uhxly,
                "uhxhy": uhxhy,
                "vlxhy": vlxhy,
                "vhxly": vhxly,
                "vhxhy": vhxhy
            })

    @staticmethod
    def _filter(channel, ftype, axis):
        if ftype not in ["lowpass", "highpass"]:
            raise ValueError("Invalid filter type", ftype, "valid filter types: ", ["lowpass", "highpass"])
        if axis not in ['x', 'y']:
            raise ValueError("Invalid axis", axis, "valid axis: ", ['x', 'y'])

        if axis == 'x':
            evens = channel[:, ::2] # all rows, 1 in 2 elements starting from element 0
            odds = channel[:, 1::2] # all rows, 1 in 2 elements starting from element 1
            if evens.shape == odds.shape:
                if ftype == "lowpass":
                    return (evens + odds) / 2
                elif ftype == "highpass":
                    return (evens - odds) / 2
            else: # if shapes not equal, evens will always have 1 more element in its rows
                lastelements = evens[:, -1:]
                allexceptlastelements = evens[:, :-1]
                if ftype == "lowpass":
                    result = (allexceptlastelements + odds) / 2
                elif ftype == "highpass":
                    result = (allexceptlastelements - odds) / 2
                return np.concatenate((result, lastelements), axis = 1)
        elif axis == 'y':
            evens = channel[::2, :] # 1 row in 2 starting from row 0, all elements
            odds = channel[1::2, :] # 1 row in 2 starting from row 1, all elements
            if evens.shape == odds.shape:
                if ftype == "lowpass":
                    return (evens + odds) / 2
                elif ftype == "highpass":
                    return (evens - odds) / 2
            else: # if shapes not equal, evens will always have 1 row
                lastrow = evens[-1:, :]
                allexceptlastrow = evens[:-1, :]
                if ftype == "lowpass":
                    result = (allexceptlastrow + odds) / 2
                elif ftype == "highpass":
                    result = (allexceptlastrow - odds) / 2
                return np.concatenate((result, lastrow), axis = 0)

class quantifiedyuvdwted:

    def __init__(self):
        self.y = None
        self.u = None
        self.v = None
        self.reconstructiondata = []
        self.deadzone = 0
        self.step = 1
    
    def initfromyuvdwted(self, yuvdwted, deadzone, step):
        self.y = quantifiedyuvdwted._quantify(yuvdwted.y.flatten(), deadzone, step)
        self.u = quantifiedyuvdwted._quantify(yuvdwted.u.flatten(), deadzone, step)
        self.v = quantifiedyuvdwted._quantify(yuvdwted.v.flatten(), deadzone, step)
        self.deadzone = deadzone
        self.step = step

        for i in yuvdwted.reconstructiondata:
            self.reconstructiondata.append({
                "ylxhy": quantifiedyuvdwted._quantify(i["ylxhy"].flatten(), deadzone, step),
                "yhxly": quantifiedyuvdwted._quantify(i["yhxly"].flatten(), deadzone, step),
                "yhxhy": quantifiedyuvdwted._quantify(i["yhxhy"].flatten(), deadzone, step),
                "ulxhy": quantifiedyuvdwted._quantify(i["ulxhy"].flatten(), deadzone, step),
                "uhxly": quantifiedyuvdwted._quantify(i["uhxly"].flatten(), deadzone, step),
                "uhxhy": quantifiedyuvdwted._quantify(i["uhxhy"].flatten(), deadzone, step),
                "vlxhy": quantifiedyuvdwted._quantify(i["vlxhy"].flatten(), deadzone, step),
                "vhxly": quantifiedyuvdwted._quantify(i["vhxly"].flatten(), deadzone, step),
                "vhxhy": quantifiedyuvdwted._quantify(i["vhxhy"].flatten(), deadzone, step)
            })
        
    
    @staticmethod
    def _quantify(vector, deadzone, step):
        return np.array([max(0, math.floor(((x - (deadzone / 2)) / step) + 1)) for x in vector])

class qydlzwed:

    def __init__(self):
        self.y = None
        self.ydict = None
        self.u = None
        self.udict = None
        self.v = None
        self.vdict = None
        self.reconstructiondata = []
    
    def initfromqyd(self, qyd):
        self.ydict, self.y = qydlzwed._encode(qyd.y)
        self.udict, self.u = qydlzwed._encode(qyd.u)
        self.vdict, self.v = qydlzwed._encode(qyd.v)

        for i in qyd.reconstructiondata:
            ylxhydict, ylxhy = qydlzwed._encode(i["ylxhy"])
            yhxlydict, yhxly = qydlzwed._encode(i["yhxly"])
            yhxhydict, yhxhy = qydlzwed._encode(i["yhxhy"])
            ulxhydict, ulxhy = qydlzwed._encode(i["ulxhy"])
            uhxlydict, uhxly = qydlzwed._encode(i["uhxly"])
            uhxhydict, uhxhy = qydlzwed._encode(i["uhxhy"])
            vlxhydict, vlxhy = qydlzwed._encode(i["vlxhy"])
            vhxlydict, vhxly = qydlzwed._encode(i["vhxly"])
            vhxhydict, vhxhy = qydlzwed._encode(i["vhxhy"])
            self.reconstructiondata.append({
                "ylxhy": ylxhy,
                "ylxhydict": ylxhydict,
                "yhxly": yhxly,
                "yhxlydict": yhxlydict,
                "yhxhy": yhxhy,
                "yhxhydict": yhxhydict,
                "ulxhy": ulxhy,
                "ulxhydict": ulxhydict,
                "uhxly": uhxly,
                "uhxlydict": uhxlydict,
                "uhxhy": uhxhy,
                "uhxhydict": uhxhydict,
                "vlxhy": vlxhy,
                "vlxhydict": vlxhydict,
                "vhxly": vhxly,
                "vhxlydict": vhxlydict,
                "vhxhy": vhxhy,
                "vhxhydict": vhxhydict,
            })
    
    @staticmethod
    def _getinitdict(vector):
        symbols = np.array([], dtype = int)
        
        for symb in vector:
            if symb not in symbols:
                symbols = np.append(symbols, symb)
        
        initdict = {}
        symbols.sort()
        for i in range(symbols.size):
            initdict[str(symbols[i])] = "{:b}".format(i).zfill(int(np.ceil(np.log2(symbols.size))))

        return initdict
    
    @staticmethod
    def _encode(vector):
        initdict = qydlzwed._getinitdict(vector)
        encdict = initdict.copy()
        encoded = np.array([], dtype = str)
        pos = 0

        while pos < vector.size:
            subsymbols = str(vector[pos])
            subsymbolsinencdict = ""

            while subsymbols in encdict and pos < vector.size:
                subsymbolsinencdict = subsymbols
                pos += 1
                if pos < vector.size:
                    subsymbols += str(vector[pos])

            encoded = np.append(encoded, encdict[subsymbolsinencdict])

            if pos < vector.size:
                encdict[subsymbols] = "{:b}".format(len(encdict))

                if np.ceil(np.log2(len(encdict))) > len(encoded[-1]):
                    for symb, code in encdict.items():
                        encdict[symb] = code.zfill(int(np.ceil(np.log2(len(encdict)))))
        
        return initdict, encoded


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
