"""
toy init.py

Run this script just once to create and init the sqlite table.
"""

from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT
from sqlite3 import OperationalError

if __name__ == "__main__":

    try:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)
        print "{} successfully created.".format(PATH)
    except OperationalError:
        print "{} already exists.".format(PATH)
