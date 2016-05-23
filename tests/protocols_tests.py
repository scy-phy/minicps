"""
protocols_test.
"""
import os
# import pymodbus
import cpppo
import subprocess
import sys
import shlex

from minicps.protocols import Protocol, EnipProtocol

from nose.tools import eq_
from nose.plugins.skip import SkipTest

# TODO: still not spec of the dict
PROTOCOL = {
    'name': 'enip',
    'port': 4444,
    'mode': 1,
}


class TestProtocol():

    def test_init(self):

        enip = Protocol(
            protocol=PROTOCOL)

        eq_(enip._name, 'enip')
        eq_(enip._port, 4444)
        eq_(enip._mode, 1)


@SkipTest
def test_EnipProtocolClassMethods():

    pass


class TestEnipProtocol():

    PROTOCOL = {
        'name': 'enip',
        'port': 44818,
        'mode': 1,
    }

    SERVER_TCP_PORT = 44818
    SERVER_UDP_PORT = 2222
    SERVER_TAGS = 'SENSOR1=INT SENSOR2=REAL ACTUATOR1=INT '
    SERVER_PRINT_STDOUT = '--print '
    CLIENT_PRINT_STDOUT = '--print '
    SERVER_HTTP = '--web localhost:8000 '
    SERVER_ADDRESS = '--address localhost:' + str(SERVER_TCP_PORT) + ' '

    if sys.platform.startswith('linux'):
        BASH = '/bin/bash -c '
        SERVER_LOG = '--log logs/protocol_tests_enip_server '
        CLIENT_LOG = '--log logs/protocol_tests_enip_client '

    else:
        raise OSError

    SERVER_CMD = sys.executable + ' -m cpppo.server.enip '
    CLIENT_CMD = sys.executable + ' -m cpppo.server.enip.client '
    CLIENT_READ = 'SENSOR1 '
    CLIENT_WRITE = 'SENSOR1=2 '

    def test_init(self):

        enip = EnipProtocol(
            protocol=TestEnipProtocol.PROTOCOL)

        eq_(enip._name, 'enip')
        eq_(enip._port, 44818)
        eq_(enip._mode, 1)

    def test_client(self):

        PROTOCOL = {
            'name': 'enip',
            'mode': 0,  # client mode
            'port': -1,
        }

        enip = EnipProtocol(
            protocol=PROTOCOL)

        # TODO: how to start TCP vs UDP server
        # start a test server
        cmd = shlex.split(
            # TestEnipProtocol.BASH +
            TestEnipProtocol.SERVER_CMD +
            TestEnipProtocol.SERVER_PRINT_STDOUT +
            TestEnipProtocol.SERVER_LOG +
            TestEnipProtocol.SERVER_ADDRESS +
            TestEnipProtocol.SERVER_TAGS
        )
        print 'DEBUG enip server cmd: ', cmd

        try:
            server = subprocess.Popen(cmd, shell=False)
            server.wait()
        except Exception as error:
            print 'ERROR enip server: ', error
            server.kill()

        # what = ('SENSOR1',)
        # enip._receive(SERVER_ADDRESS, what)

        # maybe add a try block ?

    def test_server(self):

        pass
