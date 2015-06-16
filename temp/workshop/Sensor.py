class Sensor(object):

    def __init__(self, height=0.0):
        self.__height = height

    def height(self):
        return self.__height

    def actualize(self, height):
        self.__height = height
