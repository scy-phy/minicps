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

Ethernet/IP (ENIP) is partially supported using cpppo module:
https://github.com/pjkundert/cpppo

Modbus/TCP is supported using pymodbus module:
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

    _SERIALIZER = ':'

    # TODO: what if the server supports multiple protocols with different ports
    def __init__(self, protocol):
        """Init a State object.

        protocol fields:

            - name: textual identifier
            - mode: int coding mode eg: 1 = modbus synch TCP
            - server: dict containing server settings, empty if mode = 0

        :protocol: validated dict passed from Device obj
        """

        # TODO: add client dictionary
        self._name = protocol['name']
        self._mode = protocol['mode']

        if self._mode > 0:
            # TODO: update server dict field: log
            self._server = protocol['server']
        else:
            self._server = {}

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
        """Receive a (requested) value.

        :address: to receive from
        :what: to ask for
        """

        print '_receive: please override me.'

    def _send_multiple(self, what, address):
        """Send (serve) multiple values.

        :address: to receive from
        :what: to ask for
        """

        print '_send_multiple: please override me.'


# TODO:  support vectorial tags def, read and write
# def:   SCADA[0-3]=INT
# write: SCADA[0-3]=1,2,3,4
# read:  SCADA[0-3]
class EnipProtocol(Protocol):

    """EnipProtocol manager.

    EnipProtocol manages python cpppo library, Look at the original
    documentation for more information.

    Tags are passed as a tuple of tuples, if the tuple contains only 1 tag
    remember to put an ending comma, otherwise python will interpret the data
    as a tuple and not as a tuple of tuples.

        eg: tag = (('SENSOR1'), )

    Supported tag datatypes:
        - SINT (8-bit)
        - INT (16-bit)
        - DINT (32-bit)
        - REAL (32-bit float)
        - BOOL (8-bit, bit #0)
        - SSTRING (simple string)
    """

    # server ports
    _TCP_PORT = ':44818'
    _UDP_PORT = ':2222'

    def __init__(self, protocol):

        super(EnipProtocol, self).__init__(protocol)

        self._client_cmd = sys.executable + ' -m cpppo.server.enip.client '

        if sys.platform.startswith('linux'):
            self._client_log = 'logs/enip_client '
        else:
            raise OSError

        # tcp enip server
        if self._mode == 1:
            print 'DEBUG EnipProtocol server addr: ', self._server['address']
            if self._server['address'].find(':') == -1:
                print 'DEBUG: concatenating server address with default port.'
                self._server['address'] += EnipProtocol._TCP_PORT

            elif not self._server['address'].endswith(EnipProtocol._TCP_PORT):
                print 'WARNING: not using std enip %s TCP port' % \
                    EnipProtocol._TCP_PORT

            self._server_cmd = sys.executable + ' -m cpppo.server.enip '

            if sys.platform.startswith('linux'):
                self._server_log = 'logs/enip_tcp_server '
            else:
                raise OSError

            cmd = EnipProtocol._start_server_cmd(
                address=self._server['address'],
                tags=self._server['tags'])

            self._server_subprocess = subprocess.Popen(cmd, shell=False)

        # udp enip server
        elif self._mode == 2:
            print 'DEBUG EnipProtocol server addr: ', self._server['address']
            if self._server['address'].find(':') == -1:
                print 'DEBUG: concatenating server address with default port.'
                self._server['address'] += EnipProtocol._UDP_PORT

            elif not self._server['address'].endswith(EnipProtocol._UDP_PORT):
                print 'WARNING: not using std enip %s UDP port' % \
                    EnipProtocol._UDP_PORT
            # TODO: add --udp flag
            self._server_cmd = sys.executable + ' -m cpppo.server.enip '
            if sys.platform.startswith('linux'):
                self._server_log = 'logs/enip_udp_server '
            else:
                raise OSError

            # TODO: start UDP enip server

    @classmethod
    def _tuple_to_cpppo_tag(cls, what, value=None, serializer=':'):
        """Returns a cpppo string to read/write a server.

        Can be used both to generate cpppo scalar read query, like
        SENSOR1:1, and scalar write query, like ACTUATOR1=1.
        """

        tag_string = ' '
        tag_string += str(what[0])

        if len(what) > 1:
            for field in what[1:]:
                tag_string += EnipProtocol._SERIALIZER
                tag_string += str(field)
        if value:
            tag_string += '='
            tag_string += str(value)
        # print 'DEBUG _tuple_to_cpppo_tag tag_string: ', tag_string

        return tag_string

    @classmethod
    def _tuple_to_cpppo_tags(cls, tags, serializer=':'):
        """Returns a cpppo tags string to init a server.

        cpppo API: SENSOR1=INT SENSOR2=REAL ACTUATOR1=INT
        """

        tags_string = ''
        for tag in tags:
            tags_string += str(tag[0])
            for field in tag[1:-1]:
                tags_string += serializer
                # print 'DEBUG _tuple_to_cpppo_tags field: ', field
                tags_string += str(field)

            tags_string += '='
            tags_string += str(tag[-1])
            tags_string += ' '
        print 'DEBUG enip server tags_string: ', tags_string

        return tags_string

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

        CMD = sys.executable + ' -m cpppo.server.enip '
        PRINT_STDOUT = '--print '
        HTTP = '--web %s:80 ' % address[0:address.find(':')]
        # print 'DEBUG: enip _start_server_cmd HTTP: ', HTTP
        ADDRESS = '--address ' + address + ' '
        TAGS = EnipProtocol._tuple_to_cpppo_tags(tags)

        if sys.platform.startswith('linux'):
            SHELL = '/bin/bash -c '
            LOG = '--log logs/protocols_tests_enip_server '
        else:
            raise OSError

        cmd = shlex.split(
            CMD +
            PRINT_STDOUT +
            LOG +
            ADDRESS +
            TAGS
        )
        print 'DEBUG enip _start_server cmd: ', cmd

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

    # TODO: remove try ... except, maybe return sent value
    def _send(
            self, what, value,
            address='localhost:44818'):
        """Send (serve) a value.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        :what: tuple addressing what
        :value: sent
        :address: ip[:port]
        """

        tag_string = ''
        tag_string = EnipProtocol._tuple_to_cpppo_tag(what, value)

        cmd = shlex.split(
            self._client_cmd +
            '--log ' + self._client_log +
            '--address ' + address +
            tag_string
        )
        # print 'DEBUG enip _send cmd: ', cmd

        # TODO: pipe stdout and return the sent value
        try:
            client = subprocess.Popen(cmd, shell=False)
            client.wait()

        except Exception as error:
            print 'ERROR enip _send: ', error

    # TODO: remove try ... except, maybe return rec value
    def _receive(
            self, what,
            address='localhost:44818'):
        """Recieve a (requested) value.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        :what: to ask for
        :address: to receive from
        """

        tag_string = ''
        tag_string = EnipProtocol._tuple_to_cpppo_tag(what)

        cmd = shlex.split(
            self._client_cmd +
            '--log ' + self._client_log +
            '--address ' + address +
            tag_string
        )
        # print 'DEBUG enip _receive cmd: ', cmd

        try:
            client = subprocess.Popen(
                cmd,
                shell=False,
                stdout=subprocess.PIPE)

            # client.communicate is blocking
            raw_out = client.communicate()
            # print 'DEBUG enip _receive raw_out: ', raw_out

            # value is stored as first tuple element
            # between a pair of square brackets
            raw_string = raw_out[0]
            out = raw_string[(raw_string.find('[') + 1):raw_string.find(']')]
            return out

        except Exception as error:
            print 'ERROR enip _receive: ', error
