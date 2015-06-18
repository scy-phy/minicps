class Sensor(object):
    """
    The Sensor class has only a float representing the flow level
    """
    def __init__(self, height=0.0):
        self.__height = height

    def height(self):
        return self.__height

    def actualize(self, height):
        self.__height = height
