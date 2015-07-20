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

BOOL tags are implemented using INT int cpppo because SINT datatype
is broken and BOOL is not supported.
Pump and motorized valve NAME.Status tags use this convention:
        0:  Error
        1:  Closed
        2:  Open
Dashes (-) are used instead of dots as field separators inside tag names
because cpppo tag name cannot contain a dot .

"""

import sqlite3
import logging
import os
import os.path


# PLC TAGS

# UDT Bases
class FIT_UDT(object):
    """FIT_UDT"""

    def __init__(self):

        self.Pv = '0.0'
        self.Heu = '0.0'
        self.Leu = '0.0'
        self.SAHH = '0.0'
        self.SAH = '0.0'
        self.SAL - '0.0'
        self.SALL = '0.0'
        self.Totaliser = '0.0'
        self.AHH = '0'
        self.AH = '0'
        self.AL = '0'
        self.ALL = '0'
        self.Sim = '0'
        self.Sim_PV = '0.0'
        self.Wifi_Enb = '0'
        self.Rst_Totaliser = '0'
        self.Hty = '0'


class AIN_UDT(object):
    """AIN_UDT: LIT"""

    def __init__(self):

        self.Pv = '0.0'
        self.Heu = '0.0'
        self.Leu = '0.0'
        self.SAHH = '0.0'
        self.SAH = '0.0'
        self.SAL - '0.0'
        self.SALL = '0.0'
        self.AHH = '0'
        self.AH = '0'
        self.AL = '0'
        self.ALL = '0'
        self.Wifi_Enb = '0'
        self.Hty = '0'
        self.Sim = '0'
        self.Sim_PV = '0.0'


class MV_UDT(object):
    """MV_UDT"""

    def __init__(self):
        self.Cmd = [ '' for i in range(0,16) ]
        self.Status = [ '' for i in range(0,16) ]
        self.Reset = '0'
        self.Auto = '0'
        self.FTO = '0'
        self.FTC = '0'
        self.Avl= '0'


class PMP_UDT(object):
    """PMP_UDT"""

    def __init__(self):
        self.Cmd = [ '' for i in range(0,16) ]
        self.Status = [ '' for i in range(0,16) ]
        self.RunMin = '0.0'
        self.Total_RunMin = '0.0'
        self.RunHr = '0.0'
        self.Total_RunHr = '0.0'
        self.Remote = '0'
        self.Auto = '0'
        self.Fault = '0'
        self.Avi = '0'
        self.Permissive = [ '' for i in range(0,32) ]
        self.Shutdown = [ '' for i in range(0,32) ]
        self.SD = [ '' for i in range(0,32) ]
        self.Reset = '0'
        self.Reset_RunHr = '0'
        self.FTR = '0'
        self.FTS = '0'


# UDT Aliases

    """Docstring for HMI_FIT101. """
    def __init__(self):
        """TODO: to be defined1. """


# CPPPO

PLC1_CPPPO_CACHE = "examples/swat/plc1_cpppo.cache"

# basic atomic types are: INT (16-bit), SINT (8-bit) DINT (32-bit) integer
# and REAL (32-bit float)
P1_PLC1_TAGS = [
    # ('AI_FIT_101_FLOW', 'INT'),
    ('DO_MV_101_CLOSE', 'INT'),
    ('DO_MV_101_OPEN', 'INT'),
    ('AI_LIT_101_LEVEL', 'INT'),
    ('DO_P_101_START', 'INT'),
    ('HMI_FIT201-Pv', 'REAL'),
    ('HMI_MV201-Status', 'INT'),
    ('HMI_LIT301-Pv', 'REAL'),
]

P1_PLC2_TAGS = [
    # ('AI_FIT_201_FLOW', 'INT'),
    ('DO_MV_201_CLOSE', 'INT'),
    ('DO_MV_201_OPEN', 'INT'),
    ('HMI_FIT201-Pv', 'REAL'),
    ('HMI_MV201-Status', 'INT'),
]

P1_PLC3_TAGS = [
    ('AI_LIT_301_LEVEL', 'INT'),
    ('HMI_LIT301-Pv', 'REAL'),
]



# PROCESS

# periods in sec
T_PLC_R = 10E-3
T_PLC_W = 10E-3

T_PP_R = 2E-3
T_PP_W = 2E-3

# mm
LIT_101 = {  # raw water tank
    'LL': 250.0,
    'L': 500.0,
    'H': 800.0,
    'HH': 1200.0,
}

LIT_301 = {  # ultrafiltration tank
    'LL': 250.0,
    'L': 800.0,
    'H': 1000.0,
    'HH': 1200.0,
}

# m^3 / h
FIT_201 = 0.0



# THREADS
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



# LOGGING
logging.basicConfig(
        filename = os.path.join(
            os.path.dirname(__file__),
            os.path.pardir, os.path.pardir, 'logs', 'swat.log'),
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # format='%(asctime)s (%(threadName)s) %(levelname)s: %(message)s')
logger = logging.getLogger('swat')



# CPPPO

def db2cpppo(record):
    """
    Convert from sqlite3 db record to cpppo tag string
    No vector tag support.
    BOOL are converted into INT (SINT are tags don't work)


    :record: tuple from the state db
    :returns: string

    """
    SCOPE = record[0]
    NAME = record[1]
    DATATYPE = record[2]
    VALUE = record[3]
    PID = record[4]

    if DATATYPE not in DATATYPES:
        logger.info("%s is not in the state db" % DATATYPE)
        cppo_str = ''
    else:
        # cpppo uses SINT as BOOL
        if DATATYPE == 'BOOL':
            DATATYPE = 'INT'

        cppo_str = NAME+'='+DATATYPE
        logger.debug("db2cpppo: %s -> %s" % (record, cppo_str))

    return cppo_str


def init_cpppo_server(tags):
    """Init cpppo enip server

    :tags: list of tuples (NAME, DATATYPE)

    """

    cpppo_tags = tags[0][0]+'='+tags[0][1]
    for tag in tags[1:]:
        cpppo_tags += ' '+tag[0]+'='+tag[1]

    # DEBUG TAGS
    # cpppo_tags += ' P1=INT'
    # cpppo_tags += ' P2=SINT' # doesn't work
    # cpppo_tags += ' P3=DINT'
    # cpppo_tags += ' P4=REAL'

    # logger.debug('cpppo_tags: %s' % cpppo_tags)

    cmd = 'python -m cpppo.server.enip --print -v %s &' % cpppo_tags
    rc = os.system(cmd)
    assert rc == 0, "init_cpppo_server"

def write_cpppo(ip, tag_name, val):
    """Write cpppo

    :ip: TODO
    :tag_name: str equal to the state db NAME field
    :val: str

    """

    # TODO: write multiple values
    expr = tag_name+'='+val
    cmd = "python -m cpppo.server.enip.client --print -a %s %s" % (ip, expr)
    rc = os.system(cmd)
    assert rc == 0, "write_cpppo"

def read_cpppo(ip, tag_name, cpppo_cache):
    """Read from a cpppo enip server store value in a temp cache and remove
    it.

    :ip: cpppo server IP
    :tag_name: str equal to the state db NAME field
    :cpppo_cache: path to the cpppo enip client cache

    :returns: str value otherwise -1

    """

    # TODO: read multiple values
    # TODO: append with >>
    cmd = "python -m cpppo.server.enip.client --print -a %s %s > %s" % (
            ip,
            tag_name,
            cpppo_cache)
    rc = os.system(cmd)
    assert rc == 0, "read_cpppo"

    # TODO: support for vector tags
    with open(cpppo_cache, "r") as file_ptr:
        line = file_ptr.readline()

        words = line.split()
        print words
        status = words[3][1:-1]
        if status != 'OK':
            value = '-1'
        else:
            value = words[2][1:-2]

    return value



# DB
STATE_DB_PATH = os.path.join(os.path.dirname(__file__), 'state.db')

# currently no PLC dbs
# PLC1_DB_PATH = os.path.join(os.path.dirname(__file__), 'plc1.db')
# PLC2_DB_PATH = os.path.join(os.path.dirname(__file__), 'plc2.db')
# PLC3_DB_PATH = os.path.join(os.path.dirname(__file__), 'plc3.db')
# PLC4_DB_PATH = os.path.join(os.path.dirname(__file__), 'plc4.db')
# PLC5_DB_PATH = os.path.join(os.path.dirname(__file__), 'plc5.db')
# PLC5_DB_PATH = os.path.join(os.path.dirname(__file__), 'plc5.db')
# PLC6_DB_PATH = os.path.join(os.path.dirname(__file__), 'plc6.db')

TABLE = 'Tag'

SCHEMA = """
        create table %s (
            SCOPE             text not null,
            NAME              text not null,
            DATATYPE          text not null,
            VALUE             text,
            PID               integer not null,
            PRIMARY KEY (SCOPE, NAME, PID)
        );
        """ % TABLE
        # VALUE             text default '',

# state_db specific filters, functions and aggregators
# TODO: add UDT
DATATYPES = [
        'INT',
        'DINT',
        'BOOL',
        'REAL',

        'FIT_UDT',
        'AIN_UDT',  # eg: LIT
        'MV_UDT',
        'PMP_UDT',
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
    sqlite3 uses ? placeholder for parameters substitution

    TODO: UDT modeling convention

    :db_path: full or relative path to the file.db
    :datatypes: list of DATATYPES

    """

    # Subprocess1 UDT modeling
    # P1_UDT = [
    #     ('', 'HMI_P101.Status', 'INT', '', 1),
    #     ('', 'HMI_P101.Cmd', 'INT', '', 1),
    #     ('', 'HMI_FIT101.Pv', 'REAL', '', 1),
    # ]                                     1

    # P2_UDT = [
    #     ('', 'HMI_FIT201.Pv', 'REAL', '', 2),
    #     ('', 'HMI_FIT201.Status', 'REAL', '', 2),
    # ]

    with sqlite3.connect(db_path) as conn:
        try:
            logger.info('Init tables')

            for i in range(1, 7):
                plc_filename = os.path.join(os.path.dirname(__file__), "real-tags", "P%d-Tags.CSV" % i)
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
                            par_sub = (scope, name, datatype, i)
                            cmd = """
                            INSERT INTO Tag (SCOPE, NAME, DATATYPE, PID)
                            VALUES (?, ?, ?, ?)
                            """
                            cursor.execute(cmd, par_sub)

                    conn.commit()
        except sqlite3.Error, e:
            logger.warning('Error %s:' % e.args[0])


# FIXME: set default PID and generalize the query
def read_statedb(PID, NAME=None, SCOPE='TODO'):
    """Read multiple tags
    sqlite3 uses ? placeholder for parameters substitution

    :NAME: str
    :PID: int
    :SCOPE: not implemented yet
    :returns: list of tuples

    """
    with sqlite3.connect(STATE_DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            par_temp = [PID]
            cmd = """
            SELECT * FROM Tag
            WHERE PID = ?
            """

            if NAME is not None:
                cmd += 'AND NAME = ?'
                par_temp.append(NAME)

            par_sub = tuple(par_temp)
            cursor.execute(cmd, par_sub)

            records = cursor.fetchall()
            return records
        except sqlite3.Error, e:
            logger.warning('Error %s:' % e.args[0])


# FIXME: set default PID and generalize the query
def read_statedb(PID, NAME=None, SCOPE='TODO'):
    """Read multiple tags
    sqlite3 uses ? placeholder for parameters substitution

    :NAME: str
    :PID: int
    :SCOPE: not implemented yet
    :returns: list of tuples

    """
    with sqlite3.connect(STATE_DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            par_temp = [PID]
            cmd = """
            SELECT * FROM Tag
            WHERE PID = ?
            """

            if NAME is not None:
                cmd += 'AND NAME = ?'
                par_temp.append(NAME)

            par_sub = tuple(par_temp)
            cursor.execute(cmd, par_sub)

            records = cursor.fetchall()
            return records
        except sqlite3.Error, e:
            logger.warning('Error %s:' % e.args[0])


def read_single_statedb(PID, NAME, SCOPE='TODO'):
    """Update Tag table
    sqlite3 uses ? placeholder for parameters substitution

    :NAME: str
    :PID: str
    :SCOPE: not implemented yet
    :returns: list of tuples

    """

    with sqlite3.connect(STATE_DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cmd = """
            SELECT * FROM Tag
            WHERE PID = ? AND NAME = ?
            """
            par_sub = (PID, NAME)
            cursor.execute(cmd, par_sub)

            record = cursor.fetchone()
            return record

        except sqlite3.Error, e:
            logger.warning('Error %s:' % e.args[0])

def update_statedb(VALUE, PID, NAME, SCOPE='TODO'):
    """Update Tag table

    :VALUE: str
    :NAME: str
    :PID: str
    :SCOPE: not implemented yet

    """

    with sqlite3.connect(STATE_DB_PATH) as conn:
        try:
            cursor = conn.cursor()
            cmd = """
            UPDATE Tag
            SET VALUE = ?
            WHERE PID = ? AND NAME = ?
            """
            par_sub = (VALUE, PID, NAME)
            cursor.execute(cmd, par_sub)
            conn.commit()
        except sqlite3.Error, e:
            logger.warning('Error %s:' % e.args[0])

def select_value(record):
    return float(record[3])

# NETWORK
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

PROCESS_NUMBER = 1
GRAVITATION = 9.81

VALVE_DIAMETER = 0.2
TANK_DIAMETER = 1.38

TIMER = 0.2
TIMEOUT = 120
