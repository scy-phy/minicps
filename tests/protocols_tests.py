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

    if sys.platform.startswith('linux'):
        SHELL = '/bin/bash -c '
        CLIENT_LOG = '--log logs/protocol_tests_enip_client '
    else:
        raise OSError

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

        server = EnipProtocol._start_server()

        # TODO: how to start TCP vs UDP server
        # start a test server

        # what = ('SENSOR1',)
        # enip._receive(SERVER_ADDRESS, what)

        # maybe add a try block ?

    def test_server(self):

        pass
