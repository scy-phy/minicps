"""
state_tests.py
"""

import os

from minicps.state import SQLiteState

SCHEMA = """
        create table test (
            SCOPE             text not null,
            NAME              text not null,
            DATATYPE          text not null,
            VALUE             text,
            PID               integer not null,
            PRIMARY KEY (SCOPE, NAME, PID)
        );
        """


def test_SQLiteState():

    SCHEMA = """
            create table test (
                SCOPE             text not null,
                NAME              text not null,
                DATATYPE          text not null,
                VALUE             text,
                PID               integer not null,
                PRIMARY KEY (SCOPE, NAME, PID)
            );
            """

    sqlite_state = SQLiteState()

    sqlite_state._create_state('/tmp/test-db.sqlite', SCHEMA)
