class Pump(object):

    def __init__(self, speed=42.0, diameter=0.8, height = 0.0):
        self.__open = False
        self.__speed = speed
        self.__diameter = diameter
        self.__height = height

    def open(self):
        self.__open = True

    def close(self):
        self.__open = False

    def change_speed(self, speed):
        self.__speed = speed

    def is_open(self):
        return self.__open

    def speed(self):
        return self.__speed

    def diameter(self):
        return self.__diameter

    def height(self):
        return self.__height
