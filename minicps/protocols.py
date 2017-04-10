"""
``protocols`` module.

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

Modbus is supported using pymodbus module:
https://github.com/bashwork/pymodbus
"""

import sys
import shlex
import subprocess

import cpppo
import pymodbus


# Protocol {{{1
class Protocol(object):

    """Base class.

    Ideally different objects can be attached to the same Device class
    to support multi-protocol CPS.
    """

    # NOTE: used to serialize tags when multiple keys are used
    _SERIALIZER = ':'

    # TODO: what if the server supports multiple protocols with different ports
    def __init__(self, protocol):
        """Init a Protocol object.

        protocol fields:

            - name: textual identifier (eg: enip).
            - mode: int coding mode eg: 1 = modbus asynch TCP.
            - server: dict containing server settings, empty if mode = 0.

        extra fields:

            - minicps_path: full (Linux) path, including ending backslash

        :protocol: validated dict passed from Device obj
        """

        # TODO: add client dictionary
        self._name = protocol['name']
        self._mode = protocol['mode']

        try:
            from minicps import __file__
            index = __file__.rfind('minicps')
            self._minicps_path = __file__[:index+7] + '/'

        except Exception as error:
            print 'ERROR Protocol __init__ set _minicps_path: ', error

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

    def _send(self, what, value, address, **kwargs):
        """Send (write) a value to another host.

        :what: to send
        :address: to send to
        """

        print '_send: please override me.'

    def _receive(self, what, address, **kwargs):
        """Receive (read) a value from another host.

        :address: to receive from
        :what: to ask for
        """

        print '_receive: please override me.'

    def _send_multiple(self, what, values, address):
        """Send (write) multiple values to another host.

        :address: to receive from
        :what: to ask for
        """

        print '_send_multiple: please override me.'

# }}}

# EnipProtocol {{{1

