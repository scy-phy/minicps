"""
devices.py
"""

import time


class Device(object):

    """Base class"""

    # TODO: state good name?
    def __init__(self, name, protocol, state, disk={}, memory={}):
        """PLC1 initialization steps:

        :name: name
        :protocol: database backend
        :state: database backend
        :disk: persistent memory
        :memory: main memory
        """

        self.name = name
        self.state = state
        self.protocol = protocol
        self.memory = memory
        self.disk = disk
