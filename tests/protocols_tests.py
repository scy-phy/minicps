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
SERVER = {
    'address': 'localhost:44818',
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


class TestProtocol():

    def test_init(self):

        enip = Protocol(
            protocol=CLIENT_SERVER_PROTOCOL)
        eq_(enip._name, 'enip')
        eq_(enip._mode, 1)
        eq_(enip._server['address'], 'localhost:44818')
        del enip

        enip = Protocol(
            protocol=CLIENT_PROTOCOL)
        eq_(enip._name, 'enip')
        eq_(enip._mode, 0)
        eq_(enip._server, '')


class TestEnipProtocol():

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

    def test_init(self):

        enip = EnipProtocol(
            protocol=TestEnipProtocol.CLIENT_PROTOCOL)
        eq_(enip._name, 'enip')
        del enip
        enip = EnipProtocol(
            protocol=TestEnipProtocol.CLIENT_SERVER_PROTOCOL)
        eq_(enip._name, 'enip')

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
            # time.sleep(3)
            EnipProtocol._stop_server(server)
        except Exception as error:
            print 'ERROR test_server_multikey: ', error

    def test_server_udp(self):

        pass

    def test_send_multikey(self):

        enip = EnipProtocol(
            protocol=CLIENT_PROTOCOL)

        TAGS = (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT'))
        cmd = EnipProtocol._start_server_cmd(tags=TAGS)
        try:
            server = subprocess.Popen(cmd, shell=False)

            # write a multikey
            what = ('SENSOR1', 1)
            address = 'localhost:44818'
            for value in range(5):
                enip._send(what, value, address)
                value += 1

            # write a single key
            what = ('ACTUATOR1',)
            address = 'localhost:44818'
            for value in range(5):
                enip._send(what, value, address)
                value += 1

            EnipProtocol._stop_server(server)
            time.sleep(0.5)

        except Exception as error:
            EnipProtocol._stop_server(server)
            print 'ERROR test_client: ', error
            time.sleep(0.5)

    def test_receive_multikey(self):

        enip = EnipProtocol(
            protocol=CLIENT_PROTOCOL)

        TAGS = (('SENSOR1', 1, 'INT'), ('ACTUATOR1', 'INT'))
        cmd = EnipProtocol._start_server_cmd(tags=TAGS)
        try:
            server = subprocess.Popen(cmd, shell=False)

            # write a multikey
            what = ('SENSOR1', 1)
            address = 'localhost:44818'
            enip._receive(what, address)

            # write a single key
            what = ('ACTUATOR1',)
            address = 'localhost:44818'
            enip._receive(what, address)

            EnipProtocol._stop_server(server)
            time.sleep(0.5)

        except Exception as error:
            EnipProtocol._stop_server(server)
            print 'ERROR test_client: ', error
            time.sleep(0.5)

    def test_client_server(self):

        enip = EnipProtocol(
            protocol=CLIENT_SERVER_PROTOCOL)
