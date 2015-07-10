import os
import sqlite3
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from constants import show_tags

db_path = 'examples/swat/state.db'
schema = """
        create table Tag (
            SCOPE             text not null,
            NAME              text not null,
            DATATYPE          text not null,
            VALUE             text,
            PID               integer not null,
            PRIMARY KEY (SCOPE, NAME, PID)
        );
        """
        # VALUE             text default '',

datatypes = [
        'INT',
        'DINT',
        'BOOL',
        'REAL',
]

class Aggregate(object):
    """Docstring for Aggregate. """

    def __init__(self):
        """TODO: to be defined1. """


class UserDefinedType(object):
    """
    Used to store in a single record multiple values.
    
    A UDT cannot store: Axis, MESSAGE, MOTION, GROUP, SFC_STEP, SFC_ACTION,
    SFC_STOP, PHASE, ALARM_ANALOG, ALARM_DIGITAL data types
    
    """

    def __init__(self):
        """TODO: defined1. """


def db_fun(arg1):
    """TODO: Docstring for db_fun.

    :arg1: TODO
    :returns: TODO

    """
    pass


def create(db_path):
    """TODO: Docstring for init.
    :returns: TODO

    """
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)
        logger.info('Created schema')


def remove(db_path):
    """TODO: Docstring for init.
    :returns: TODO

    """
    logger.info('Removing %s' % db_path)
    try:
        os.remove(db_path)
    except Exception, err:
        logger.warning(err)
    

def init(db_path):
    """
    Import only

    :db_path: TODO
    :returns: TODO

    """
    with sqlite3.connect(db_path) as conn:
        logger.info('Init tables')

        for i in range(1, 7):
            plc_filename = "examples/swat/real-tags/P%d-Tags.CSV" % i
            with open(plc_filename, "rt") as f:

                text = f.read()
                tags = text.split('\n')  # new-line splitted list of tags

                cursor = conn.cursor()

                for tag in tags[7:-1]:
                    fields = tag.split(',')
                    datatype = fields[4][1:-1]  # extract BOOL from "BOOL" 
                    if datatype in datatypes:
                        scope = fields[1]
                        name = fields[2]
                        logger.debug('NAME: %s  DATATYPE: %s' % (name,
                            datatype))
                        cmd = """
                        INSERT INTO Tag (SCOPE, NAME, DATATYPE, PID)
                        VALUES ('%s', '%s', '%s', %d)
                        """ % (scope, name, datatype, i)
                        cursor.execute(cmd)

                conn.commit()

        
if __name__ == '__main__':

    remove(db_path)

    db_is_new = not os.path.exists(db_path)
    if db_is_new:
        create(db_path)

    init(db_path)
