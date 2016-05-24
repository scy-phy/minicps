"""
devices.py
"""

import time

from os.path import splitext
from minicps.state import SQLiteState, RedisState
from minicps.protocols import EnipProtocol


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

        self._validate_inputs(name, protocol, state, disk, memory)

        self.name = name
        self.state = state
        self.protocol = protocol
        self.memory = memory
        self.disk = disk

        self._init_state()
        self._init_protocol()
        self._start()

    # TODO: validate protocol dict
    def _validate_inputs(self, name, protocol, state, disk, memory):

        # name string
        if type(name) is not str:
            raise TypeError('Name must be a string.')
        elif not name:
            raise ValueError('Name string cannot be empty.')

        # state dict
        if type(state) is not dict:
            raise TypeError('State must be a dict.')
        else:
            state_keys = state.keys()
            if (not state_keys) or (len(state_keys) != 2):
                raise KeyError('Dict must contain 2 keys.')
            else:
                for key in state_keys:
                    if (key != 'path') and (key != 'name'):
                        raise KeyError('%s is an invalid key.' % key)
            state_values = state.values()
            for val in state_values:
                if type(val) is not str:
                    raise TypeError('Value must be a string.')
            # state['path']
            subpath, extension = splitext(state['path'])
            # print 'DEBUG subpath: ', subpath
            # print 'DEBUG extension: ', extension
            if (extension != '.redis') and (extension != '.sqlite'):
                raise ValueError('%s extension not supported.' % extension)
            # state['name']
            if type(state['name']) is not str:
                raise TypeError('State name must be a string.')

        # protocol
        # TODO

    def _init_state(self):
        """Bind device to the physical layer API."""

        subpath, extension = splitext(self.state['path'])

        if extension == '.sqlite':
            # TODO: add parametric value filed
            # print 'DEBUG state: ', self.state
            self._state = SQLiteState(self.state)
        elif extension == '.redis':
            # TODO: add parametric key serialization
            self._state = RedisState(self.state)
        else:
            print 'ERROR: %s backend not supported.' % self.state

    def _init_protocol(self):
        """Bind device to network API."""

        name = self.protocol['name']

        if name == 'enip':
            self._protocol = EnipProtocol(self.protocol)
        else:
            print 'ERROR: %s protocol not supported.' % self.protocol

    def _start(self):
        """Start a device."""

        print "TODO _start: please override me"

    def _stop(self):
        """Start a device."""

        print "TODO _stop: please override me"

    # TODO: add what doc
    def set(self, what, value):
        """Set a value.

        :returns: setted value
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._state._set(what, value)

    # TODO: add what doc
    def get(self, what):
        """Get a value.

        :returns: get value
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._state._get(what)

    def send(self, what, value, address):
        """Send (serve) a value.

        :what: tuple addressing what
        :value: sent
        :address: ip[:port]

        :returns: sent value
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._protocol._send(what, value, address)

    def recieve(self, what, address):
        """Recieve a (requested) value.

        :what: to ask for
        :address: to receive from

        :returns: sent value
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._protocol._receive(what, address)


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

        print "TODO pre_loop: please override me"
        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        """PLC main loop.

        :sleep: sleep n sec after each iteration
        """

        sec = 0
        while(sec < 1):

            print "TODO main_loop: please override me"
            time.sleep(sleep)

            sec += 1
