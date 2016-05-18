"""
state_tests.py

SQLite uses text datatype instead of varchar.
"""

import os

from minicps.state import SQLiteState

from nose.tools import eq_

# TODO: change to /tmp when install SQLitesutdio in ubuntu
PATH = "temp/state_test_db.sqlite"
NAME = 'state_test'
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
    INSERT INTO state_test VALUES ('SENSOR1',   'int', '0', 1);
    INSERT INTO state_test VALUES ('SENSOR2',   'float', '0.0', 1);
    INSERT INTO state_test VALUES ('SENSOR3',   'int', '1', 1);
    INSERT INTO state_test VALUES ('SENSOR3',   'int', '2', 2);
    INSERT INTO state_test VALUES ('ACTUATOR1', 'int', '1', 1);
    INSERT INTO state_test VALUES ('ACTUATOR2', 'int', '0', 1);
"""


def test_SQLiteStateClassMethods():

    try:
        os.remove(PATH)

    except OSError as e:
        print 'TEST %s do NOT exists in the filesystem.'

    finally:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)
        SQLiteState._delete(PATH)


# class TestSQLiteState():

    # def test_SQLiteState(self):

    #     state = SQLiteState(STATE)

    #     print
    #     eq_(state._get(('SENSOR3', 1)), '1')
    #     eq_(state._get(('SENSOR3', 2)), '2')

    #     eq_(state._set(('SENSOR1', 1), '10'), '10')
    #     eq_(state._get(('SENSOR1', 1)), '10')
