#!/usr/bin/env python

"""
swat-s1 init.py

Run this script just once to create and init the sqlite table.
"""

from minicps.state import SQLiteState
from utils import PATH, SCHEMA, DATATYPES

import sqlite3


def init_db(db_path, datatypes):
    """Init a sqlite db from RSLogix 5000 exported csv files.

    It uses prepared statement.

    :db_path: full or relative path to the file.db
    :datatypes: list of DATATYPES
    """

    with sqlite3.connect(db_path) as conn:
        try:
            for i in range(1, 7):
                plc_filename = "real-tags/P%d-Tags.CSV" % i
                with open(plc_filename, "rt") as f:
                    text = f.read()
                    tags = text.split('\n')  # new-line splitted list of tags
                    cursor = conn.cursor()
                    for tag in tags[7:-1]:
                        fields = tag.split(',')
                        datatype = fields[4][1:-1]  # extract BOOL from "BOOL"
                        if datatype in datatypes:
                            scope = fields[1]
                            if not scope:
                                scope = 'NO'
                            name = fields[2]
                            print 'DEBUG: name: %s  datatype: %s' % (
                                name, datatype)
                            par_sub = (scope, name, datatype, i)
                            cmd = """
                            INSERT INTO swat_s1 (scope, name, datatype, pid)
                            VALUES (?, ?, ?, ?)
                            """
                            cursor.execute(cmd, par_sub)

                    conn.commit()
        except sqlite3.Error as error:
            print 'ERROR swat-s1 init %s: ', error


if __name__ == "__main__":

    SQLiteState._create(PATH, SCHEMA)
    init_db(PATH, DATATYPES)
