"""
toy init.py

Run this script just once to create and init the sqlite table.
"""

import os
import sys

from minicps.state import SQLiteState

# TODO: find a nicer way to manage examples path
sys.path.append(os.getcwd())
from examples.toy.utils import PATH, SCHEMA, SCHEMA_INIT

SQLiteState._create(PATH, SCHEMA)
SQLiteState._init(PATH, SCHEMA_INIT)
