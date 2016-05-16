"""
state_tests.py
"""

import os

from minicps.state import SQLiteState

# TODO: change to /tmp when install SQLitesutdio in ubuntu
PATH = "temp/state_test_db.sqlite"
SCHEMA = """
create table state_test (
    NAME              text not null,
    DATATYPE          text not null,
    VALUE             text,
    PID               integer not null,
    PRIMARY KEY (NAME, PID)
);
"""
SCHEMA_INIT = """
    INSERT INTO state_test VALUES ('SENSOR1', 'int', '0', 1);
"""


def test_SQLiteState():

    sqlite_state = SQLiteState()

    # os.remove(PATH)
    sqlite_state._create(PATH, SCHEMA)
    sqlite_state._init(PATH, SCHEMA_INIT)
    # sqlite_state._delete()
