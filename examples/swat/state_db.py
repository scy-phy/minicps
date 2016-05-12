import os
import sqlite3

# TODO: delete constants and use other names
from constants import logger
from constants import init_db
from constants import STATE_DB_PATH, SCHEMA, DATATYPES

# TODO: use high level functions

# used to debug
from constants import read_statedb, read_single_statedb, update_statedb


# TODO: move to state.py
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
    """
    Manage swat state db (create, init fields, init value and optionally
    remove it).

    FIT values are assumed constant (either 0 or a fixed value taken from the
    SWaT spec).
    """

    # remove_db(STATE_DB_PATH)

    db_is_new = not os.path.exists(STATE_DB_PATH)
    if db_is_new:
        create_db(STATE_DB_PATH, SCHEMA)
        init_db(STATE_DB_PATH, DATATYPES)

    # SPHINX_SWAT_TUTORIAL SET LIT101DB
    # update_statedb('1198', 'AI_LIT_101_LEVEL')
    update_statedb('798', 'AI_LIT_101_LEVEL')
    # update_statedb('498', 'AI_LIT_101_LEVEL')
    # update_statedb('248', 'AI_LIT_101_LEVEL')
    # SPHINX_SWAT_TUTORIAL END SET LIT101DB

    update_statedb('710', 'AI_LIT_301_LEVEL')

    update_statedb('1', 'DO_P_101_START')

    update_statedb('1', 'DO_MV_101_OPEN')
    update_statedb('0', 'DO_MV_101_CLOSE')

    update_statedb('2.55', 'AI_FIT_101_FLOW')
    update_statedb('2.45', 'AI_FIT_201_FLOW')

    update_statedb('1', 'DO_MV_201_OPEN')
    update_statedb('0', 'DO_MV_201_CLOSE')

    logger.info('DB - Initial values set')
