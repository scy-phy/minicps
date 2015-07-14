"""
PLC1 multithreaded simulation

plc_db init the db and set event_db. 

enip_server wait for event_db to be setted within a timeout and fire an
Exception in case of timeout (non-blocking).

enip_client bla bla bla

plc_logic bla bla bla

"""
import sqlite3
import os
import time

from constants import logger, 
from constants import P1_TAGS, LIT_101, LIT_301, FIT_201
from constants import db2cpppo


if __name__ == '__main__':
    """
    plc1 main loop
    """

    # init the ENIP server
    db_tags = P1_TAGS.values()

    cpppo_tags = db2cpppo(db_tags)

    # synch with plc2, plc3
    time.sleep(1)

    # look a Stridhar graph
    while True:
        logger.debug("plc1 main loop")
        break

