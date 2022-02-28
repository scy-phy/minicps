"""
devices tests
"""

import time
import sys
import os

from minicps.devices import Device, PLC, HMI, Tank, SCADAServer, RTU
from minicps.states import SQLiteState

from nose.tools import eq_, raises
from nose.plugins.skip import SkipTest

# NOTE: currently testing only set and get
# TODO: find a way to test also send and received outside network emulaiton

class TestDevice():

    """TestDevice: build and input validation tests.

    Reading this tests is a good way to review the MiniCPS APIs for the
    physical process and network layer.

    """

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

    @raises(TypeError)
    def test_device_name_is_int(self):

        device = Device(
            name=1,
            state=TestDevice.STATE,
            protocol=TestDevice.PROTOCOL)

    @raises(ValueError)
    def test_device_name_is_empty_string(self):

        device = Device(
            name='',
            state=TestDevice.STATE,
            protocol=TestDevice.PROTOCOL)

    @raises(TypeError)
    def test_device_state_is_string(self):

        device = Device(
            name=TestDevice.NAME,
            state='state',
            protocol=TestDevice.PROTOCOL)

    @raises(KeyError)
    def test_device_state_empty_dict(self):

        device = Device(
            name=TestDevice.NAME,
            state={},
            protocol=TestDevice.PROTOCOL)

    @raises(KeyError)
    def test_device_state_more_than_two_keys(self):

        device = Device(
            name=TestDevice.NAME,
            state={
                'name': 'table_name', 'path': '/path.db',
                'wrong': 'key-val'},
            protocol=TestDevice.PROTOCOL)

    @raises(KeyError)
    def test_device_state_less_than_two_keys(self):

        device = Device(
            name=TestDevice.NAME,
            state={'name': 'table_name'},
            protocol=TestDevice.PROTOCOL)

    @raises(KeyError)
    def test_device_state_wrong_key(self):

        device = Device(
            name=TestDevice.NAME,
            state={
                'path': '/bla',
                'bla': 'table_name'},
            protocol=TestDevice.PROTOCOL)

    @raises(TypeError)
    def test_device_state_integer_values(self):

        device = Device(
            name=TestDevice.NAME,
            state={
                'path': 0,
                'name': 0},
            protocol=TestDevice.PROTOCOL)

    @raises(ValueError)
    def test_device_state_unsupported_path_extension(self):

        device = Device(
            name=TestDevice.NAME,
            state={
                'path': '/not/supported.ext',
                'name': 'table_name'},
            protocol=TestDevice.PROTOCOL)


    @raises(TypeError)
    def test_device_protocol_is_string(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol='protocol')

    @raises(KeyError)
    def test_device_protocol_empty_dict(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={})

    @raises(KeyError)
    def test_device_protocol_more_than_three_keys(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={
                'name': 'enip', 'mode': 0, 'server': '',
                'too': 'much'})

    @raises(KeyError)
    def test_device_protocol_less_than_three_keys(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={'name': 'enip', 'mode': 0})

    @raises(KeyError)
    def test_device_protocol_wrong_key(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={
                'name': 'enip', 'mode': 0, 'bla': ''})

    @raises(TypeError)
    def test_device_protocol_name_not_string(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={
                'name': 1, 'mode': 0, 'server': ''})

    @raises(ValueError)
    def test_device_protocol_name_unsupported_name(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={
                'name': 'wow', 'mode': 0, 'server': ''})

    @raises(TypeError)
    def test_device_protocol_mode_float(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={
                'name': 'enip', 'mode': 0.3, 'server': ''})

    @raises(ValueError)
    def test_device_protocol_mode_negative_int(self):

        device = Device(
            name=TestDevice.NAME,
            state=TestDevice.STATE,
            protocol={
                'name': 'enip', 'mode': -3, 'server': ''})

        # protocol['server'] TODO
        # protocol['client'] TODO

    def test_validate_disk(self):

        pass

    def test_validate_memory(self):

        pass


