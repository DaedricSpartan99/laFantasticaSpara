from pygame.locals import *
import math

# Bi-dimensional vector with omogeneous coordinate z

class Vector:
    def __init__(self, tup = (0, 0)):
        self.x = tup[0]
        self.y = tup[1]

    def null(self):
        self.x = 0
        self.y = 0

    def unit(self):
        mod = self.mod()
        self.x /= mod
        self.y /= mod

    def tuple(self):
        return (self.x, self.y)

    def __iter__(self):
        return self.tuple()

    def __getitem__(self, key):
        if (key == 0):
            return self.x
        elif (key == 1):
            return self.y
        else:
            return 0

    def __mul__(self, num):
        return Vector((self.x * num, self.y * num))

    def __truediv__(self, num):
        return Vector((self.x / num, self.y / num))

    def __floordiv__(self, num):
        return Vector((self.x // num, self.y // num))

    def __rmul__(self, num):
        return Vector((self.x * num, self.y * num))

    def __rtruediv__(self, num):
        return Vector((self.x / num, self.y / num))

    def __rfloordiv__(self, num):
        return Vector((self.x // num, self.y // num))

    def __imul__(self, num):
        self.x *= num
        self.y *= num
        return self
        
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __itruediv__(self, num):
        self.x /= num
        self.y /= num
        return self

    def __ifloordiv__(self, num):
        self.x //= num
        self.y //= num
        return self

    def __xor__(self, other):
        return self.x * other.y - self.y * other.x
    
    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def mod(self):
        return math.sqrt(self.sqmod())

    def sqmod(self):
        return self.x**2 + self.y**2



class Vector3d:   
    def __init__(self, tup):
        self.x = tup[0]
        self.y = tup[1]
        
        if (len(tup) > 2):
            self.z = tup[2]
        else:
            self.z = 1

    def __iter__(self):
        return self.tuple()

    def __getitem__(self, key):
        if (key == 0):
            return self.x
        elif (key == 1):
            return self.y
        elif (key == 2):
            return self.z
        else:
            return 0

    def setValues(self, tup):
        self.x = tup[0]
        self.y = tup[1]
        
        if (len(tup) > 2):
            self.z = tup[2]
        else:
            self.z = 1

    def tuple(self):
        return (self.x, self.y, self.z)

    def array(self):
        return [self.x, self.y, self.z]

    def applyMatrix(self, matrix):
        return matrixApplication(self, matrix)

    def null(self):
        self.x = 0
        self.y = 0
        self.z = 0
        
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __xor__(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)
    
    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y, self.z - other.z))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.z != other.z

    def mod(self):
        return math.sqrt(self.sqmod())

    def sqmod(self):
        return self.x**2 + self.y**2 + self.z**2

null = Vector((0, 0))
null3d = Vector3d((0, 0, 0))

def rotate(obj, deg):
    return pygame.transform.rotate(obj, deg * math.pi / 180)

class Coords:
    def __init__(self, origin, ratio):
        self.origin = origin
        self.ratio = ratio

def get_px(v, coords):
    x = int(v[0] * coords.ratio[0]) + coords.origin[0]
    y = - int(v[1] * coords.ratio[1]) + coords.origin[1]
    return (x, y)

def get_vector(px, coords):
    x = float(px[0] - coords.origin[0]) / coords.ratio[0]
    y = - float(px[1] - coords.origin[1]) / coords.ratio[1]
    return Vector((x, y))

def degrees(rad):
    return rad * 180.0 / math.pi

def radians(deg):
    return deg * math.pi / 180.0

def matrixApplication(vector, matrix):  # returns an Array
    out = [0, 0, 0]
    i = 0
    for row in matrix:
        j = 0
        for col in row:
            out[i] += vector[j] * col
            j += 1
        i += 1
    return out
