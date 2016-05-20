"""
protocols.py.

Ethernet/IP (ENIP) is partially supported using cpppo module
https://github.com/pjkundert/cpppo

Modbus/TCP is supported using pymodbus module.
"""

# import cpppo
# import pymodbus

# ENIP {{{1
ENIP_MISC = {
    'tcp_port': 44818,
    'udp_port': 2222,
}


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
    def _start_server(cls, where, values):
        """Start a protocol server.

        Eg: create a ENIP server.

        :where: to serve
        :values: to serve
        """

        pass

    @classmethod
    def _stop_server(cls, where):
        """Stop a protocol server.

        Eg: stop a ENIP server.

        :where: to stop
        """

        pass

    def _send(self, where, what):
        """Send (serve) a value.

        :where: to send
        :what: to send
        """

        pass

    def _receive(self, what):
        """Recieve a (requested) value.

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

    def __init__(self, protocol):

        super(EnipProtocol, self).__init__(protocol)

        # TODO: maybe add some enip specific stuff
        if protocol['mode'] == 0:
            pass  # do not start a server
        elif protocol['mode'] == 1:
            print 'TODO: decide mode 1'
        elif protocol['mode'] == 2:
            print 'TODO: decide mode 2'
