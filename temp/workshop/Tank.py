import math
import Sensor
import Pump
from Utils import GRAVITATION

class Tank(object):

    HH_LVL = 1600.0
    H_LVL = 1000.0
    L_LVL = 500.0
    LL_LVL = 0.0

    def __init__(self, diameter=1.0):
        self.__diameter = diameter

    def speed_to_height(self, speed, diameter):
        return speed * math.pow((diameter / 2),2) / math.pow((self.__diameter / 2),2)

    def out_flow_speed(self, pump, sensor):
        """
        Toricelli formula
        """
        return math.sqrt(2 * GRAVITATION * (sensor.height() - pump.height()))

    def tank_flow(self, in_pumps, out_pumps, sensor, timer):
        h = sensor.height()
        for in_pump in in_pumps:
            if(in_pump.is_open()):
                h += timer * self.speed_to_height(in_pump.speed(), in_pump.diameter())
        for out_pump in out_pumps:
            if(out_pump.is_open()):
                h -= timer * self.speed_to_height(out_pump.speed(), out_pump.diameter())
        return h
