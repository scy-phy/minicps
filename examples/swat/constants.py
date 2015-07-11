"""
SWaT constants

L0 rings are isolated dicts.
L1 network devices are divided into dicts according to the device type.
Devices are mapped with actual SWaT IP, MAC and netmasks.

Dedicated dict map and set each SWaT network level link parameters.
It is also possible to fine tune each link in a single network level.
Network level node numbers are stored in constats eg: L3_NODES, and
they are used for example to distribute evenly CPU processing power.
Dict key mirror where possible mininet device names, indeed it is
super easy to create a new Topo class using those dictionaries.
"""

import sqlite3
import logging
import os


# Threads

def wait_for_event_timeout(event, timeout, ename):
    """
    Use it inside thread to synch (non-blocking)

    :swat_event: Custom threading.Event subclass
    :timeout: wait timeout second before generating an Exception
    :returns: nothing in normal conditions otherwise raise an Exception

    """
    msg = "Waiting for %s to be set" % (ename)
    logging.debug(msg)
    while not event.is_set():
        event_is_set = event.wait(timeout)

        if event_is_set:
            msg = "%s is set" % (ename)
            logging.debug(msg)
            return
        else:
            emsg = "%s not set after %s sec" % (
                    ename, str(timeout))
            raise Exception(emsg)


# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(
        level=logging.DEBUG,
        # TODO: use the same log format for minicps?
        format='%(asctime)s (%(threadName)s) %(levelname)s: %(message)s')
logger = logging.getLogger('swat')

# DB
STATE_DB_PATH = 'examples/swat/state.db'
PLC1_DB_PATH = 'examples/swat/plc1.db'
PLC2_DB_PATH = 'examples/swat/plc2.db'
PLC3_DB_PATH = 'examples/swat/plc3.db'
PLC4_DB_PATH = 'examples/swat/plc4.db'
PLC5_DB_PATH = 'examples/swat/plc5.db'
PLC5_DB_PATH = 'examples/swat/plc5.db'
PLC6_DB_PATH = 'examples/swat/plc6.db'

SCHEMA = """
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

# state_db specific filters, functions and aggregators
DATATYPES = [
        'INT',
        'DINT',
        'BOOL',
        'REAL',
]

def create_db(db_path, schema):
    """TODO: Docstring for init.
    :db_path: full or relative path to the file.db
    :schema: str containing the schema

    """
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)
        logger.info('Created schema')


def remove_db(db_path):
    """TODO: Docstring for init.
    :returns: TODO

    """
    logger.info('Removing %s' % db_path)
    try:
        os.remove(db_path)
    except Exception, err:
        logger.warning(err)
    

def init_db(db_path, datatypes):
    """
    Init a DB from RSLogix 5000 exported csv file

    :db_path: full or relative path to the file.db
    :datatypes: list of DATATYPES

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


def show_db_tags(conn, table='', pid='0', how_many=0):
    """
    Show all entries from the dict table
    
    SQL commands must be separated
    """

    cursor = conn.cursor()
    cmd = "SELECT * FROM %s" % table

    if pid > '0' and pid < '8':
        cmd += ' WHERE pid = %s' % pid

    cursor.execute(cmd)

    if how_many == 0:
        records = cursor.fetchall()
    elif how_many == 1:
        records = cursor.fetchone()
    else:
        records = cursor.fetchmany(how_many)

    for record in records:
        logger.debug(record)

# CONSTANTS
L0_RING1 = {
    'plc': '192.168.0.10',
    'plcr': '192.168.0.11',
    'rio': '192.168.0.12',
    'rio_ap': '192.168.0.14',
    'sens_wifi_client': '192.168.0.15',
}

L0_RING2 = {
    'plc': '192.168.0.20',
    'plcr': '192.168.0.21',
    'rio': '192.168.0.22',
    'rio_ap': '192.168.0.24',
    'sens_wifi_client': '192.168.0.25',
}

L0_RING3 = {
    'plc': '192.168.0.30',
    'plcr': '192.168.0.31',
    'rio': '192.168.0.32',
    'rio_ap': '192.168.0.34',
    'sens_wifi_client': '192.168.0.35',
}

L0_RING4 = {
    'plc': '192.168.0.40',
    'plcr': '192.168.0.41',
    'rio': '192.168.0.42',
    'rio_ap': '192.168.0.44',
    'sens_wifi_client': '192.168.0.45',
}

L0_RING5 = {
    'plc': '192.168.0.50',
    'plcr': '192.168.0.51',
    'rio': '192.168.0.52',
    'rio_ap': '192.168.0.54',
    'sens_wifi_client': '192.168.0.55',
    'etap_vsd1': '192.168.0.56',
    'vsd1': '192.168.0.57',
    'etap_vsd2': '192.168.0.58',
    'vsd2': '192.168.0.59',
}

L0_RING6 = {
    'plc': '192.168.0.60',
    'plcr': '192.168.0.61',
    'rio': '192.168.0.62',
    'rio_ap': '192.168.0.64',
    'sens_wifi_client': '192.168.0.65',
}

L0_RING7 = {
    'plc': '192.168.0.70',
    'rio': '192.168.0.72',
    'rio_ap': '192.168.0.74',
    'sens_wifi_client': '192.168.0.75',
}

