"""
protocols.py.

Addresses are passed as string containing an optional port,
eg: localhost[:44818].

A Protocol instance can be used both as a client and a server.
The server dictionary contains the static options to configure the running
server. No client information are stored because the public API allows the
query different hosts at different addresses in the same CPS network.
The mode integer indicates whether the client wants to use the Protocol
instance as a client (mode = 0 ) or client and server (mode > 1). Different
positive modes indicates different server configurations eg: enip tcp server
(mode = 1) vs enip udp server (mode = 2).


Ethernet/IP (ENIP) is partially supported using cpppo module.
https://github.com/pjkundert/cpppo

Modbus/TCP is supported using pymodbus module.
https://github.com/bashwork/pymodbus
"""

import sys
import shlex
import subprocess

import cpppo
# import pymodbus


# PROTOCOLS {{{1
class Protocol(object):

    """Base class.

    Ideally different objects can be attached to the same Device class
    to support multi-protocol CPS.
    """

    # TODO: what if the server supports multiple protocols with different ports
    def __init__(self, protocol):
        """Init a State object.

        protocol fields:

            - name: textual identifier
            - mode: int coding mode eg: 1 = modbus synch TCP
            - server: dict containing server settings, empty if mode = 0

        :protocol: validated dict passed from Device obj
        """

        # https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
        # TODO: update
        self._name = protocol['name']
        self._mode = protocol['mode']
        self._server = protocol['server']

    @classmethod
    def _start_server(cls, address, values):
        """Start a protocol server.

        Eg: create a ENIP server.

        :address: to serve
        :values: to serve
        """

        print '_start_server: please override me.'

    @classmethod
    def _stop_server(cls, address):
        """Stop a protocol server.

        Eg: stop a ENIP server.

        :address: to stop
        """

        print '_stop_server: please override me.'

    def _send(self, what, address):
        """Send (serve) a value.

        :what: to send
        :address: to receive from
        """

        print '_send: please override me.'

    def _receive(self, what, address):
        """Recieve a (requested) value.

        :address: to receive from
        :what: to ask for
        """

        print '_receive: please override me.'


class EnipProtocol(Protocol):

    """EnipProtocol manager.

    EnipProtocol manages python cpppo library, Look at the original
    documentation for more information.

    Supported tags:
        - SINT (8-bit)
        - INT (16-bit)
        - DINT (32-bit)
        - REAL (32-bit float)
        - BOOL (8-bit, bit #0)
        - SSTRING (simple string)
    """

    # server ports
    TCP_PORT = '44818'
    UDP_PORT = '2222'

    def __init__(self, protocol):

        super(EnipProtocol, self).__init__(protocol)

        if self._mode == 0:
            print 'DEBUG: do NOT start a enip server.'

        elif self._mode == 1:
            if not self._server['address'].endswith(EnipProtocol.TCP_PORT):
                print 'WARNING: not using std enip %d TCP port' % \
                    EnipProtocol.TCP_PORT

            # TODO: start TCP enip server

        elif self._mode == 2:
            if not self._server['address'].endswith(EnipProtocol.UDP_PORT):
                print 'WARNING: not using std enip %d UDP port' % \
                    EnipProtocol.UDP_PORT

            # TODO: start UDP enip server

    # TODO: how to start a UDP cpppo server?
    # TODO: parametric PRINT_STDOUT and others
    @classmethod
    def _start_server_cmd(
        cls,
        address='localhost:44818',
        tags=(
            ('SENSOR1', 'INT'), ('ACTUATOR1', 'INT'))):
        """Build a Popen cmd string for cpppo server.

        Tags can be any tuple of tuples. Each tuple has to contain a set of
        string-convertible fields, the last one has to be a string containing
        a supported datatype. The current serializer is : (colon).

        Consistency between enip server key-values and state key-values has to
        be guaranteed by the client.

        :address: to serve
        :tags: to serve
        :returns: cmd string passable to Popen object
        """

        # TCP_PORT = '44818'
        # UDP_PORT = '2222'
        CMD = sys.executable + ' -m cpppo.server.enip '
        PRINT_STDOUT = '--print '
        HTTP = '--web %s:80 ' % address[0:address.find(':')]
        # print 'DEBUG: enip _start_server_cmd HTTP: ', HTTP
        ADDRESS = '--address ' + address + ' '

        # cpppo API: 'SENSOR1=INT SENSOR2=REAL ACTUATOR1=INT '
        TAGS = ''
        SERIALIZER = ':'  # consistent with redis hints
        # SERIALIZER = '|'
        for tag in tags:
            TAGS += str(tag[0])
            for field in tag[1:-1]:
                TAGS += SERIALIZER
                TAGS += str(tag[field])

            TAGS += '='
            TAGS += str(tag[-1])
            TAGS += ' '
        print 'DEBUG enip server TAGS: ', TAGS

        if sys.platform.startswith('linux'):
            SHELL = '/bin/bash -c '
            LOG = '--log logs/protocol_tests_enip_server '
        else:
            raise OSError

        cmd = shlex.split(
            CMD +
            PRINT_STDOUT +
            LOG +
            ADDRESS +
            TAGS
        )
        print 'DEBUG enip server cmd: ', cmd

        return cmd

    @classmethod
    def _start_server(cls, address, tags):
        """Start a cpppo enip server.

        Notice that the client has to manage the new process,
        eg:kill it after use.

        :address: to serve
        :tags: to serve
        """

        try:
            cmd = EnipProtocol._start_server_cmd(address, tags)
            server = subprocess.Popen(cmd, shell=False)
            server.wait()

        except Exception as error:
            print 'ERROR enip _start_server: ', error

    @classmethod
    def _stop_server(cls, server):
        """Stop an enip server.

        :server: Popen object
        """

        try:
            server.kill()
        except Exception as error:
            print 'ERROR stop enip server: ', error

    def _send(self, what, address):
        """Send (serve) a value.

        :what: to send
        :address: to receive from
        """

        print '_send: please override me.'

    def _receive(self, what, address):
        """Recieve a (requested) value.

        :address: to receive from
        :what: to ask for
        """

        print '_receive: please override me.'
