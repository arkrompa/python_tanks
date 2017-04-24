import math
from PyQt5 import QtCore, QtGui
from constants import *


class Hexagon:
    def __init__(self, x, y, color_key):
        self.center = QtCore.QPointF(x, y)
        self.hex_polygon = self.createPolygon(HEX_SIZE)
        self.color_key = color_key

    def createPolygon(self, size):
        hex_polygon = QtGui.QPolygonF()
        for i in range(6):
            angle_deg = 60 * i + 30
            angle_rad = math.pi / 180 * angle_deg
            hex_polygon.append(QtCore.QPointF(self.center.x() + size * math.cos(angle_rad),
                                              self.center.y() + size * math.sin(angle_rad)))
        return hex_polygon

    def getColor(self):
        return COLOR_DICT.get(self.color_key)

    def getRiflePolygon(self, i):
        hex_polygon = QtGui.QPolygonF()
        hex_polygon.append(self.hex_polygon[-i])
        hex_polygon.append(self.hex_polygon[-i + 1])
        hex_polygon.append(self.center)
        return hex_polygon
