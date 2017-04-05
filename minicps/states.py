"""
``states`` module.

MiniCPS uses prepared statements to speed-up the execution of the queries,
and protect the database against SQL injection attacks.
"""

import os
import sqlite3
# import redis
# import pymongo


class State(object):

    """Base class."""

    def __init__(self, state):
        """Init a State object.

        For ``state`` format see the ``devices`` module docstring.

        :param dict state: validated dict passed from a Device instance.
        """

        self._state = state

    @classmethod
    def _create(cls):
        """Create a state instance.

        Eg: create a MySQL db.

        """
        pass

    @classmethod
    def _init(cls):
        """Initialize a state instance.

        Eg: init MySQL db tables.

        """
        pass

    @classmethod
    def _delete(cls):
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
# TODO: single table or multiple tables to separate datatypes
class SQLiteState(State):

    """SQLite state manager.

    SQLite uses TEXT data type instead of VARCHAR.

    Client has to use ordered primary key fields to use get and set.
    """

    def __init__(self, state):

        super(SQLiteState, self).__init__(state)

        self._name = self._state['name']
        self._path = self._state['path']
        self._value = 'value'  # TODO: add it to the device state dict
        self._what = ()

        self._init_what()

        if not self._what:
            raise ValueError('Primary key not found.')
        else:
            self._init_get_query()
            self._init_set_query()

    # TODO check :memory: opt to save db in main memory"
    @classmethod
    def _create(cls, db_name, schema):
        """Create a sqlite db given a schema.

        OVERWRITES db_name path by default.

        :db_name: full or relative paths are supported
        :schema: str containing the schema
        """

        with sqlite3.connect(db_name) as conn:
            conn.executescript(schema)

    @classmethod
    def _init(cls, db_name, init_cmd):
        """Initialize a sqlite database given commands.

        :db_name: full or relative paths are supported
        :init_cmd: initialization commands
        """

        with sqlite3.connect(db_name) as conn:
            conn.executescript(init_cmd)

    @classmethod
    def _delete(cls, db_name):
        """Delete a sqlite database given commands.

        :db_name: full or relative paths are supported
        """

        try:
            os.remove(db_name)

        except OSError as e:
            print 'DEBUG %s do NOT exists in the filesystem.'

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
                    # print 'DEBUG sorted pks: ', pks

                    what_list = []
                    for pk in pks:
                        what_list.append(pk[1])
                    # print 'DEBUG what list: ', what_list

                    self._what = tuple(what_list)
                    # print 'DEBUG self._what: ', self._what

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

    def _init_set_query(self):
        """Use prepared statements."""

        set_query = 'UPDATE %s SET %s = ? WHERE %s = ?' % (
            self._name,
            self._value,
            self._what[0])

        # for composite pk
        for pk in self._what[1:]:
            set_query += ' AND %s = ?' % (
                pk)

        print 'DEBUG set_query:', set_query
        self._set_query = set_query

    # TODO: return result of cursor.execute
    def _set(self, what, value):
        """Returns setted value.

        ``value``'s type is not checked, the client has to specify the correct
        one.

        what_list overwrites the given what tuple,
        eg new what tuple: ``(value, what[0], what[1], ...)``
        """
        what_list = [value]

        for pk in what:
            what_list.append(pk)

        what = tuple(what_list)
        # print 'DEBUG set what: ', what

        with sqlite3.connect(self._path) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(self._set_query, what)
                conn.commit()
                return value

            except sqlite3.Error, e:
                print('_set ERROR: %s: ' % e.args[0])

    def _get(self, what):
        """Returns the first element of the result tuple."""

        with sqlite3.connect(self._path) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(self._get_query, what)
                record = cursor.fetchone()
                return record[0]

            except sqlite3.Error, e:
                print('_get ERROR: %s: ' % e.args[0])


# redis {{{1
class RedisState(State):

    """Redis state manager."""

    pass

# mongodb {{{1

# spreasheet/csv {{{1
