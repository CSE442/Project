#
# file:   car.py
# author: Nathan Burgers
#

from point2d import Point2D

class Car(object):
    def __init__(self, position = Point2D()):
        self.position = position
