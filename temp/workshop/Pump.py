class Pump(object):
    """
    The Pump class describes a pump used to fill a tank
    It as attributes as a flow speed, a diameter and a height from the ground of the tank
    It also has two states: open and closed
    """
    def __init__(self, speed=42.0, diameter=0.8, height = 0.0):
        self.__open = False
        self.__speed = speed
        self.__diameter = diameter
        self.__height = height

    def open(self):
        """
        Opens the pump
        """
        self.__open = True

    def close(self):
        """
        Closes the pump
        """
        self.__open = False

    def change_speed(self, speed):
        """
        Sets the speed of the pump, so it can have a variable flow
        """
        self.__speed = speed

    def is_open(self):
        """
        To know if the pump is open
        """
        return self.__open

    def speed(self):
        """
        Get the speed
        """
        return self.__speed

    def diameter(self):
        """
        Get the diameter
        """
        return self.__diameter

    def height(self):
        """
        Get the height
        """
        return self.__height