# TODO:  support vectorial tags def, read and write
# int def:   SCADA=INT[3]
# int read:  SCADA[0-3]
# int write: SCADA[0-3]=1,2,3,4
# string def:   TEXT=SSTRING[30]
# string read:  TEXT
# string write: 'TEXT[0]=(SSTRING)"Hello world"'
class EnipProtocol(Protocol):

    """EnipProtocol manager.

    name: enip

    EnipProtocol manages python cpppo library, Look at the original
    documentation for more information.

    Tags are passed as a tuple of tuples, if the tuple contains only 1 tag
    remember to put an ending comma, otherwise python will interpret the data
    as a tuple and not as a tuple of tuples.

        eg: tag = (('SENSOR1'), )

    Supported modes:
        - 0: client only
        - 1: tcp enip server

    Supported tag data types:
        - SINT (8-bit)
        - INT (16-bit)
        - DINT (32-bit)
        - REAL (32-bit float)
        - BOOL (8-bit, bit #0)
        - SSTRING[10] (simple string of 10 chars)
    """

    # server ports
    _TCP_PORT = ':44818'
    _UDP_PORT = ':2222'

    def __init__(self, protocol):

        super(EnipProtocol, self).__init__(protocol)

        self._client_cmd = sys.executable + ' -m cpppo.server.enip.client '

        # NOTE: set up logging
        if sys.platform.startswith('linux'):
            self._client_log = 'logs/enip_client '
        else:
            raise OSError

        # tcp enip server
        if self._mode == 1:

            # NOTE: set up logging
            if sys.platform.startswith('linux'):
                self._server_log = 'logs/enip_tcp_server '
            else:
                raise OSError

            print 'DEBUG EnipProtocol server addr: ', self._server['address']
            if self._server['address'].find(':') == -1:
                print 'DEBUG: concatenating server address with default port.'
                self._server['address'] += EnipProtocol._TCP_PORT

            elif not self._server['address'].endswith(EnipProtocol._TCP_PORT):
                print 'WARNING: not using std enip %s TCP port' % \
                    EnipProtocol._TCP_PORT

            self._server_cmd = sys.executable + ' -m cpppo.server.enip '

            self._server_subprocess = EnipProtocol._start_server(
                    address=self._server['address'],
                    tags=self._server['tags'])

        # TODO: udp enip server
        elif self._mode == 2:

            # NOTE: set up logging
            if sys.platform.startswith('linux'):
                self._server_log = 'logs/enip_udp_server '
            else:
                raise OSError

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

        Value correctness is up the client and it is blindly
        converted to string and appended to the cpppo client query.
        """

        tag_string = ''
        tag_string += str(what[0])

        if len(what) > 1:
            for field in what[1:]:
                tag_string += EnipProtocol._SERIALIZER
                tag_string += str(field)
        if value is not None:
            if type(value) is str:
                # TODO: add support for SSTRING tags
                # ''' enip_client -a 192.168.1.20 'README:2[0]=(SSTRING)"string"' '''
                pass
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

    @classmethod
    def _start_server(cls, address, tags):
        """Start a cpppo enip server.

        The command used to start the server is generated by
        ``_start_server_cmd``.

        Notice that the client has to manage the new process,
        eg:kill it after use.

        :address: to serve
        :tags: to serve
        """

        try:
            cmd = EnipProtocol._start_server_cmd(address, tags)
            server = subprocess.Popen(cmd, shell=False)

            return server

        except Exception as error:
            print 'ERROR enip _start_server: ', error

    # TODO: how to start a UDP cpppo server?
    # TODO: parametric PRINT_STDOUT and others
    @classmethod
    def _start_server_cmd(cls, address='localhost:44818',
        tags=(('SENSOR1', 'INT'), ('ACTUATOR1', 'INT'))):
        """Build a subprocess.Popen cmd string for cpppo server.

        Tags can be any tuple of tuples. Each tuple has to contain a set of
        string-convertible fields, the last one has to be a string containing
        a supported datatype. The current serializer is : (colon).

        Consistency between enip server key-values and state key-values has to
        be guaranteed by the client.

        :address: to serve
        :tags: to serve

        :returns: list of strings generated with shlex.split,
                  passable to subprocess.Popen object
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
    def _stop_server(cls, server):
        """Stop an enip server.

        :server: subprocess.Popen object
        """

        try:
            server.kill()
        except Exception as error:
            print 'ERROR stop enip server: ', error

    def _send(self, what, value, address='localhost:44818', **kwargs):
        """Send (write) a value to another host.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        :what: tuple addressing what
        :value: sent
        :address: ip[:port]
        """

        tag_string = ''
        tag_string = EnipProtocol._tuple_to_cpppo_tag(what, value)
        # print 'DEBUG enip _send tag_string: ', tag_string

        cmd = shlex.split(
            self._client_cmd +
            '--log ' + self._client_log +
            '--address ' + address +
            ' ' + tag_string
        )
        # print 'DEBUG enip _send cmd shlex list: ', cmd

        # TODO: pipe stdout and return the sent value
        try:
            client = subprocess.Popen(cmd, shell=False)
            client.wait()

        except Exception as error:
            print 'ERROR enip _send: ', error

    def _receive(self, what, address='localhost:44818', **kwargs):
        """Receive (read) a value from another host.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        :what: to ask for
        :address: to receive from

        :returns: tag value as a `str`
        """

        tag_string = ''
        tag_string = EnipProtocol._tuple_to_cpppo_tag(what)

        cmd = shlex.split(
            self._client_cmd +
            '--log ' + self._client_log +
            '--address ' + address +
            ' ' + tag_string
        )
        # print 'DEBUG enip _receive cmd shlex list: ', cmd

        try:
            client = subprocess.Popen(cmd, shell=False,
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

# }}}


# ModbusProtocol {{{1
class ModbusProtocol(Protocol):

    """ModbusProtocol manager.

    name: modbus

    Tag is a generic name to manage modbus datatypes: coils, discrete inputs,
    holding registers, and input registers. The servers will init all the tags
    to 0, and they will use pymodbus's ModbusSequentialDataBlock. The
    addressing is the default one (zero_mode=False). The context is using a
    single slave mode.

    Supported modes:
        - 0: client only (currently synch and blocking)
        - 1: tcp asynch modbus server

    Supported tag data types:
        - CO (1-bit, coil, read and write)
        - DI (1-bit, discrete input, read only)
        - HR (16-bit, holding register, read and write)
        - IR (16-bit, input register, read only)
    """

    # server ports
    _TCP_PORT = ':502'
    # _UDP_PORT = ':TODO

    def __init__(self, protocol):

        super(ModbusProtocol, self).__init__(protocol)

        self._client_cmd = sys.executable + ' ' + \
        self._minicps_path + 'pymodbus/synch-client.py '  # NOTE: ending whitespace
        # NOTE: currently using blocking synch client
        # self._client_cmd = sys.executable + \
        # self._minicps_path + 'pymodbus/asynch-client.py '  # NOTE: ending whitespace

        if sys.platform.startswith('linux'):
            self._client_log = 'logs/modbus_client '
        else:
            raise OSError

        # NOTE: modbus asynch tcp server
        if self._mode == 1:

            # NOTE: set up logging
            if sys.platform.startswith('linux'):
                self._server_log = 'logs/modbus_tcp_server '
            else:
                raise OSError

            print 'DEBUG ModbusProtocol server addr: ', self._server['address']
            if self._server['address'].find(':') == -1:
                print 'DEBUG: concatenating server address with default port.'
                self._server['address'] += ModbusProtocol._TCP_PORT

            elif not self._server['address'].endswith(ModbusProtocol._TCP_PORT):
                print 'WARNING: not using std modbus %s TCP port' % \
                    ModbusProtocol._TCP_PORT

            server_cmd_path = sys.executable + ' ' + self._minicps_path + \
                    'pymodbus/servers.py '   # NOTE: ending whitespace
            print 'DEBUG: generating server_cmd_path: {}'.format(server_cmd_path)

            self._server_subprocess = ModbusProtocol._start_server(
                address=self._server['address'],
                tags=self._server['tags'],
                cmd_path=server_cmd_path,
                mode=self._mode,
            )

        # TODO: udp modbus server
        elif self._mode == 2:

            # NOTE: set up logging
            if sys.platform.startswith('linux'):
                self._server_log = 'logs/modbus_udp_server '
            else:
                raise OSError

            # TODO: implement it


    # TODO: still not sure about the tags API
    @classmethod
    def _start_server(cls, cmd_path, address='localhost:502',
        tags=(20, 20, 20, 20), mode=1):
        """Start a pymodbus modbus server.

        The command used to start the server is generated by
        ``_start_server_cmd``.

        Consistency between modbus server key-values and state key-values has to
        be guaranteed by the client.

        :cmd_path: path to the script to start a server
        :address: ip:port
        :tags: ordered tuple of ints representing the numbers of discrete
               inputs, coils, input registers, and holding registers to be init.
               Current pymodbus servers only support ModbusSequentialDataBlock.
        :mode: int greater than 1, typically set by the constructor

        :returns: list of strings generated with shlex.split,
                  passable to subprocess.Popen object
        """

        try:
            cmd = ModbusProtocol._start_server_cmd(cmd_path, address, tags, mode)
            server = subprocess.Popen(cmd, shell=False)

            return server

        except Exception as error:
            print 'ERROR modbus _start_server: ', error


    @classmethod
    def _start_server_cmd(cls, cmd_path, address='localhost:502',
        tags=(20, 20, 20, 20), mode=1):
        """Build a subprocess.Popen cmd string for pycomm server."""

        if sys.platform.startswith('linux'):
            SHELL = '/bin/bash -c '
            LOG = '--log logs/protocols_tests_modbus_server '
        else:
            raise OSError

        colon_index = address.find(':')
        IP = '-i {} '.format(address[:colon_index])
        PORT = '-p {} '.format(address[colon_index+1:])
        MODE = '-m {} '.format(mode)
        DI = '-d {} '.format(tags[0])
        CO = '-c {} '.format(tags[1])
        IR = '-r {} '.format(tags[2])
        HR = '-R {} '.format(tags[3])
        # TAGS = ModbusProtocol._tuple_to_pymodbus_tags(tags)

        cmd = shlex.split(
            cmd_path +
            IP +
            PORT +
            MODE +
            DI + CO + IR + HR
        )
        print 'DEBUG modbus _start_server cmd: ', cmd

        return cmd


    # FIXME: not implemented because we are passing just the number of tags
    @classmethod
    def _tuple_to_pymodbus_tags(cls, tags, serializer=':'):
        """Returns a TODO

        pymodbus server API:

            store = ModbusSlaveContext(
                di=ModbusSequentialDataBlock(0, [17] * 100),
                co=ModbusSequentialDataBlock(0, [17] * 100),
                hr=ModbusSequentialDataBlock(0, [17] * 100),
                ir=ModbusSequentialDataBlock(0, [17] * 100),
            )

        """

        pass


    @classmethod
    def _stop_server(cls, server):
        """Stop a modbus server.

        :server: subprocess.Popen object
        """

        try:
            server.kill()
        except Exception as error:
            print 'ERROR stop modbus server: ', error


    def _send(self, what, value, address='localhost:502', **kwargs):
        """Send (write) a value to another host.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        Boolean values are converted back and forth to integers because
        ``argparse`` does not handle bool arguments correctly, eg: False
        string is evaluated and passed as True.

        pymodbus has a ``count`` kwarg to perform sequential read and write
        starting from the offset passed inside ``what``. Default call will
        write one value at a time. Pass a list of values if ``count`` is
        greater than one.


        :what: tuple addressing what
        :value: sent
        :address: ip[:port], not validated
        """

        colon_index = address.find(':')
        IP = '-i {} '.format(address[:colon_index])
        PORT = '-p {} '.format(address[colon_index+1:])
        # NOTE: following data is validated by client script
        MODE = '-m {} '.format('w')
        TYPE = '-t {} '.format(what[0])
        OFFSET = '-o {} '.format(what[1])  # NOTE: 0-based

        # NOTE: value is a list of bools or ints when write multiple times
        if 'count' in kwargs and kwargs['count'] > 1:
            count = kwargs['count']
            COUNT = '--count {} '.format(count)
        else:
            count = 1
            COUNT = '--count {} '.format(count)

        # NOTE: value is a int when writing to a register
        if what[0] == 'HR':
            if count == 1:
                VALUE = '-r {} '.format(value)
            else:
                VALUE = '-r '
                for v in value:
                    VALUE += str(v)
                    VALUE += ' '

        # NOTE: value is a bool when writing to a coil
        elif what[0] == 'CO':
            if count == 1:
                if value == True:
                    VALUE = '-c {} '.format(1)
                else:
                    VALUE = '-c {} '.format(0)
            else:
                VALUE = '-c '
                for v in value:
                    if v ==  True:
                        VALUE += str(1)
                    else:
                        VALUE += str(0)
                    VALUE += ' '
        else:
            raise ValueError('IR and DI are read only data.')


        cmd = shlex.split(
            self._client_cmd +
            IP +
            PORT +
            MODE +
            TYPE +
            OFFSET +
            COUNT +
            VALUE
        )
        # print 'DEBUG modbus_send cmd shlex list: ', cmd

        # TODO: pipe stdout and return the sent value
        try:
            client = subprocess.Popen(cmd, shell=False)
            client.wait()

        except Exception as error:
            print 'ERROR modbus _send: ', error


    def _receive(self, what, address='localhost:502', **kwargs):
        """Receive (read) a value from another host.

        It is a blocking operation the parent process will wait till the child
        cpppo process returns.

        pymodbus has a ``count`` kwarg to perform sequential read and write
        starting from the offset passed inside ``what``. Default call will
        request and return one value at a time.

        The return type depends on the request type:
            - read_coils returns an array of bools
            - read_discrete_inputs returns a list of bools
            - read_register returns an int
            - read_registers returns a list of ints

        :what: to ask for
        :address: ip[:port], not validated

        :returns: read value(s)
        """
        colon_index = address.find(':')
        IP = '-i {} '.format(address[:colon_index])
        PORT = '-p {} '.format(address[colon_index+1:])
        # NOTE: following data is validated by client script
        MODE = '-m {} '.format('r')
        TYPE = '-t {} '.format(what[0])
        OFFSET = '-o {} '.format(what[1])  # NOTE: 0-based

        # NOTE: kwargs
        if 'count' in kwargs:
            count = kwargs['count']
            COUNT = '--count {} '.format(kwargs['count'])
        else:
            count = 1
            COUNT = '--count {} '.format(1)

        cmd = shlex.split(
            self._client_cmd +
            IP +
            PORT +
            MODE +
            TYPE +
            OFFSET +
            COUNT
        )
        # print 'DEBUG modbus_receive cmd shlex list: ', cmd

        try:
            client = subprocess.Popen(cmd, shell=False,
                stdout=subprocess.PIPE)

            # client.communicate is blocking
            raw_out = client.communicate()
            # print 'DEBUG modbus _receive raw_out: ', raw_out

            # value is stored as first tuple element
            # between a pair of square brackets
            raw_string = raw_out[0].strip()

            # NOTE: registers store int
            if what[0] == 'HR' or what[0] == 'IR':

                # NOTE: single read returns an int
                if count == 1:
                    out = int(raw_string[1:-1])

                # NOTE: multiple reads returns a list of ints
                else:
                    out = []
                    hrs = raw_string[1:-1].split(',')
                    for hr in hrs:
                        out.append(int(hr))
                    if len(out) != count:
                        raise ValueError('Wrong number of values in the response.')

            # NOTE: coils and discrete inputs store 8 bools
            elif what[0] == 'CO' or what[0] == 'DI':
                # print 'DEBUG modbus _receive bools: ', bools

                # NOTE: pymodbus always returns at least a list of 8 bools
                bools = raw_string[1:-1].split(',')

                # NOTE: single read returns a bool
                if count == 1:
                    if bools[0] == 'False':
                        out = False
                    elif bools[0] == 'True':
                        out = True
                    else:
                        raise TypeError('CO or DI values must be bool.')

                # NOTE: multiple reads returns a list of bools
                else:
                    out = []
                    i = 0
                    for b in bools:
                        if i >= count:
                            break
                        elif b.strip() == 'False':
                            out.append(False)
                        elif b.strip() == 'True':
                            out.append(True)
                        else:
                            raise TypeError('CO or DI values must be bool.')
                        i += 1

            return out

        except Exception as error:
            print 'ERROR modbus _receive: ', error

# }}}
