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

    def test_init(self):

        enip = Protocol(
            protocol=CLIENT_SERVER_PROTOCOL)
        eq_(enip._name, 'enip')
        eq_(enip._mode, 1)
        eq_(enip._server['address'], 'localhost:44818')
        eq_(
            enip._server['tags'],
            (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT')))
        del enip

        enip = Protocol(
            protocol=CLIENT_PROTOCOL)
        eq_(enip._name, 'enip')
        eq_(enip._mode, 0)
        eq_(enip._server, {})  # pass an empty server dict

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
            print "TEST: client has to kill the cpppo process."
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

        TAGS = (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT'))
        cmd = EnipProtocol._start_server_cmd(tags=TAGS)
        try:
            server = subprocess.Popen(cmd, shell=False)

            # read a multikey
            what = ('SENSOR1', 1)
            address = 'localhost:44818'
            enip._receive(what, address)

            # read a single key
            what = ('ACTUATOR1',)
            address = 'localhost:44818'
            enip._receive(what, address)

            EnipProtocol._stop_server(server)

        except Exception as error:
            EnipProtocol._stop_server(server)
            print 'ERROR test_client: ', error

    def test_client_server(self):

        try:
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

    @SkipTest
    def test_server_start_cmd(self):

        try:
            print "TEST: client has to kill the pymodbus process."
            cmd = ModbusProtocol._start_server_cmd(tags=self.TAGS)
            server = subprocess.Popen(cmd, shell=False)
        except Exception as error:
            print 'ERROR test_server_start_cmd: ', error

    @SkipTest
    def test_server_start(self):

        try:
            print "TEST: client has to kill the pymodbus process."
            ModbusProtocol._start_server('localhost:502', self.TAGS)

        except Exception as error:
            print 'ERROR test_server_start: ', error

    def test_server_stop(self):

        cmd = ModbusProtocol._start_server_cmd()
        try:
            server = subprocess.Popen(cmd, shell=False)
            ModbusProtocol._stop_server(server)

        except Exception as error:
            print 'ERROR test_server_stop: ', error

    def test_init(self):

        # TODO: add _stop_server
        client = ModbusProtocol(
            protocol=TestModbusProtocol.CLIENT_PROTOCOL)
        eq_(client._name, 'modbus')
        del client

        server = ModbusProtocol(
            protocol=TestModbusProtocol.CLIENT_SERVER_PROTOCOL)
        eq_(server._name, 'modbus')
        server._stop_server(server._server_subprocess)
        del server


    # TODO: test client commands
    # TODO: test client and server interactions
# }}}
