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
PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'port': 4444,
}

MEMORY = {
    'TAG1': '1',
    'TAG2': '2',
}

DISK = {
    'TAG1': '1',
    'TAG2': '2',
    'TAG4': '4',
    'TAG5': '5',
}


class TestDevice():

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

        try:
            device = Device(
                name=NAME,
                state={
                    'path': '/not/supported.ext',
                    'name': 'table_name'},
                protocol=PROTOCOL)
        except ValueError as error:
            print 'TEST: state has an unsupported path extension: ', error

        try:
            device = Device(
                name=NAME,
                state={
                    'path': '/not/supported.ext',
                    'name': 4},
                protocol=PROTOCOL)
        except TypeError as error:
            print 'TEST: state has an integer name: ', error

    # TODO: finish to set the API
    def test_validate_protocol(self):

        pass

    def test_validate_disk(self):
        """disk should be a dict."""

        pass

    def test_validate_memory(self):
        """memory should be a dict."""

        pass

    def test_validate_get(self):
        """get accepts a tuple."""

        device = Device(
            name=NAME,
            state=STATE,
            protocol=PROTOCOL)

        try:
            device.get(2.22)
        except TypeError as error:
            print 'TEST: get what is a float: ', error

    def test_validate_set(self):
        """set accepts a tuple and a generic value."""

        device = Device(
            name=NAME,
            state=STATE,
            protocol=PROTOCOL)

        try:
            device.set(2, 5)
        except TypeError as error:
            print 'TEST: set what is an integer: ', error

    # TODO: finish to set the API
    def test_validate_send(self):

        pass

    # TODO: finish to set the API
    def test_validate_recieve(self):

        pass

    def test_init(self):
        """validate Device __init__."""

        device = Device(
            name=NAME,
            state=STATE,
            protocol=PROTOCOL)


class TestPLC():

    def test_set_get(self, sleep=0.3):

        print

        class ToyPLC(PLC):

            def pre_loop(self):

                eq_(self.set(('SENSOR1', 1), '10'), '10')
                eq_(self.get(('SENSOR1', 1)), '10')
                eq_(self.get(('SENSOR3', 1)), '1')
                eq_(self.get(('SENSOR3', 2)), '2')
                time.sleep(sleep)

        device = ToyPLC(
            name=NAME,
            state=STATE,
            protocol=PROTOCOL)
