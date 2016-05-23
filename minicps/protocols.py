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
            - server: dict containing server settings

        :protocol: validated dict passed from Device obj
        """

        # https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
        self._name = protocol['name']
        self._mode = protocol['mode']
        self._port = protocol['port']

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

    SERVER_TCP_PORT = 44818
    SERVER_UDP_PORT = 2222

    def __init__(self, protocol):

        super(EnipProtocol, self).__init__(protocol)

        if self._mode == 0:
            print 'DEBUG: do NOT start a enip server.'

        elif self._mode == 1:
            if self._port != EnipProtocol.SERVER_TCP_PORT:
                print 'WARNING: not using std enip %d TCP port' % \
                    EnipProtocol.SERVER_TCP_PORT

            # TODO: start TCP enip server

        elif self._mode == 2:
            if self._port != EnipProtocol.SERVER_UDP_PORT:
                print 'WARNING: not using std enip %d UDP port' % \
                    EnipProtocol.SERVER_UDP_PORT

            # TODO: start UDP enip server

    # TODO: how to start a UDP cpppo server?
    @classmethod
    def _start_server(
        cls,
        address='localhost',
        port=44818,
        values=(
            ('SENSOR1', 'INT'), ('ACTUATOR1', 'INT'))):
        """Start an enip server.

        :address: to serve
        :values: to serve
        """

        TCP_PORT = 44818
        UDP_PORT = 2222
        CMD = sys.executable + ' -m cpppo.server.enip '
        PRINT_STDOUT = '--print '
        HTTP = '--web %s:80 ' % address
        ADDRESS = '--address ' + address + ':' + str(port) + ' '

        # TAGS = 'SENSOR1=INT SENSOR2=REAL ACTUATOR1=INT '
        TAGS = ''
        for tag in values:
            TAGS += tag[0]
            TAGS += '='
            TAGS += tag[1]
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

        try:
            server = subprocess.Popen(cmd, shell=False)
            # TODO: add initial value loading capability
            server.wait()
        except Exception as error:
            print 'ERROR enip server: ', error
            server.kill()

    @classmethod
    def _stop_server(cls, address):
        """Stop an enip server.

        :address: to stop
        """

        pass
