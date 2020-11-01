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
        # self.g = np.clip(g, 0, 255)
        # self.r = np.clip(yuvimage.v + self.g, 0, 255) # r = v + g
        # self.b = np.clip(yuvimage.u + self.g, 0, 255) # b = u + g
        self.r = np.clip(yuvimage.v + g, 0, 255) # r = v + g
        self.b = np.clip(yuvimage.u + g, 0, 255) # b = u + g
        self.g = np.clip(g, 0, 255)
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
    
    def initfromyuvsubsampled(self, yuvsubsampled):
        self.y = yuvsubsampled.y.copy()
        self.u = np.empty(self.y.shape)
        self.v = np.empty(self.y.shape)
        self.width, self.height = yuvsubsampled.size()

        if yuvsubsampled.subsampling == (4, 2, 0):
            self.u[::2, ::2] = yuvsubsampled.u[:, :]
            self.u[::2, 1::2] = yuvsubsampled.u[:, :]
            self.u[1::2, ::2] = yuvsubsampled.u[:, :]
            self.u[1::2, 1::2] = yuvsubsampled.u[:, :]
            self.v[::2, ::2] = yuvsubsampled.v[:, :]
            self.v[::2, 1::2] = yuvsubsampled.v[:, :]
            self.v[1::2, ::2] = yuvsubsampled.v[:, :]
            self.v[1::2, 1::2] = yuvsubsampled.v[:, :]

        elif yuvsubsampled.subsampling == (4, 2, 2):
            self.u[:, ::2] = yuvsubsampled.u[:, :]
            self.u[:, 1::2] = yuvsubsampled.u[:, :]
            self.v[:, ::2] = yuvsubsampled.v[:, :]
            self.v[:, 1::2] = yuvsubsampled.v[:, :]
        elif yuvsubsampled.subsampling == (4, 4, 4):
            self.u = yuvsubsampled.u.copy()
            self.v = yuvsubsampled.v.copy()

