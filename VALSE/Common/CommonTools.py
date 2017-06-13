from enum import Enum
from PyQt5.Qt import *
from PyQt5.QtCore import *

class Color(Enum):
    red = 0
    blue = 1
    yellow = 2
    black = 3
    green = 4
    gray=5
    
colors=[QColor(Qt.red), QColor(Qt.blue), QColor(Qt.yellow), QColor(Qt.black), QColor(Qt.green), QColor(Qt.gray)]
# color selection items whose content same with colors
colorItems=['Red','Blue','Yellow','Black','Green','Gray']

class Shape(Enum):
    square=0
    circle=1
    triangle=2
    cross=3
    
shapes=[Shape.square, Shape.circle, Shape.triangle, Shape.cross]
# shape select items whose content same with shapes
shapeItems=['Square','Circle','Triangle','Cross']

import itertools
class Mark(object):
    colors=[Color.red, Color.black, Color.blue, Color.yellow, Color.green, Color.gray]
    shapes=[Shape.square, Shape.circle, Shape.triangle, Shape.cross]
    marks=[]
    for x in itertools.product(shapes, colors):
        marks.append(x)
    def printMakrs(self):
        for m in self.marks:
            print(m)

#class Marker(object):
#    shape=Shape.shapes(0)
#    color=Color.colors(0)
