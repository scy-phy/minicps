"""
protocols.py.

Ethernet/IP (ENIP) is partially supported using cpppo module
https://github.com/pjkundert/cpppo

Modbus/TCP is supported using pymodbus module.
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
            - port: server listening port

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

        pass

    @classmethod
    def _stop_server(cls, address):
        """Stop a protocol server.

        Eg: stop a ENIP server.

        :address: to stop
        """

        pass

    def _send(self, address, what):
        """Send (serve) a value.

        :address: to send
        :what: to send
        """

        pass

    def _receive(self, address, what):
        """Recieve a (requested) value.

        :address: to receive from
        :what: to ask for
        """

        pass


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

    TCP_PORT = 44818
    UDP_PORT = 2222

    def __init__(self, protocol):

        super(EnipProtocol, self).__init__(protocol)

        if self._mode == 0:
            print 'DEBUG: do NOT start a enip server.'
        elif self._mode == 1:
            if self._port != EnipProtocol.TCP_PORT:
                print 'WARNING: not using std enip %d TCP port' % \
                    EnipProtocol.TCP_PORT
        elif self._mode == 2:
            if self._port != EnipProtocol.UDP_PORT:
                print 'WARNING: not using std enip %d UDP port' % \
                    EnipProtocol.UDP_PORT

    @classmethod
    def _start_server(cls, address, values):
        """Start a protocol server.

        Eg: create a ENIP server.

        :address: to serve
        :values: to serve
        """

        pass

    @classmethod
    def _stop_server(cls, address):
        """Stop a protocol server.

        Eg: stop a ENIP server.

        :address: to stop
        """

        pass
