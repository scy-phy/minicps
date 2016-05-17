"""
state_tests.py
"""

import os

from minicps.state import SQLiteState

from nose.tools import eq_


def test_SQLiteState():

    # TODO: change to /tmp when install SQLitesutdio in ubuntu
    PATH = "temp/state_test_db.sqlite"
    NAME = 'state_test'

    STATE = {
        'name': NAME,
        'path': PATH
    }

    # sqlite use text instead of VARCHAR
    # TODO: datatype field is necessary?
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

    print
    state = SQLiteState(STATE)

    # os.remove(PATH)
    # state._create(PATH, SCHEMA)
    # state._init(PATH, SCHEMA_INIT)
    # state._delete()

    eq_(state._get(('SENSOR3', 1))[0], '1')
    eq_(state._get(('SENSOR3', 2))[0], '2')
