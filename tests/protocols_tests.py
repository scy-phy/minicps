"""
protocols_test.
"""

import os
import subprocess
import sys
import shlex
import time

import pymodbus
import cpppo

from minicps.protocols import Protocol, EnipProtocol, ModbusProtocol

from nose.tools import eq_
from nose.plugins.skip import SkipTest

# TODO: add new server keys
SERVER = {
    'address': 'localhost:44818',
    'tags': (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT')),
}
CLIENT_SERVER_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': SERVER,
}

CLIENT_PROTOCOL = {
    'name': 'enip',
    'mode': 0,
    'server': '',
}

# TestProtocol {{{1
class TestProtocol():

    pass

# }}}

# TestEnipProtocol {{{1
class TestEnipProtocol():

    # NOTE: second tuple element is the process id
    TAGS = (
        ('SENSOR1', 1, 'INT'),
        ('SENSOR1', 2, 'INT'),
        ('ACTUATOR1', 'INT'))
    SERVER = {
        'address': 'localhost:44818',
        'tags': TAGS
    }
    CLIENT_SERVER_PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': SERVER,
    }
    CLIENT_PROTOCOL = {
        'name': 'enip',
        'mode': 0,
        'server': '',
    }
    if sys.platform.startswith('linux'):
        SHELL = '/bin/bash -c '
        CLIENT_LOG = '--log logs/protocols_tests_enip_client '
    else:
        raise OSError

    def test_server_start_stop(self):

        ADDRESS = 'localhost:44818'  # TEST port
        TAGS = (('SENSOR1', 'INT'), ('ACTUATOR1', 'INT'))

        try:
            server = EnipProtocol._start_server(ADDRESS, TAGS)
            EnipProtocol._stop_server(server)

        except Exception as error:
            print 'ERROR test_server_start_stop: ', error

    def test_init_client(self):

        try:
            client = EnipProtocol(
                protocol=TestEnipProtocol.CLIENT_PROTOCOL)
            eq_(client._name, 'enip')
            del client
        except Exception as error:
            print 'ERROR test_init_client: ', error

    def test_init_server(self):

        try:
            server = EnipProtocol(
                protocol=TestEnipProtocol.CLIENT_SERVER_PROTOCOL)
            eq_(server._name, 'enip')
            server._stop_server(server._server_subprocess)
            del server
        except Exception as error:
            print 'ERROR test_init_server: ', error

    def test_server_multikey(self):

        ADDRESS = 'localhost:44818'  # TEST port
        TAGS = (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT'))
        try:
            server = EnipProtocol._start_server(ADDRESS, TAGS)
            EnipProtocol._stop_server(server)
        except Exception as error:
            print 'ERROR test_server_multikey: ', error

    def test_send_multikey(self):

        enip = EnipProtocol(
            protocol=CLIENT_PROTOCOL)

        ADDRESS = 'localhost:44818'  # TEST port
        TAGS = (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT'))

        try:
            server = EnipProtocol._start_server(ADDRESS, TAGS)

            # write a multikey
            what = ('SENSOR1', 1)
            for value in range(5):
                enip._send(what, value, ADDRESS)

            # write a single key
            what = ('ACTUATOR1',)
            for value in range(5):
                enip._send(what, value, ADDRESS)

            EnipProtocol._stop_server(server)

        except Exception as error:
            EnipProtocol._stop_server(server)
            print 'ERROR test_send_multikey: ', error

    def test_receive_multikey(self):

        enip = EnipProtocol(
            protocol=CLIENT_PROTOCOL)

        ADDRESS = 'localhost:44818'  # TEST port
        TAGS = (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT'))

        try:
            server = EnipProtocol._start_server(ADDRESS, TAGS)

            # read a multikey
            what = ('SENSOR1', 1)
            address = 'localhost:44818'
            enip._receive(what, ADDRESS)

            # read a single key
            what = ('ACTUATOR1',)
            address = 'localhost:44818'
            enip._receive(what, ADDRESS)

            EnipProtocol._stop_server(server)

        except Exception as error:
            EnipProtocol._stop_server(server)
            print 'ERROR test_receive_multikey: ', error

    def test_client_server(self):

        try:

            # same instance used as server and client
            enip = EnipProtocol(
                protocol=CLIENT_SERVER_PROTOCOL)

            # read a multikey
            what = ('SENSOR1', 1)
            address = 'localhost:44818'
            enip._receive(what, address)

            # read a single key
            what = ('ACTUATOR1',)
            address = 'localhost:44818'
            enip._receive(what, address)

            # write a multikey
            what = ('SENSOR1', 1)
            address = 'localhost:44818'
            for value in range(5):
                enip._send(what, value, address)

            # write a single key
            what = ('ACTUATOR1',)
            address = 'localhost:44818'
            for value in range(5):
                enip._send(what, value, address)

            EnipProtocol._stop_server(enip._server_subprocess)

        except Exception as error:
            EnipProtocol._stop_server(enip._server_subprocess)
            print 'ERROR test_client_server: ', error

    @SkipTest
    def test_server_udp(self):

        # TODO: implement it
        pass

# }}}

# TestModbusProtocol {{{1
class TestModbusProtocol():

    # NOTE: second tuple element is the process id
    TAGS = (10, 10, 10, 10)
    # TAGS = (
    #     ('CO1', 1, 'CO'),
    #     ('CO1', 2, 'CO'),
    #     ('DI1', 1, 'DI'),
    #     ('DI1', 2, 'DI'),
    #     ('HR1', 1, 'HR'),
    #     ('HR2', 2, 'HR'),
    #     ('IR1', 1, 'IR'),
    #     ('IR2', 4, 'IR'))
    SERVER = {
        'address': 'localhost:502',
        'tags': TAGS
    }
    CLIENT_SERVER_PROTOCOL = {
        'name': 'modbus',
        'mode': 1,
        'server': SERVER,
    }
    CLIENT_PROTOCOL = {
        'name': 'modbus',
        'mode': 0,
        'server': '',
    }
    if sys.platform.startswith('linux'):
        SHELL = '/bin/bash -c '
        CLIENT_LOG = '--log logs/protocols_tests_modbus_client '
    else:
        raise OSError

    def test_server_start_stop(self):

        try:
            server = ModbusProtocol._start_server('localhost:502', self.TAGS)
            ModbusProtocol._stop_server(server)

        except Exception as error:
            print 'ERROR test_server_start_stop: ', error


    def test_init_client(self):

        try:
            client = ModbusProtocol(
                protocol=TestModbusProtocol.CLIENT_PROTOCOL)
            eq_(client._name, 'modbus')
            del client

        except Exception as error:
            print 'ERROR test_init_client: ', error


    def test_init_server(self):

        try:
            server = ModbusProtocol(
                protocol=TestModbusProtocol.CLIENT_SERVER_PROTOCOL)
            eq_(server._name, 'modbus')
            server._stop_server(server._server_subprocess)
            del server

        except Exception as error:
            print 'ERROR test_init_server: ', error


    def test_send(self):

        client = ModbusProtocol(
            protocol=CLIENT_PROTOCOL)

        ADDRESS = 'localhost:502'
        TAGS = (20, 20, 20, 20)
        OFFSET = 10

        try:
            server = ModbusProtocol._start_server(ADDRESS, TAGS)
            time.sleep(1.0)

            print('TEST: Write to holding registers')
            for count in range(0, OFFSET):
                what = ('HR', count)
                client._send(what, count, ADDRESS)
            print('')

            coil = True
            print('TEST: Write to coils')
            for count in range(0, OFFSET):
                what = ('CO', count)
                client._send(what, coil, ADDRESS)
                coil = not coil
            print('')

            ModbusProtocol._stop_server(server)

        except Exception as error:
            ModbusProtocol._stop_server(server)
            print 'ERROR test_send: ', error


# }}}
