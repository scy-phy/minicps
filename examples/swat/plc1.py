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
import threading as th
import time

from constants import logger, wait_for_event_timeout
from constants import create_db, remove_db, init_db
from constants import PLC1_DB_PATH, SCHEMA, DATATYPES


def plc_db(db_path, schema, datatypes, event_db):
    """
    plc_db thread

    :db_path: path to the plc db
    :schema: string containing the sql db schema
    :datatypes: list containing the datatypes to filter in
    :event_db: tuple (event_obj, event_name) used to synch with other threads

    """
    logger.debug("Starting")

    time.sleep(2)  # simulate db setting time
    event_db[0].set()

    logger.debug("%s setted" % event_db[1])

    logger.debug("Exiting")


def enip_server(event_db):
    """
    enip_server thread

    :event_db: tuple (event_obj, event_name) used to synch with other threads

    """
    logger.debug("Starting")

    wait_for_event_timeout(event_db[0], 4, event_db[1])

    logger.debug("Exiting")


def enip_client():
    """
    enip_client thread

    :arg1: TODO
    :returns: TODO

    """
    name = th.currentThread().getName()
    logger.debug("Starting")

    time.sleep(1)

    logger.debug("Exiting")


def plc_logic():
    """
    Maybe move it in the main thread ????
    logic thread


    """
    name = th.currentThread().getName()
    logger.debug("Starting")

    time.sleep(1)

    logger.debug("Exiting")


if __name__ == '__main__':
    """
    main thread
    """

    # Init events: use tuple to attach a name to Event
    event_db = (th.Event(), 'event_db')

    # Init threads
    threads = {}

    threads['enip_server'] = th.Thread(name='enip_server',
                                       target=enip_server,
                                       args=(event_db,))

    threads['enip_client'] = th.Thread(name='enip_client',
                                       target=enip_client,
                                       args=())

    threads['plc_db'] = th.Thread(name='plc_db',
                                  target=plc_db, 
                                  args=(PLC1_DB_PATH, SCHEMA, DATATYPES,
                                      event_db,))

    threads['plc_logic'] = th.Thread(name='plc_logic', target=plc_logic)

    # Start threads
    try:
        threads['plc_db'].start()
        threads['enip_server'].start()
        # threads['enip_client'].start()
        # threads['plc_logic'].start()

    except Exception as e:
        logger.error(e.message)
        exit(1)

    finally:
        exit(0)
