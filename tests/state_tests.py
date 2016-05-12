"""
state_tests.py
"""

import os

from minicps.state import _create_sqlite_db


def test_create_sqlite_db():

    schema = """
            create table test (
                SCOPE             text not null,
                NAME              text not null,
                DATATYPE          text not null,
                VALUE             text,
                PID               integer not null,
                PRIMARY KEY (SCOPE, NAME, PID)
            );
            """

    os.remove("/tmp/database.sqlite")
    db_name = '/tmp/database.sqlite'
    _create_sqlite_db(db_name, schema)
