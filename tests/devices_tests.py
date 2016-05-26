"""
devices tests
"""

import time
import sys
import os

from minicps.devices import Device, PLC, HMI
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
        'mode': 0,
        'server': '',
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

    def test_validate_device_name(self):

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
                state={'name': 'table_name'},
                protocol=TestDevice.PROTOCOL)
        except KeyError as error:
            print 'state has less than 2 keys: ', error

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
                    'name': 0},
                protocol=TestDevice.PROTOCOL)
        except TypeError as error:
            print 'state has integer values: ', error

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

    def test_validate_protocol(self):

        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol='protocol')
        except TypeError as error:
            print 'protocol is string: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={})
        except KeyError as error:
            print 'protocol is an empty dict: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={
                    'name': 'enip', 'mode': 0, 'server': '',
                    'too': 'much'})
        except KeyError as error:
            print 'protocol has more than 3 keys: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={'name': 'enip', 'mode': 0})
        except KeyError as error:
            print 'protocol has less than 3 keys: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={
                    'name': 'enip', 'mode': 0, 'bla': ''})
        except KeyError as error:
            print 'protocol has a wrong key: ', error

        # protocol['name']
        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={
                    'name': 1, 'mode': 0, 'server': ''})
        except TypeError as error:
            print 'protocol name is not a string: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={
                    'name': 'wow', 'mode': 0, 'server': ''})
        except ValueError as error:
            print 'protocol has an unsupported name: ', error

        # protocol['mode']
        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={
                    'name': 'enip', 'mode': 0.3, 'server': ''})
        except TypeError as error:
            print 'protocol mode is a float: ', error

        try:
            device = Device(
                name=TestDevice.NAME,
                state=TestDevice.STATE,
                protocol={
                    'name': 'enip', 'mode': -3, 'server': ''})
        except ValueError as error:
            print 'protocol mode is a negative int: ', error

        # protocol['server'] TODO
        # protocol['client'] TODO

    def test_validate_disk(self):

        pass

    def test_validate_memory(self):

        pass


class TestPLC():

    NAME = 'plc_tests'
    PATH = 'temp/plc_tests.sqlite'
    STATE = {
        'path': PATH,
        'name': NAME
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 0,
        'server': '',
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


class TestHMI():

    NAME = 'hmi_tests'
    PATH = 'temp/hmi_tests.sqlite'
    STATE = {
        'path': PATH,
        'name': NAME
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 0,
        'server': '',
    }

    SCHEMA = """
    CREATE TABLE hmi_tests (
        name              TEXT NOT NULL,
        datatype          TEXT NOT NULL,
        value             TEXT,
        PRIMARY KEY (name)
    );
    """

    SCHEMA_INIT = """
        INSERT INTO hmi_tests VALUES ('SENSOR1',   'int', '1');
        INSERT INTO hmi_tests VALUES ('SENSOR2',   'float', '22.2');
        INSERT INTO hmi_tests VALUES ('SENSOR3',   'int', '5');
        INSERT INTO hmi_tests VALUES ('ACTUATOR2', 'int', '2');
    """

    def test_set_get(self, sleep=0.3):

        try:
            os.remove(TestHMI.PATH)
        except OSError:
            pass

        SQLiteState._create(TestHMI.PATH, TestHMI.SCHEMA)
        SQLiteState._init(TestHMI.PATH, TestHMI.SCHEMA_INIT)

        class ToyHMI(HMI):

            def main_loop(self):

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

        hmi = ToyHMI(
            name=TestHMI.NAME,
            state=TestHMI.STATE,
            protocol=TestHMI.PROTOCOL)

        SQLiteState._delete(TestHMI.PATH)
