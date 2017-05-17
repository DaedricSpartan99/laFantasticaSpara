from pygame.locals import *
import math

class Vector:
    def __init__(self, tup):
        self.x = tup[0]
        self.y = tup[1]

    def __iter__(self):
        return self.tuple()

    def tuple(self):
        return (self.x, self.y)

    def array(self):
        return [self.x, self.y]

def rotate(obj, deg):
    return pygame.transform.rotate(obj, deg * math.pi / 180)