class TestTank():

    """TestTank: device with state capability."""

    NAME = 'tank_tests'
    PATH = 'temp/tank_tests.sqlite'
    STATE = {
        'path': PATH,
        'name': NAME
    }
    PROTOCOL = None

    SCHEMA = """
    CREATE TABLE tank_tests (
        name              TEXT NOT NULL,
        datatype          TEXT NOT NULL,
        value             TEXT,
        PRIMARY KEY (name)
    );
    """

    SCHEMA_INIT = """
        INSERT INTO tank_tests VALUES ('SENSOR1',   'int', '1');
        INSERT INTO tank_tests VALUES ('SENSOR2',   'float', '22.2');
        INSERT INTO tank_tests VALUES ('SENSOR3',   'int', '5');
        INSERT INTO tank_tests VALUES ('ACTUATOR2', 'int', '2');
    """

    SECTION = 1.5  # m^2
    FIT = 2.55  # m^3/h
    INFLOWS = [
        [False, FIT, 0.5],
    ]
    OUTFLOWS = [
        [False, FIT, 0.5],
        [False, FIT, 0.3],
    ]
    THRESHOLDS = {
        'LL': 250.0,
        'L': 500.0,
        'H': 800.0,
        'HH': 1200.0,
    }
    LEVEL = 500.0

    def test_init(self):

        try:
            os.remove(TestTank.PATH)
        except OSError:
            pass

        SQLiteState._create(TestTank.PATH, TestTank.SCHEMA)
        SQLiteState._init(TestTank.PATH, TestTank.SCHEMA_INIT)

        tank = Tank(
            name=TestTank.NAME,
            state=TestTank.STATE,
            protocol=TestTank.PROTOCOL,

            section=TestTank.SECTION,
            level=TestTank.LEVEL
        )

        SQLiteState._delete(TestTank.PATH)

    @SkipTest
    def test_set_get(self, sleep=0.3):

        try:
            os.remove(TestTank.PATH)
        except OSError:
            pass

        SQLiteState._create(TestTank.PATH, TestTank.SCHEMA)
        SQLiteState._init(TestTank.PATH, TestTank.SCHEMA_INIT)

        class ToyTank(Tank):

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

        # TODO: add atts
        tank = ToyTank(
            name=TestTank.NAME,
            state=TestTank.STATE,
            protocol=TestTank.PROTOCOL)

        SQLiteState._delete(TestTank.PATH)


class TestPLC():

    """TestPLC: device with state and protocol client/server capabilites."""

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

    """TestHMI: device with state and protocol client capabilites."""

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


class TestSCADAServer():

    """TestSCADAServer: device with state and protocol client/server capabilites."""

    NAME = 'scadaserver_tests'
    PATH = 'temp/scadaserver_tests.sqlite'
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
    CREATE TABLE scadaserver_tests (
        name              TEXT NOT NULL,
        datatype          TEXT NOT NULL,
        value             TEXT,
        PRIMARY KEY (name)
    );
    """

    SCHEMA_INIT = """
        INSERT INTO scadaserver_tests VALUES ('SENSOR1',   'int', '1');
        INSERT INTO scadaserver_tests VALUES ('SENSOR2',   'float', '22.2');
        INSERT INTO scadaserver_tests VALUES ('SENSOR3',   'int', '5');
        INSERT INTO scadaserver_tests VALUES ('ACTUATOR2', 'int', '2');
    """

    def test_set_get(self, sleep=0.3):

        try:
            os.remove(TestSCADAServer.PATH)
        except OSError:
            pass

        SQLiteState._create(TestSCADAServer.PATH, TestSCADAServer.SCHEMA)
        SQLiteState._init(TestSCADAServer.PATH, TestSCADAServer.SCHEMA_INIT)

        class ToySCADAServer(SCADAServer):

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

        scadaserver = ToySCADAServer(
            name=TestSCADAServer.NAME,
            state=TestSCADAServer.STATE,
            protocol=TestSCADAServer.PROTOCOL)

        SQLiteState._delete(TestSCADAServer.PATH)


class TestRTU():

    """TestRTU: device with state and protocol client/server capabilites."""

    NAME = 'rtu_tests'
    PATH = 'temp/rtu_tests.sqlite'
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
    CREATE TABLE rtu_tests (
        name              TEXT NOT NULL,
        datatype          TEXT NOT NULL,
        value             TEXT,
        PRIMARY KEY (name)
    );
    """

    SCHEMA_INIT = """
        INSERT INTO rtu_tests VALUES ('SENSOR1',   'int', '1');
        INSERT INTO rtu_tests VALUES ('SENSOR2',   'float', '22.2');
        INSERT INTO rtu_tests VALUES ('SENSOR3',   'int', '5');
        INSERT INTO rtu_tests VALUES ('ACTUATOR2', 'int', '2');
    """

    def test_set_get(self, sleep=0.3):

        try:
            os.remove(TestRTU.PATH)
        except OSError:
            pass

        SQLiteState._create(TestRTU.PATH, TestRTU.SCHEMA)
        SQLiteState._init(TestRTU.PATH, TestRTU.SCHEMA_INIT)

        class ToyRTU(RTU):

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

        scadaserver = ToyRTU(
            name=TestRTU.NAME,
            state=TestRTU.STATE,
            protocol=TestRTU.PROTOCOL)

        SQLiteState._delete(TestRTU.PATH)
