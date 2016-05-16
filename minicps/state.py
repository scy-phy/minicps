"""
state.py
"""

import sqlite3
# import redis
# import pymongo


# TODO: use State and StateSqlite classes ?
class State(object):

    """Base class."""

    def __init__(self):
        """TODO: to be defined1."""

        pass

    def _create_state(self):
        """Create a state instance.

        eg: create a MySQL db.

        """
        pass

    def _init_state(self):
        """Initialize a state instance.

        eg: init MySQL db tables.

        """
        pass

    def _delete_state(self):
        """Create a state instance.

        eg: remove a MySQL db.

        """
        pass

    def set(self, what, value):
        """Set (write) a state value."""

        print "set: please override"

    def get(self, value):
        """Get (read) a state value."""

        print "get: please override"


# sqlite {{{1
class SQLiteState(State):

    """SQLite state manager."""

    # TODO check :memory: opt to save db in main memory"
    def _create_state(self, db_name, schema):
        """Create a sqlite db given a schema.

        Remove old file first if you want to reuse a path

        :db_name: full or relative paths are supported
        :schema: str containing the schema
        """

        with sqlite3.connect(db_name) as conn:
            conn.executescript(schema)

    def set(self, what, value):
        """Write a SQL record into a sqlite database.

        :arg1: TODO
        :returns: TODO
        """

        print "set_sqlite: TODO"

    def get(self, value):
        """Read a SQL record from a sqlite database.

        :arg1: TODO
        :returns: TODO
        """

        print "get_sqlite: TODO"

# redis {{{1

# mongodb {{{1
