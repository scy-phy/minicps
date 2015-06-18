from Utils import GRAVITATION # 9.81 m.s^-2
import math
import Pump
import Sensor

class Tank(object):
    """
    Tank is a class designed to simulates water flow in a tank
    It uses Toricelli formula, based on the Bernoulli one
    """
    # Class constants simulating the different levels for the sensors
    HH_LVL = 1600.0
    H_LVL = 1000.0
    L_LVL = 500.0
    LL_LVL = 0.0

    def __init__(self, diameter=1.0):
        self.__diameter = diameter

    def speed_to_height(self, speed, diameter):
        """
        Converts the speed of a flow considering the diameter of the hole
        into a heigh of water in the tank according to its diameter
        """
        return speed * math.pow((diameter / 2),2) / math.pow((self.__diameter / 2),2)

    def out_flow_speed(self, pump, sensor):
        """
        Toricelli formula, which gives the speed of the flow according ot the flow level in the tank,
        considering the speed as a constant in the Bernoulli formula
        """
        return math.sqrt(2 * GRAVITATION * (sensor.height() - pump.height()))

    def tank_flow(self, in_pumps, out_pumps, sensor, timer):
        """
        Computes the new flow level depending on
        The flow level
        The incoming flows
        The outgoing flows
        The flow discharge time in seconds 
        """
        h = sensor.height()
        for in_pump in in_pumps:
            if(in_pump.is_open()):
                h += timer * self.speed_to_height(in_pump.speed(), in_pump.diameter())
        for out_pump in out_pumps:
            if(out_pump.is_open()):
                h -= timer * self.speed_to_height(self.out_flow_speed(out_pump, sensor), out_pump.diameter()) # out_pump.speed()
        return h