class yuvsubsampled(image):

    _supportedsubsampling = [(4, 2, 0), (4, 2, 2), (4, 4, 4)]
    def __init__(self, subsampling: tuple = (4, 2, 0)):
        if subsampling not in yuvsubsampled._supportedsubsampling:
            raise ValueError("Unsupported subsampling", subsampling, "supported subsampling: ", yuvsubsampled._supportedsubsampling)

        image.__init__(self)
        self.subsampling = subsampling
        self.y = None
        self.u = None
        self.v = None

    def initfromyuvimage(self, yuvimage):
        self.width, self.height = yuvimage.size()
        self.y = yuvimage.y
        print("subsample:\t\t", self.subsampling)
        if self.subsampling == (4, 2, 0):
            self.u = yuvimage.u[::2, ::2] # keep 1 row in 2 and 1 element in 2 from each row
            self.v = yuvimage.v[::2, ::2]
        elif self.subsampling == (4, 2, 2):
            self.u = yuvimage.u[:, ::2] # keep every row and 1 element in 2 from each row
            self.v = yuvimage.v[:, ::2]
        elif self.subsampling == (4, 4, 4):
            self.u = yuvimage.u
            self.v = yuvimage.v
        else:
            print("This was not supposed to happen...")
    
    def initfromyuvdwted(self, yuvdwted, subsampling):
        originalwidth, originalheight = yuvdwted.size()
        ywidth, yheight, uwidth, uheight, vwidth, vheight = yuvsubsampled._getshape(originalwidth, originalheight, yuvdwted.recursionlevel - 1, subsampling)
        ylxly = yuvdwted.y.reshape(yheight, ywidth)
        ulxly = yuvdwted.u.reshape(uheight, uwidth)
        vlxly = yuvdwted.v.reshape(vheight, vwidth)
        
        for i in reversed(range(yuvdwted.recursionlevel)):
            ywidth, yheight, uwidth, uheight, vwidth, vheight = yuvsubsampled._getshape(originalwidth, originalheight, i, subsampling)
            ylxly = yuvsubsampled._getdwtoriginal(
                ylxly,
                yuvdwted.reconstructiondata[i]["ylxhy"].reshape((yheight, ywidth)),
                yuvdwted.reconstructiondata[i]["yhxly"].reshape((yheight, ywidth)),
                yuvdwted.reconstructiondata[i]["yhxhy"].reshape((yheight, ywidth))
            )
            ulxly = yuvsubsampled._getdwtoriginal(
                ulxly,
                yuvdwted.reconstructiondata[i]["ulxhy"].reshape((uheight, uwidth)),
                yuvdwted.reconstructiondata[i]["uhxly"].reshape((uheight, uwidth)),
                yuvdwted.reconstructiondata[i]["uhxhy"].reshape((uheight, uwidth))
            )
            vlxly = yuvsubsampled._getdwtoriginal(
                vlxly,
                yuvdwted.reconstructiondata[i]["vlxhy"].reshape((vheight, vwidth)),
                yuvdwted.reconstructiondata[i]["vhxly"].reshape((vheight, vwidth)),
                yuvdwted.reconstructiondata[i]["vhxhy"].reshape((vheight, vwidth))
            )
        
        self.y = ylxly
        self.u = ulxly
        self.v = vlxly
        self.subsampling = subsampling
        self.width, self.height = yuvdwted.size()
    
    @staticmethod
    def _getshape(originalwidth, originalheight, recursionlevel, subsampling):
        ywidth = originalwidth / (2**(recursionlevel + 1))
        yheight = originalheight / (2**(recursionlevel + 1))
        
        if subsampling == (4, 2, 0):
            uwidth = vwidth = ywidth / 2
            uheight = vheight = yheight / 2
        elif subsampling == (4, 2, 2):
            uwidth = vwidth = ywidth / 2
            uheight = vheight = yheight
        elif subsampling == (4, 4, 4):
            uwidth = vwidth = ywidth
            uheight = vheight = yheight
        else:
            print("whyyyyy?")
        
        return int(ywidth), int(yheight), int(uwidth), int(uheight), int(vwidth), int(vheight)
    
    @staticmethod
    def _getdwtoriginal(lxly, lxhy, hxly, hxhy):
        height, width = lxly.shape
        # get lx
        lx = np.empty((2 * height, width))
        lx[::2, :] = lxly[:, :] + lxhy[:, :]
        lx[1::2, :] = lxly[:, :] - lxhy[:, :]
        #get hx
        hx = np.empty((2 * height, width))
        hx[::2, :] = hxly[:, :] + hxhy[:, :]
        hx[1::2, :] = hxly[:, :] - hxhy[:, :]
        #get original
        height, width = lx.shape
        original = np.empty((height, 2 * width))
        original[:, ::2] = lx[:, :] + hx[:, :]
        original[:, 1::2] = lx[:, :] - hx[:, :]

        return original

