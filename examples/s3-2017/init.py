#!/usr/bin/env python

"""
init.py

Run this script just once to create and init the sqlite table.
"""

from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT
from utils import PATH_SWAT, SCHEMA_SWAT, SCHEMA_INIT_SWAT


if __name__ == "__main__":

    # NOTE: wadi.sqlite
    SQLiteState._create(PATH, SCHEMA)
    SQLiteState._init(PATH, SCHEMA_INIT)

    # NOTE: enip.sqlite
    SQLiteState._create(PATH_SWAT, SCHEMA_SWAT)
    SQLiteState._init(PATH_SWAT, SCHEMA_INIT_SWAT)

