"""
protocols_test.
"""
# import os
import pymodbus
import cpppo

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
        'port': 4444,
        'mode': 1,
    }

    SERVER_PORT = 44818
    SERVER_CMD = 'python -m cpppo.server.enip'
    SERVER_TAGS = 'SENSOR1=INT SENSOR2=REAL ACTUATOR1=INT'
    SERVER_PRINT_STDOUT = '--print'
    SERVER_HTTP = '--web localhost:8000'
    SERVER_LOG = '--log logs/protocol_tests_enip_server'

    CLIENT_CMD = 'python -m cpppo.server.enip.client'
    CLIENT_PRINT_STDOUT = '--print'
    CLIENT_READ = 'SENSOR1'
    CLIENT_WRITE = 'SENSOR1=2'
    CLIENT_LOG = '--log logs/protocol_tests_enip_client'

    def test_init(self):

        enip = EnipProtocol(
            protocol=TestEnipProtocol.PROTOCOL)

        eq_(enip._name, 'enip')
        eq_(enip._port, 4444)
        eq_(enip._mode, 1)

    def test_client(self):

        PROTOCOL = {
            'name': 'enip',
            'port': 4444,
            'mode': 0,  # client mode
        }

        # start an enip server

        # enip = EnipProtocol(
        #     protocol=PROTOCOL)

        # enip._send(SERVER_ADDR, what)

        # kill enip server

    def test_server(self):

        pass