class yuvdwted(image):

    def __init__(self):
        image.__init__(self)
        self.recursionlevel = 1
        self.y = None
        self.u = None
        self.v = None
        self.reconstructiondata = []

    def initfromyuvsubsampled(self, yuvsubsampled, recursionlevel):
        self.width, self.height = yuvsubsampled.size()
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
    
    def initfromqyd(self, qyd):
        self.recursionlevel = qyd.recursionlevel
        self.y = yuvdwted._dequantize(qyd.y, qyd.deadzone, qyd.step)
        self.u = yuvdwted._dequantize(qyd.u, qyd.deadzone, qyd.step)
        self.v = yuvdwted._dequantize(qyd.v, qyd.deadzone, qyd.step)
        self.reconstructiondata = []
        self.width, self.height = qyd.size()
        self.recursionlevel = qyd.recursionlevel
        
        for i in qyd.reconstructiondata:
            self.reconstructiondata.append({
                "ylxhy": yuvdwted._dequantize(i["ylxhy"], qyd.deadzone, qyd.step),
                "yhxly": yuvdwted._dequantize(i["yhxly"], qyd.deadzone, qyd.step),
                "yhxhy": yuvdwted._dequantize(i["yhxhy"], qyd.deadzone, qyd.step),
                "ulxhy": yuvdwted._dequantize(i["ulxhy"], qyd.deadzone, qyd.step),
                "uhxly": yuvdwted._dequantize(i["uhxly"], qyd.deadzone, qyd.step),
                "uhxhy": yuvdwted._dequantize(i["uhxhy"], qyd.deadzone, qyd.step),
                "vlxhy": yuvdwted._dequantize(i["vlxhy"], qyd.deadzone, qyd.step),
                "vhxly": yuvdwted._dequantize(i["vhxly"], qyd.deadzone, qyd.step),
                "vhxhy": yuvdwted._dequantize(i["vhxhy"], qyd.deadzone, qyd.step)
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
    
    @staticmethod
    def _dequantize(vector, deadzone, step):
        return np.array([np.sign(x) * ((deadzone / 2) + (step * (abs(x) - 1 + 0.5))) for x in vector])

class quantizedyuvdwted(image):

    def __init__(self):
        image.__init__(self)
        self.y = None
        self.u = None
        self.v = None
        self.reconstructiondata = []
        self.deadzone = 0
        self.step = 1
        self.recursionlevel = 1
    
    def initfromyuvdwted(self, yuvdwted, deadzone, step):
        self.width, self.height = yuvdwted.size()
        self.y = quantizedyuvdwted._quantize(yuvdwted.y.flatten(), deadzone, step)
        self.u = quantizedyuvdwted._quantize(yuvdwted.u.flatten(), deadzone, step)
        self.v = quantizedyuvdwted._quantize(yuvdwted.v.flatten(), deadzone, step)
        self.deadzone = deadzone
        self.step = step
        self.recursionlevel = yuvdwted.recursionlevel

        for i in yuvdwted.reconstructiondata:
            self.reconstructiondata.append({
                "ylxhy": quantizedyuvdwted._quantize(i["ylxhy"].flatten(), deadzone, step),
                "yhxly": quantizedyuvdwted._quantize(i["yhxly"].flatten(), deadzone, step),
                "yhxhy": quantizedyuvdwted._quantize(i["yhxhy"].flatten(), deadzone, step),
                "ulxhy": quantizedyuvdwted._quantize(i["ulxhy"].flatten(), deadzone, step),
                "uhxly": quantizedyuvdwted._quantize(i["uhxly"].flatten(), deadzone, step),
                "uhxhy": quantizedyuvdwted._quantize(i["uhxhy"].flatten(), deadzone, step),
                "vlxhy": quantizedyuvdwted._quantize(i["vlxhy"].flatten(), deadzone, step),
                "vhxly": quantizedyuvdwted._quantize(i["vhxly"].flatten(), deadzone, step),
                "vhxhy": quantizedyuvdwted._quantize(i["vhxhy"].flatten(), deadzone, step)
            })
    
    @staticmethod
    def _quantize(vector, deadzone, step):
        return np.array([np.sign(x) * max(0, math.floor(((abs(x) - (deadzone / 2)) / step) + 1)) for x in vector])

class qydlzwed(image):

    def __init__(self):
        image.__init__(self)
        self.y = None
        self.ydict = None
        self.u = None
        self.udict = None
        self.v = None
        self.vdict = None
        self.reconstructiondata = []
    
    def initfromqyd(self, qyd):
        self.width, self.height = qyd.size()
        encoded_sizes = []
        self.ydict, self.y, size_y = qydlzwed._encode(qyd.y)
        encoded_sizes.append(size_y)
        self.udict, self.u, size_u = qydlzwed._encode(qyd.u)
        encoded_sizes.append(size_u)
        self.vdict, self.v, size_v = qydlzwed._encode(qyd.v)
        encoded_sizes.append(size_v)

        for i in qyd.reconstructiondata:
            ylxhydict, ylxhy, size_0 = qydlzwed._encode(i["ylxhy"])
            encoded_sizes.append(size_0)
            yhxlydict, yhxly, size_1 = qydlzwed._encode(i["yhxly"])
            encoded_sizes.append(size_1)
            yhxhydict, yhxhy, size_2 = qydlzwed._encode(i["yhxhy"])
            encoded_sizes.append(size_2)
            ulxhydict, ulxhy, size_3 = qydlzwed._encode(i["ulxhy"])
            encoded_sizes.append(size_3)
            uhxlydict, uhxly, size_4 = qydlzwed._encode(i["uhxly"])
            encoded_sizes.append(size_4)
            uhxhydict, uhxhy, size_5 = qydlzwed._encode(i["uhxhy"])
            encoded_sizes.append(size_5)
            vlxhydict, vlxhy, size_6 = qydlzwed._encode(i["vlxhy"])
            encoded_sizes.append(size_6)
            vhxlydict, vhxly, size_7 = qydlzwed._encode(i["vhxly"])
            encoded_sizes.append(size_7)
            vhxhydict, vhxhy, size_8 = qydlzwed._encode(i["vhxhy"])
            encoded_sizes.append(size_8)
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
        total_encoded_size = 0
        for size in encoded_sizes:
            total_encoded_size += size
        print("encoded size:\t", total_encoded_size/1000, " kilobits")
    
    @staticmethod
    def _getinitdict(vector):
        symbols = np.array([], dtype = int)
        
        for symb in vector:
            if int(symb) not in symbols:
                symbols = np.append(symbols, int(symb))
        
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
            subsymbols = str(int(vector[pos]))
            subsymbolsinencdict = str(int(vector[pos]))

            while subsymbols in encdict and pos < vector.size:
                subsymbolsinencdict = subsymbols
                pos += 1
                if pos < vector.size:
                    subsymbols += str(int(vector[pos]))

            encoded = np.append(encoded, encdict[subsymbolsinencdict])

            if pos < vector.size:
                encdict[subsymbols] = "{:b}".format(len(encdict))

                if np.ceil(np.log2(len(encdict))) > len(encoded[-1]):
                    for symb, code in encdict.items():
                        encdict[symb] = code.zfill(int(np.ceil(np.log2(len(encdict)))))
        print(initdict)
        print("nb elem", len(initdict))
        elem_len = len(initdict[(next(iter(initdict)))])
        print("elem len", elem_len)
        size_bit = len(initdict) * len(initdict[(next(iter(initdict)))]) + (len(initdict) * 8)
        print(encoded)
        for code in encoded:
            size_bit += len(code)
        return initdict, encoded, size_bit

class compressedimage(image):
    def __init__(self, imread, yuvsubsamp = (4, 2, 0), dwtrecurslevel = 3, quantizdeadzone = 4, quantizstep = 1):
        print("dwt recursions:\t", dwtrecurslevel)
        print("deadzone:\t\t", quantizdeadzone)
        image.__init__(self)
        self.rgbimage = rgbimage()
        self.yuvimage = yuvimage()
        self.yuvsubsampled = yuvsubsampled(yuvsubsamp)
        self.yuvdwted = yuvdwted()
        self.quantizedyuvdwted = quantizedyuvdwted()
        self.qydlzwed = qydlzwed()

        self.yuvimage.initfromimread(imread)
        self.yuvsubsampled.initfromyuvimage(self.yuvimage)
        self.yuvdwted.initfromyuvsubsampled(self.yuvsubsampled, dwtrecurslevel)
        self.quantizedyuvdwted.initfromyuvdwted(self.yuvdwted, quantizdeadzone, quantizstep)
        self.qydlzwed.initfromqyd(self.quantizedyuvdwted)

    def getprintable(self):
        tmpyuvdwted = yuvdwted()
        tmpyuvdwted.initfromqyd(self.quantizedyuvdwted)
        tmpyuvsubsampled = yuvsubsampled()
        tmpyuvsubsampled.initfromyuvdwted(tmpyuvdwted, self.yuvsubsampled.subsampling)
        tmpyuvimage = yuvimage()
        tmpyuvimage.initfromyuvsubsampled(tmpyuvsubsampled)
        tmprgbimage = rgbimage()
        tmprgbimage.initfromyuvimage(tmpyuvimage)
        printable = tmprgbimage.getprintable()
        return printable
