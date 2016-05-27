"""
toy init.py

Run this script just once to create and init the sqlite table.
"""

from minicps.state import SQLiteState

from utils import PATH, SCHEMA, SCHEMA_INIT

SQLiteState._create(PATH, SCHEMA)
SQLiteState._init(PATH, SCHEMA_INIT)
