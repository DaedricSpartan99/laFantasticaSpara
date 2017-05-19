from pygame.locals import *
import math

# Bi-dimensional vector with omogeneous coordinate z

class Vector:   
    def __init__(self, tup):
        self.x = tup[0]
        self.y = tup[1]
        
        if (len(tup) > 2):
            self.z = tup[2]
        else:
            self.z = 1

    def __iter__(self):
        return self.toTuple()

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
        self.setValues(matrixApplication(self, matrix))

def rotate(obj, deg):
    return pygame.transform.rotate(obj, deg * math.pi / 180)

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

# metrics section

ppmMatrix = ((30, 0, 0), (0, -20, 768), (0, 0, 1))

def setPixelTransform(res, perc):
    return # TODO

def toPixels(vector):
    return matrixApplication(vector, ppmMatrix)
