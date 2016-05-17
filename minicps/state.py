"""
state.py
"""

import sqlite3
# import redis
# import pymongo


class State(object):

    """Base class."""

    def __init__(self, state):
        """Init a State object.

        :state: dict passed from Device obj
        """

        # TODO: public or private?
        self.state = state

    def _create(self):
        """Create a state instance.

        Eg: create a MySQL db.

        """
        pass

    def _init(self):
        """Initialize a state instance.

        Eg: init MySQL db tables.

        """
        pass

    def _delete(self):
        """Create a state instance.

        Eg: remove a MySQL db.

        """
        pass

    def _set(self, what, value):
        """Set (write) a state value.

        :what: tuple with field identifiers
        :value: value
        """

        print "set: please override"

    def _get(self, what):
        """Get (read) a state value.

        :what: (Immutable) tuple with field identifiers
        """

        print "get: please override"


# sqlite {{{1
# TODO: extend prepared statement to every SQL backend
class SQLiteState(State):

    """SQLite state manager.

    IT uses prepared statemetns to speed-up queries executions and protect
    against SQL injection attacks.

    Client has to use ordered primary key fields to use get and set.
    """

    def __init__(self, state):

        super(SQLiteState, self).__init__(state)

        self._name = self.state['name']
        self._path = self.state['path']
        self._value = 'value'  # TODO: client can override value field

        self._init_what()
        self._init_get_query()

    def _init_what(self):
        """Save a ordered tuple of pk field names in self._what."""

        # https://sqlite.org/pragma.html#pragma_table_info
        query = "PRAGMA table_info(%s)" % self._name
        # print "DEBUG query: ", query

        with sqlite3.connect(self._path) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                table_info = cursor.fetchall()
                # print "DEBUG table_info: ", table_info

                # last tuple element
                pks = []
                for field in table_info:
                    if field[-1] > 0:
                        # print 'DEBUG pk field: ', field
                        pks.append(field)

                if not pks:
                    print "ERROR: please provide at least 1 primary key"
                else:
                    # sort by pk order
                    pks.sort(key=lambda x: x[5])
                    print 'DEBUG sorted pks: ', pks

                    what_list = []
                    for pk in pks:
                        what_list.append(pk[1])
                    print 'DEBUG what list: ', what_list

                    self._what = tuple(what_list)
                    print 'DEBUG self._what: ', self._what

            except sqlite3.Error, e:
                print('ERROR: %s: ' % e.args[0])

    def _init_get_query(self):
        """Use prepared statement."""

        get_query = 'SELECT %s FROM %s WHERE %s = ?' % (
            self._value,
            self._name,
            self._what[0])

        # for composite pk
        for pk in self._what[1:]:
            get_query += ' AND %s = ?' % (
                pk)

        print 'DEBUG get_query:', get_query
        self._get_query = get_query

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

        if what != self._what:
            print "ERROR: search tuple different from %s" % self._what

    def _get(self, what):

        # if what != self._what:
        #     print "ERROR: search tuple different from %s" % self._what

        with sqlite3.connect(self._path) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(self._get_query, what)
                record = cursor.fetchone()
                return record

            except sqlite3.Error, e:
                print('ERROR: %s: ' % e.args[0])


# redis {{{1
class RedisState(State):

    """Redis state manager."""

    pass

# mongodb {{{1

# spreasheet/csv {{{1
