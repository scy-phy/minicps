"""
state_tests.py

SQLite uses text datatype instead of varchar.
"""

import os

from minicps.state import SQLiteState

from nose.tools import eq_
from nose.plugins.skip import SkipTest

# TODO: change to /tmp when install SQLitesutdio in ubuntu

PATH = "temp/state_tests.sqlite"
NAME = 'state_tests'
STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE state_tests (
    name              TEXT NOT NULL,
    datatype          TEXT NOT NULL,
    value             TEXT,
    PRIMARY KEY (name)
);
"""

SCHEMA_INIT = """
    INSERT INTO state_tests VALUES ('SENSOR1',   'int', '1');
    INSERT INTO state_tests VALUES ('SENSOR2',   'float', '22.2');
    INSERT INTO state_tests VALUES ('ACTUATOR2', 'int', '2');
"""


def test_SQLiteStateClassMethods():

    try:
        os.remove(PATH)

    except OSError as error:
        pass
        # print '%s do NOT exists: ', error

    finally:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)
        SQLiteState._delete(PATH)


class TestSQLiteState():

    def test_NoPk(self):

        PATH = "temp/no_pk.sqlite"
        NAME = 'no_pk'
        STATE = {
            'name': NAME,
            'path': PATH
        }

        SCHEMA = """
        CREATE TABLE %s (
            name              TEXT NOT NULL,
            datatype          TEXT NOT NULL
        );
        """ % NAME

        SQLiteState._create(PATH, SCHEMA)

        try:
            state = SQLiteState(STATE)

        except ValueError as error:
            print 'schema with no pk: ', error

        finally:
            SQLiteState._delete(PATH)

    def test_OnePk(self):

        PATH = "temp/one_pk.sqlite"
        NAME = 'one_pk'
        STATE = {
            'name': NAME,
            'path': PATH
        }

        SCHEMA = """
        CREATE TABLE %s (
            name              TEXT NOT NULL,
            datatype          TEXT NOT NULL,
            value             INT,
            PRIMARY KEY (name)
        );
        """ % NAME

        SCHEMA_INIT = """
            INSERT INTO one_pk VALUES ('SENSOR1',   'int', 1);
            INSERT INTO one_pk VALUES ('SENSOR2',   'float', 22.2);
            INSERT INTO one_pk VALUES ('ACTUATOR2', 'int', 2);
        """

        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)

        state = SQLiteState(STATE)

        eq_(state._get(('SENSOR1',)), 1)
        eq_(state._set(('SENSOR1',), 5), 5)
        eq_(state._get(('SENSOR1',)), 5)

        SQLiteState._delete(PATH)

    def test_TwoPk(self):

        PATH = "temp/two_pks.sqlite"
        NAME = 'two_pks'
        STATE = {
            'name': NAME,
            'path': PATH
        }

        SCHEMA = """
        CREATE TABLE %s (
            name              TEXT NOT NULL,
            datatype          TEXT NOT NULL,
            value             TEXT,
            pid               INTEGER NOT NULL,
            PRIMARY KEY (name, pid)
        );
        """ % NAME

        SCHEMA_INIT = """
            INSERT INTO two_pks VALUES ('SENSOR1',   'int', '0', 1);
            INSERT INTO two_pks VALUES ('SENSOR2',   'float', '0.0', 1);
            INSERT INTO two_pks VALUES ('SENSOR3',   'int', '1', 1);
            INSERT INTO two_pks VALUES ('SENSOR3',   'int', '2', 2);
            INSERT INTO two_pks VALUES ('ACTUATOR1', 'int', '1', 1);
            INSERT INTO two_pks VALUES ('ACTUATOR2', 'int', '0', 1);
        """

        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)

        state = SQLiteState(STATE)

        eq_(state._get(('SENSOR3', 1)), '1')
        eq_(state._get(('SENSOR3', 2)), '2')

        eq_(state._set(('SENSOR1', 1), '10'), '10')
        eq_(state._get(('SENSOR1', 1)), '10')

        SQLiteState._delete(PATH)
