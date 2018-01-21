#!/usr/bin/env python

"""
s3-2017 init.py

Run this script just once to create and init the sqlite tables.
"""

from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT
from utils import PATH_SWAT, SCHEMA_SWAT, SCHEMA_INIT_SWAT
from sqlite3 import OperationalError


if __name__ == "__main__":

    # NOTE: wadi.sqlite
    try:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)
        print "{} successfully created.".format(PATH)
    except OperationalError:
        print "{} already exists.".format(PATH)

    # NOTE: enip.sqlite
    try:
        SQLiteState._create(PATH_SWAT, SCHEMA_SWAT)
        SQLiteState._init(PATH_SWAT, SCHEMA_INIT_SWAT)
        print "{} successfully created.".format(PATH_SWAT)
    except OperationalError:
        print "{} already exists.".format(PATH_SWAT)

