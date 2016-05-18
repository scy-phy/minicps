"""
devices tests
"""

import time
import sys

from minicps.devices import Device, PLC

from nose.tools import eq_
from nose.plugins.skip import SkipTest

NAME = 'devices_tests'
STATE = {
    'path': 'temp/state_test_db.sqlite',
    'name': 'state_test'
}
PROTOCOL = 'enip'


@SkipTest
def test_Device():

    print
    device = Device(
        name='device',
        state={
            'path': 'temp/state_test_db.sqlite',
            'name': 'state_test'
        },
        protocol='enip',
        memory={
            'TAG1': '1',
            'TAG2': '2',
        },
        disk={
            'TAG1': '1',
            'TAG2': '2',
            'TAG4': '4',
            'TAG5': '5',
        })

    print 'Device name: ', device.name
    print 'Device state: ', device.state
    print 'Device protocol: ', device.protocol
    print 'Device memory: ', device.memory
    print 'Device disk: ', device.disk

    # device.set('TAG1', '2')
    # device.get('TAG2')


class TestDevicePublicAPI():

    def test_validate_name(self):
        """name should be a non-empty string."""

        print
        try:
            device = Device(
                name=1,
                state=STATE,
                protocol=PROTOCOL)
        except TypeError as error:
            print 'TEST name is an int: ', error

        try:
            device = Device(
                name='',
                state=STATE,
                protocol=PROTOCOL)
        except ValueError as error:
            print 'TEST name is empty string: ', error

    def test_validate_state(self):
        """state should be a dict.

        state = {
            'name': 'state_name',
            'path': '/tmp/state.ext'

        """

        print
        try:
            device = Device(
                name=NAME,
                state='state',
                protocol=PROTOCOL)
        except TypeError as error:
            print 'TEST state is a string: ', error

        try:
            device = Device(
                name=NAME,
                state={},
                protocol=PROTOCOL)
        except KeyError as error:
            print 'TEST state is an empty dict: ', error

        try:
            device = Device(
                name=NAME,
                state={
                    'name': 'table_name', 'path': '/path.db',
                    'wrong': 'key-val'},
                protocol=PROTOCOL)
        except KeyError as error:
            print 'TEST state has more than 2 keys: ', error

        try:
            device = Device(
                name=NAME,
                state={
                    'path': '/bla',
                    'bla': 'table_name'},
                protocol=PROTOCOL)
        except KeyError as error:
            print 'TEST: state has a wrong key: ', error

        try:
            device = Device(
                name=NAME,
                state={
                    'path': 0,
                    'name': 'table_name'},
                protocol=PROTOCOL)
        except TypeError as error:
            print 'TEST: state has a key referencing an int: ', error


@SkipTest
def test_PLC():

    class TestPLC(PLC):

        def pre_loop(self, sleep=0.5):
            """PLC boot process.

            :sleep: sleep n sec after it
            """

            eq_(self.set(('SENSOR1', 1), '10'), '10')
            eq_(self.get(('SENSOR1', 1)), '10')
            eq_(self.get(('SENSOR3', 1)), '1')
            eq_(self.get(('SENSOR3', 2)), '2')
            time.sleep(sleep)

    print
    plc = TestPLC(
        name='plc',
        state={
            'path': 'temp/state_test_db.sqlite',
            'name': 'state_test'
        },
        protocol='enip',
        memory={
            'TAG1': '1',
            'TAG2': '2',
        },
        disk={
            'TAG1': '1',
            'TAG2': '2',
            'TAG4': '4',
            'TAG5': '5',
        })

    # eq_(plc.get(('SENSOR3', 1))[0], '1')
    # eq_(plc.get(('SENSOR3', 2))[0], '2')
