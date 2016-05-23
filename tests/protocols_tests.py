"""
protocols_test.
"""

import os
import subprocess
import sys
import shlex
import time

# import pymodbus
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

    def test_server_stop(self):

        cmd = EnipProtocol._start_server_cmd()
        try:
            server = subprocess.Popen(cmd, shell=False)
            EnipProtocol._stop_server(server)

        except Exception as error:
            print 'ERROR test_server_stop: ', error

    @SkipTest
    def test_server_start(self):

        ADDRESS = 'localhost:44818'  # TEST port
        TAGS = (('SENSOR1', 'INT'), ('ACTUATOR1', 'INT'))
        try:
            print "TEST: client has to kill the cpppo process."
            EnipProtocol._start_server(ADDRESS, TAGS)
        except Exception as error:
            print 'ERROR test_server_start: ', error

    def test_server_multikey(self):

        TAGS = (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT'))
        cmd = EnipProtocol._start_server_cmd(tags=TAGS)
        try:
            server = subprocess.Popen(cmd, shell=False)
            time.sleep(15)
            EnipProtocol._stop_server(server)
        except Exception as error:
            print 'ERROR test_server_multikey: ', error

    def test_server_udp(self):

        pass

    def test_client(self):

        PROTOCOL = {
            'name': 'enip',
            'mode': 0,
            'port': -1,
        }

        enip = EnipProtocol(
            protocol=PROTOCOL)

        # what = ('SENSOR1',)
        # enip._receive(SERVER_ADDRESS, what)

    def test_client_server(self):

        PROTOCOL = {
            'name': 'enip',
            'mode': 1,
            'port': 1,
        }

        enip = EnipProtocol(
            protocol=PROTOCOL)
