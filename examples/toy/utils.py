"""
toy utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores
values as strings.

sqlite uses float keyword and cpppo use REAL keyword.

if ACTUATORX is 1 then is ON otherwise is OFF.
"""

from minicps.utils import build_debug_logger

toy_logger = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')


# others
PLC1_DATA = {
    'SENSOR1': '0',
    'SENSOR2': '0.0',
    'SENSOR3': '0',  # interlock with PLC2
    'ACTUATOR1': '1',  # 0 means OFF and 1 means ON
    'ACTUATOR2': '0',
}
PLC2_DATA = {
    'SENSOR3': '0'  # interlock with PLC1
}


PLC2_TAGS = (
    # ('AI_FIT_201_FLOW', 'INT'),
    ('DO_MV_201_CLOSE', 'INT'),
    ('DO_MV_201_OPEN', 'INT'),
    ('HMI_FIT201-Pv', 'REAL'),
    ('HMI_MV201-Status', 'INT'),
)

PLC3_TAGS = (
    ('AI_LIT_301_LEVEL', 'INT'),
    ('HMI_LIT301-Pv', 'REAL'),
)


# protocol
PLC1_MAC = '00:00:00:00:00:01'
PLC1_ADDR = '10.0.0.1'
PLC1_TAGS = (
    ('AI_FIT_101_FLOW', 1, 'INT'),
    ('DO_MV_101_CLOSE', 1, 'INT'),
    ('DO_MV_101_OPEN', 1, 'INT'),
    ('AI_LIT_101_LEVEL', 1, 'INT'),
    ('DO_P_101_START', 1, 'INT'),
    ('HMI_FIT201-Pv', 1, 'REAL'),
    ('HMI_MV201-Status', 1, 'INT'),
    ('HMI_MV101-Status', 1, 'INT'),
    ('HMI_P101-Status', 1, 'INT'),
    ('HMI_LIT301-Pv', 1, 'REAL'),
    ('HMI_LIT101-Pv', 1, 'REAL'),
)
PLC1_SERVER = {
    'address': PLC1_ADDR,
    'tags': PLC1_TAGS
}
PLC1_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC1_SERVER
}

PLC2_MAC = '00:00:00:00:00:02'
PLC2_ADDR = '10.0.0.2'
PLC2_TAGS = (
    ('SENSOR3', 2, 'INT'),)  # interlock with PLC1
PLC2_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC2_TAGS
}
PLC2_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC2_SERVER
}

# state
PATH = 'toy_db.sqlite'
NAME = 'toy_table'

STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE toy_table (
    name              TEXT NOT NULL,
    datatype          TEXT NOT NULL,
    value             TEXT,
    pid               INTEGER NOT NULL,
    PRIMARY KEY (name, pid)
);
"""
SCHEMA_INIT = """
    INSERT INTO toy_table VALUES ('SENSOR1',   'int', '0', 1);
    INSERT INTO toy_table VALUES ('SENSOR2',   'float', '0.0', 1);
    INSERT INTO toy_table VALUES ('SENSOR3',   'int', '1', 1);
    INSERT INTO toy_table VALUES ('ACTUATOR1', 'int', '1', 1);
    INSERT INTO toy_table VALUES ('ACTUATOR2', 'int', '0', 1);
    INSERT INTO toy_table VALUES ('SENSOR3',   'int', '2', 2);
"""
