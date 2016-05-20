"""
devices tests
"""

import time
import sys
import os

from minicps.devices import Device, PLC
from minicps.state import SQLiteState

from nose.tools import eq_
from nose.plugins.skip import SkipTest


class TestDevice():

    NAME = 'devices_tests'
    STATE = {
        'path': 'temp/devices_tests.sqlite',
        'name': 'devices_tests'
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

    def test_validate_name(self):

        try:
            device = Device(
                name=1,
                state=TestDevice.STATE,
                protocol=TestDevice.PROTOCOL)
        except TypeError as error:
            print 'name is an int: ', error

        try:
            device = Device(
                name='',
                state=TestDevice.STATE,
                protocol=TestDevice.PROTOCOL)
        except ValueError as error:
            print 'name is empty string: ', error

    def test_validate_state(self):

        try:
            device = Device(
                name=TestDevice.NAME,
                state='state',
                protocol=TestDevice.PROTOCOL)
        except TypeError as error:
            print 'state is string: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state={},
                protocol=TestDevice.PROTOCOL)
        except KeyError as error:
            print 'state is an empty dict: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state={
                    'name': 'table_name', 'path': '/path.db',
                    'wrong': 'key-val'},
                protocol=TestDevice.PROTOCOL)
        except KeyError as error:
            print 'state has more than 2 keys: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state={
                    'path': '/bla',
                    'bla': 'table_name'},
                protocol=TestDevice.PROTOCOL)
        except KeyError as error:
            print 'state has a wrong key: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state={
                    'path': 0,
                    'name': 'table_name'},
                protocol=TestDevice.PROTOCOL)
        except TypeError as error:
            print 'state has a key referencing an int: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state={
                    'path': '/not/supported.ext',
                    'name': 'table_name'},
                protocol=TestDevice.PROTOCOL)
        except ValueError as error:
            print 'state has an unsupported path extension: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state={
                    'path': '/not/supported.ext',
                    'name': 4},
                protocol=TestDevice.PROTOCOL)
        except TypeError as error:
            print 'state has an integer name: ', error

    # TODO: finish to set the API
    def test_validate_protocol(self):

        pass

    def test_validate_disk(self):

        pass

    def test_validate_memory(self):

        pass


class TestPLC():

    NAME = 'plc_tests'
    PATH = 'temp/plc_tests.sqlite'
    STATE = {
        'path': 'temp/plc_tests.sqlite',
        'name': 'plc_tests'
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'port': 4444,
    }

    SCHEMA = """
    CREATE TABLE plc_tests (
        name              TEXT NOT NULL,
        datatype          TEXT NOT NULL,
        value             TEXT,
        PRIMARY KEY (name)
    );
    """

    SCHEMA_INIT = """
        INSERT INTO plc_tests VALUES ('SENSOR1',   'int', '1');
        INSERT INTO plc_tests VALUES ('SENSOR2',   'float', '22.2');
        INSERT INTO plc_tests VALUES ('SENSOR3',   'int', '5');
        INSERT INTO plc_tests VALUES ('ACTUATOR2', 'int', '2');
    """

    def test_set_get(self, sleep=0.3):

        try:
            os.remove(TestPLC.PATH)
        except OSError:
            pass

        SQLiteState._create(TestPLC.PATH, TestPLC.SCHEMA)
        SQLiteState._init(TestPLC.PATH, TestPLC.SCHEMA_INIT)

        class ToyPLC(PLC):

            def pre_loop(self):

                eq_(self.set(('SENSOR1',), '10'), '10')
                eq_(self.get(('SENSOR1',)), '10')
                eq_(self.get(('SENSOR2',)), '22.2')
                eq_(self.get(('SENSOR3',)), '5')
                time.sleep(sleep)

                try:
                    self.get(2.22)
                except TypeError as error:
                    print 'get what is a float: ', error

                try:
                    self.set(2, 5)
                except TypeError as error:
                    print 'set what is an integer: ', error

        plc = ToyPLC(
            name=TestPLC.NAME,
            state=TestPLC.STATE,
            protocol=TestPLC.PROTOCOL)

        SQLiteState._delete(TestPLC.PATH)
