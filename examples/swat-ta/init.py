#!/usr/bin/env python

"""
swat-ta init.py

Run this script just once to create and init the sqlite table.
"""

from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT

def init_state(path, schema, schema_init):

    try:

        SQLiteState._create(path, schema)
        SQLiteState._init(path, schema_init)

    except Exception, e:

        print('swat-ta init.py: {}'.format(e))


if __name__ == "__main__":

    init_state(PATH, SCHEMA, SCHEMA_INIT)

