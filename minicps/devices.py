"""
devices.py

This module contains:
    - the bindings to the physical layer API
    - the bindings to the network API (mininet)
    - the user input validation code

Any device can be initialized with any couple of (state, protocol)
dictionaries. The consistency of the system should be guaranteed by the
client, e.g., do NOT init two different PLCs referencing to two different
states or speaking two different protocols.

Device subclasses can be customized overriding the _start and _stop methods.
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
        self._stop()

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
                raise KeyError('State must contain 2 keys.')
            else:
                for key in state_keys:
                    if (key != 'path') and (key != 'name'):
                        raise KeyError('%s is an invalid key.' % key)
            state_values = state.values()
            for val in state_values:
                if type(val) is not str:
                    raise TypeError('state values must be strings.')
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
        if type(protocol) is not dict:
            if protocol is not None:
                raise TypeError('Protocol must be either None or a dict.')
        else:
            protocol_keys = protocol.keys()
            if (not protocol_keys) or (len(protocol_keys) != 3):
                raise KeyError('Protocol must contain 3 keys.')
            else:
                for key in protocol_keys:
                    if ((key != 'name') and
                            (key != 'mode') and
                            (key != 'server')):
                        raise KeyError('%s is an invalid key.' % key)

            # protocol['name']
            if type(protocol['name']) is not str:
                raise TypeError('Protocol name must be a string.')
            else:
                name = protocol['name']
                if (name != 'enip'):
                    raise ValueError('%s protocol not supported.' % protocol)
            # protocol['mode']
            if type(protocol['mode']) is not int:
                raise TypeError('Protocol mode must be a int.')
            else:
                mode = protocol['mode']
                if (mode < 0):
                    raise ValueError('Protocol mode must be positive.')
            # protocol['server'] TODO
            # protocol['client'] TODO after adding it to the API

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

        if self.protocol is None:
            print 'DEBUG: %s has no networking capabilities.' % self.name
            pass
        else:
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

    def set(self, what, value):
        """Set (write) a state value.

        :what: tuple with field identifiers
        :value: value

        :returns: setted value
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._state._set(what, value)

    def get(self, what):
        """Get (read) a state value.

        :what: (Immutable) tuple with field identifiers

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
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._protocol._send(what, value, address)

    def recieve(self, what, address):
        """Receive a (requested) value.

        :what: to ask for
        :address: to receive from
        """

        if type(what) is not tuple:
            raise TypeError('Parameter must be a tuple.')
        else:
            return self._protocol._receive(what, address)


# TODO: rename pre_loop and main_loop?
class PLC(Device):

    """Programmable Logic Controller.

    PLC has control, monitor and network capabilities.

    Usually they run a pre-loop initialization routine and then they enter a
    main loop.
    """

    def _start(self):

        self.pre_loop()
        self.main_loop()

    def _stop(self):

        if self.protocol['mode'] > 0:
            self._protocol._server_subprocess.kill()

    def pre_loop(self, sleep=0.5):
        """PLC boot process.

        :sleep: sleep n sec after it
        """

        print "TODO PLC pre_loop: please override me"
        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        """PLC main loop.

        :sleep: sleep n sec after each iteration
        """

        sec = 0
        while(sec < 1):

            print "TODO PLC main_loop: please override me"
            time.sleep(sleep)

            sec += 1


# TODO: add show something
class HMI(Device):

    """Human Machine Interface.

    HMI has monitor and network capabilities.
    """

    def _start(self):

        self.main_loop()

    def _stop(self):

        if self.protocol['mode'] > 0:
            self._protocol._server_subprocess.kill()

    def main_loop(self, sleep=0.5):
        """HMI main loop.

        :sleep: sleep n sec after each iteration
        """

        sec = 0
        while(sec < 1):

            print "TODO HMI main_loop: please override me"
            time.sleep(sleep)

            sec += 1


class Tank(Device):

    """Tank.

    Tank has:
        - state capabilities
        - no memory
        - no disk
        - no networking capabilities
    """

    def __init__(
            self, name, protocol, state,
            section, level):
        """
        :section: cross section of the tank in m^2
        :level: current level in m

        Eg: inflows = [[True, 2.5], [False, 3.3]]
        """

        self.section = section
        self.level = level
        super(Tank, self).__init__(name, protocol, state)

    def _start(self):

        self.pre_loop()
        self.main_loop()

    def pre_loop(self, sleep=0.5):
        """Tank pre_loop."""

        print "TODO Tank pre_loop: please override me"

    def main_loop(self, sleep=0.5):
        """Tank main loop.

        :sleep: sleep n sec after each iteration
        """

        sec = 0
        while(sec < 1):

            print "TODO Tank main_loop: please override me"
            time.sleep(sleep)

            sec += 1
