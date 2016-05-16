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

    def _create(self):
        """Create a state instance.

        eg: create a MySQL db.

        """
        pass

    def _init(self):
        """Initialize a state instance.

        eg: init MySQL db tables.

        """
        pass

    def _delete(self):
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
    def _create(self, db_name, schema):
        """Create a sqlite db given a schema.

        OVERWRITES db_name path by default.

        :db_name: full or relative paths are supported
        :schema: str containing the schema
        """

        with sqlite3.connect(db_name) as conn:
            conn.executescript(schema)

    def _init(self, db_name, init_cmd):
        """Initialize a sqlite database given commands.

        :db_name: full or relative paths are supported
        :init_cmd: initialization commands
        """

        with sqlite3.connect(db_name) as conn:
            conn.executescript(init_cmd)

    def _set(self, what, value):

        print "set_sqlite: TODO"

    def _get(self, value):

        print "get_sqlite: TODO"

# redis {{{1

# mongodb {{{1
