
class Color(object):
    red = QColor(Qt.red)
    blue = QColor(Qt.blue)
    yellow = QColor(Qt.yellow)
    black = QColor(Qt.black)
    green = QColor(Qt.green)
    gray=QColor(Qt.gray)

class Shape(object):
    sqaure=0
    circle=1
    triangle=2
    cross=3

import itertools
class Mark(object):
    colors=[Color.red, Color.black, Color.blue, Color.yellow, Color.green, Color.gray]
    shapes=[Shape.sqaure, Shape.circle, Shape.triangle, Shape.cross]
    marks=[]
    for x in itertools.product(shapes, colors):
        marks.append(x)
    def printMakrs(self):
        for m in self.marks:
            print(m)