L1_PLCS_IP = {
    'plc1':  '192.168.1.10',
    'plc2':  '192.168.1.20',
    'plc3':  '192.168.1.30',
    'plc4':  '192.168.1.40',
    'plc5':  '192.168.1.50',
    'plc6':  '192.168.1.60',
    'plc1r': '192.168.1.11',
    'plc2r': '192.168.1.21',
    'plc3r': '192.168.1.31',
    'plc4r': '192.168.1.41',
    'plc5r': '192.168.1.51',
    'plc6r': '192.168.1.61',
    # used as central hub
    'plc7':  '192.168.1.70',
    'attacker': '192.168.1.77',
}


L1_WIFI_CLIENTS_IP = {
    'c1': '192.168.1.12',
    'c2': '192.168.1.22',
    'c3': '192.168.1.32',
    'c4': '192.168.1.42',
    'c5': '192.168.1.52',
    'c6': '192.168.1.62',
    'c7': '192.168.1.72',
}

L2_HMI = {
    'hmi': '192.168.1.100',
    'wifi_client': '192.168.1.101',
}

CONDUITS = {
    'firewall': '192.168.1.102',
    'pcn_ap':   '192.168.1.103',  # plant control network
    'dmz_ap':   '192.168.1.104',
}

L3_PLANT_NETWORK = {
    'histn':   '192.168.1.200',
    'workstn': '192.168.1.201',
}

L0_NETMASK = ''
L1_NETMASK = '/24'
L2_NETMASK = ''
L3_NETMASK = '/24'

PLCS_MAC = {
    'plc1':  '00:1D:9C:C7:B0:70',
    'plc2':  '00:1D:9C:C8:BC:46',
    'plc3':  '00:1D:9C:C8:BD:F2',
    'plc4':  '00:1D:9C:C7:FA:2C',
    'plc5':  '00:1D:9C:C8:BC:2F',
    'plc6':  '00:1D:9C:C7:FA:2D',
    'plc1r': '00:1D:9C:C8:BD:E7',
    'plc2r': '00:1D:9C:C8:BD:0D',
    'plc3r': '00:1D:9C:C7:F8:3B',
    'plc4r': '00:1D:9C:C8:BC:31',
    'plc5r': '00:1D:9C:C8:F4:B9',
    'plc6r': '00:1D:9C:C8:F5:DB',
    'plc7':  'TODO',
}


OTHER_MACS = {
    'histn':   'B8:2A:72:D7:B0:EC',
    'workstn': '98:90:96:98:CC:49',
    'hmi':     '00:1D:9C:C6:72:E8',
    'attacker': 'AA:AA:AA:AA:AA:AA',  # easy to recognize in the capture
}

IPS_TO_MACS = {
        # plcs
        '192.168.1.10':  '00:1D:9C:C7:B0:70',
        '192.168.1.20':  '00:1D:9C:C8:BC:46',
        '192.168.1.30':  '00:1D:9C:C8:BD:F2',
        '192.168.1.40':  '00:1D:9C:C7:FA:2C',
        '192.168.1.50':  '00:1D:9C:C8:BC:2F',
        '192.168.1.60':  '00:1D:9C:C7:FA:2D',
        '192.168.1.11':  '00:1D:9C:C8:BD:E7',
        '192.168.1.21':  '00:1D:9C:C8:BD:0D',
        '192.168.1.31':  '00:1D:9C:C7:F8:3B',
        '192.168.1.41':  '00:1D:9C:C8:BC:31',
        '192.168.1.51':  '00:1D:9C:C8:F4:B9',
        '192.168.1.61':  '00:1D:9C:C8:F5:DB',
        # hist and workstn
        '192.168.1.200': 'B8:2A:72:D7:B0:EC',
        '192.168.1.201': '98:90:96:98:CC:49',
        # hmi
        '192.168.1.100': '00:1D:9C:C6:72:E8',
}

PLCS = len(PLCS_MAC)
L1_NODES = 0 # TODO
L2_NODES = 0 # TODO
L3_NODES = PLCS/2 + 2  # 13/2 gives 6

# TODO: use real tag name and data types
# basic atomic types are: INT (16-bit), SINT (8-bit) DINT (32-bit) integer
# and REAL (32-bit float)
TAGS = {
    'pump3': 'pump3=INT[10]',
    'flow3': 'flow3=INT[10]',
}

CIP_VENDOR_IDS = {
    'plc1':  'TODO',
    'plc2':  'TODO',
    'plc3':  'TODO',
    'plc4':  'TODO',
    'plc5':  'TODO',
    'plc6':  'TODO',
    'plc1r': 'TODO',
    'plc2r': 'TODO',
    'plc3r': 'TODO',
    'plc4r': 'TODO',
    'plc5r': 'TODO',
    'plc6r': 'TODO',
    # used as central hub
    'plc7':  'TODO',
    'attacker': 'TODO',
}

CIP_SERIAL_NUMBERS = {
    'plc1':  'TODO',
    'plc2':  'TODO',
    'plc3':  'TODO',
    'plc4':  'TODO',
    'plc5':  'TODO',
    'plc6':  'TODO',
    'plc1r': 'TODO',
    'plc2r': 'TODO',
    'plc3r': 'TODO',
    'plc4r': 'TODO',
    'plc5r': 'TODO',
    'plc6r': 'TODO',
    # used as central hub
    'plc7':  'TODO',
    'attacker': 'TODO',
}
