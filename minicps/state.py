"""
state.py
"""

import sqlite3
# import redis
# import pymongo


# public {{{1
# TODO: decide name
def set(arg1):
    """Set a value.

    :arg1: TODO
    :returns: TODO

    """
    pass


def get(arg1):
    """Get a value.

    :arg1: TODO
    :returns: TODO

    """
    pass


# sqlite {{{1
# TODO check :memory: opt to save db in main memory"
def _create_sqlite_db(db_name, schema):
    """Create a sqlite db given a schema.

    Remove old file first if you want to reuse a path

    :db_name: full or relative paths are supported
    :schema: str containing the schema
    """

    with sqlite3.connect(db_name) as conn:
        conn.executescript(schema)

# redis {{{1

# mongodb {{{1
