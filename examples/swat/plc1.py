"""
PLC1 multithreaded simulation

enip_server bla bla bla

enip_client bla bla bla

plc_db bla bla bla

plc_logic bla bla bla
"""
import sqlite3
import os
import threading as th
import time

from constants import logger
from constants import create_db, remove_db, init_db
from constants import PLC1_DB_PATH, SCHEMA, DATATYPES


def enip_server():
    """
    enip_server thread

    :arg1: TODO
    :returns: TODO

    """
    name = th.currentThread().getName()
    logger.debug("Starting %s" % (name))

    time.sleep(1)

    logger.debug("Exiting %s" % (name))


def enip_client():
    """
    enip_client thread

    :arg1: TODO
    :returns: TODO

    """
    name = th.currentThread().getName()
    logger.debug("Starting %s" % (name))

    time.sleep(1)

    logger.debug("Exiting %s" % (name))


def plc_db(db_path, schema, datatypes):
    """
    db thread

    :arg1: TODO
    :returns: TODO

    """
    name = th.currentThread().getName()
    logger.debug("Starting %s" % (name))

    time.sleep(1)
    print db_path, schema, datatypes

    logger.debug("Exiting %s" % (name))


def plc_logic():
    """
    logic thread


    """
    name = th.currentThread().getName()
    logger.debug("Starting %s" % (name))

    time.sleep(1)

    logger.debug("Exiting %s" % (name))





if __name__ == '__main__':
    """
    args are passed in a tuple (var_name1, var_name2,)
    """

    # Init threads
    threads = {}
    threads['enip_server'] = th.Thread(name='enip_server', target=enip_server)
    threads['enip_client'] = th.Thread(name='enip_client', target=enip_client)
    threads['plc_db'] = th.Thread(name='plc_db',
            target=plc_db, 
            args=(PLC1_DB_PATH, SCHEMA, DATATYPES))
    threads['plc_logic'] = th.Thread(name='plc_logic', target=plc_logic)

    # Start threads
    threads['enip_server'].start()
    threads['enip_client'].start()
    threads['plc_db'].start()
    threads['plc_logic'].start()
