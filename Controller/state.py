#
# file:   state.py
# author: Nathan Burgers
#

from car import Car

class State(object):
    def __init__(self, cars = [Car(), Car()]):
        self.cars = cars
