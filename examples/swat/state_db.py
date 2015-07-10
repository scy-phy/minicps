import os
import sqlite3

from constants import create_db, remove_db, init_db, STATE_DB_PATH, logger

SCHEMA = """
        create table Tag (
            SCOPE             text not null,
            NAME              text not null,
            DATATYPE          text not null,
            VALUE             text,
            PID               integer not null,
            PRIMARY KEY (SCOPE, NAME, PID)
        );
        """
        # VALUE             text default '',

# state_db specific filters, functions and aggregators
DATATYPES = [
        'INT',
        'DINT',
        'BOOL',
        'REAL',
]

class Aggregate(object):
    """Docstring for Aggregate. """

    def __init__(self):
        """TODO: to be defined1. """


class UserDefinedType(object):
    """
    Used to store in a single record multiple values.
    
    A UDT cannot store: Axis, MESSAGE, MOTION, GROUP, SFC_STEP, SFC_ACTION,
    SFC_STOP, PHASE, ALARM_ANALOG, ALARM_DIGITAL data types
    
    """

    def __init__(self):
        """TODO: defined1. """


def db_fun(arg1):
    """TODO: Docstring for db_fun.

    :arg1: TODO
    :returns: TODO

    """
    pass

        
if __name__ == '__main__':

    remove_db(STATE_DB_PATH)

    db_is_new = not os.path.exists(STATE_DB_PATH)
    if db_is_new:
        create_db(STATE_DB_PATH, SCHEMA)

    init_db(STATE_DB_PATH, DATATYPES)
