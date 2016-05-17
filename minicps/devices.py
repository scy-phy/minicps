"""
devices.py
"""

import time

from os.path import splitext
from minicps.state import SQLiteState, RedisState


class Device(object):

    """Base class."""

    # TODO: state dict convention (eg: multiple table support?)
    def __init__(self, name, protocol, state, disk={}, memory={}):
        """PLC1 initialization steps:

        :name: name
        :protocol: used for network emulation
        :state: dict containing 'path' and 'name'
        :disk: persistent memory
        :memory: main memory
        """

        self.name = name
        self.state = state
        self.protocol = protocol
        self.memory = memory
        self.disk = disk

        # TODO: good idea to attach to another function?
        # TDOD: what happend with self?

        # TODO: add protocol bindings

        self._init_state()
        self._init_protocol()
        self._start()

    def _init_state(self):
        """Bind device to the physical layer API."""

        subpath, extension = splitext(self.state['path'])
        print 'DEBUG subpath: ', subpath
        print 'DEBUG extension: ', extension

        if not extension:
            print 'ERROR: provide a path with extension'

        if not self.state['path']:
            print 'ERROR: provide a state path'

        if not self.state['name']:
            print 'ERROR: provide a state name'

        if extension == '.sqlite':
            # TODO: add parametric value filed
            print 'DEBUG state: ', self.state
            self._state = SQLiteState(self.state)
        elif extension == '.redis':
            # TODO: add parametric key serialization
            self._state = RedisState(self.state)
        else:
            print 'ERROR: %s backend not supported.' % self.state

    def _init_protocol(self):
        """Bind device to network API."""

        # TODO: implement
        pass

        print "_init_protocol: please override me"

    def _start(self):
        """Start a device."""

        print "_start: please override me"

    def _stop(self):
        """Start a device."""

        print "_stop: please override me"

    def set(self, what, value):
        """Get a value."""

        self._state._set(what, value)

    def get(self, what):
        """Get a value."""

        # print 'DEBUG device.get what: ', what
        return self._state._get(what)


class PLC(Device):

    """Programmable Logic Controller.

    PLC has control, monitor and network capabilites.

    Usually they run a pre-loop initialization routine and then they enter a
    main loop.
    """

    def _start(self):

        self.pre_loop()
        self.main_loop()

    # TODO
    def _stop(self):

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
