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

        self.start()

    def start(self):
        """Start a device."""

        print "start: please override me"

    def stop(self):
        """Start a device."""

        print "stop: please override me"


class PLC(Device):

    """Programmable Logic Controller.

    PLC has control, monitor and network capabilites.

    Usually they run a pre-loop initialization routine and then they enter a
    main loop.
    """

    def start(self):

        self.pre_loop()
        self.main_loop()

    # TODO
    def stop(self):

        pass

    def pre_loop(self, sleep=0.5):
        """PLC boot process.

        :sleep: sleep n sec after it
        """

        print "pre_loop: please override me"
        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        """PLC main loop.

        :sleep: sleep n sec after each iteration
        """

        sec = 0
        while(sec < 1):

            print "main_loop: please override me"
            time.sleep(sleep)

            sec += 1
