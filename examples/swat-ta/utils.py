"""
swat-ta utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores
values as strings.

Actuator state is encoded with the following integer values:
    - -1 = error
    -  0 = off
    -  1 = on

sqlite uses float keyword and cpppo use REAL keyword.
"""

# physical process {{{1

GRAVITATION = 9.81             # m.s^-2
TANK_DIAMETER = 1.38           # m
TANK_SECTION = 1.5             # m^2
PUMP_FLOWRATE_IN = 2.55        # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 2.45       # m^3/h spec say btw 2.2 and 2.4

# periods in msec
# R/W = Read or Write
T_PLC_R = 100E-3
T_PLC_W = 100E-3

T_PP_R = 200E-3
T_PP_W = 200E-3
T_HMI_R = 100E-3

# Control logic thresholds
LIT_101_MM = {  # raw water tank mm
    'LL': 250.0,
    'L': 500.0,
    'H': 800.0,
    'HH': 1200.0,
}
LIT_101_M = {  # raw water tank m
    'LL': 0.250,
    'L': 0.500,
    'H': 0.800,
    'HH': 1.200,
}

LIT_301_MM = {  # ultrafiltration tank mm
    'LL': 250.0,
    'L': 800.0,
    'H': 1000.0,
    'HH': 1200.0,
}
LIT_301_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.800,
    'H': 1.000,
    'HH': 1.200,
}

TANK_HEIGHT = 1.600  # m

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.20  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

RWT_INIT_LEVEL = 0.500  # l

# m^3 / h
FIT_201_THRESH = 0.500  # m^3/h

# }}}

# topo {{{1
IP = {
    'plc1': '192.168.1.10',
    'plc2': '192.168.1.20',
    'plc3': '192.168.1.30',
    'plc4': '192.168.1.40',
    'plc5': '192.168.1.50',
    'plc6': '192.168.1.60',
    'attacker': '192.168.1.77',
}

NETMASK = '/24'

MAC = {
    'plc1': '00:1D:9C:C7:B0:70',
    'plc2': '00:1D:9C:C8:BC:46',
    'plc3': '00:1D:9C:C8:BD:F2',
    'plc4': '00:1D:9C:C7:FA:2C',
    'plc5': '00:1D:9C:C8:BC:2F',
    'plc6': '00:1D:9C:C7:FA:2D',
    'attacker': 'AA:AA:AA:AA:AA:AA',
}
# }}}

# protocols {{{1

# NOTE: empy dicts used for memory and disk abstraction
PLC1_DATA = {}
PLC2_DATA = {}
PLC3_DATA = {}


PLC1_ADDR = IP['plc1']
PLC1_TAGS = (
    ('FIT101', 1, 'REAL'),
    ('MV101', 1, 'INT'),
    ('LIT101', 1, 'REAL'),
    ('P101', 1, 'INT'),
    # interlocks does NOT go to the statedb
    ('FIT201', 1, 'REAL'),
    ('MV201', 1, 'INT'),
    ('LIT301', 1, 'REAL'),
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

PLC2_ADDR = IP['plc2']
PLC2_TAGS = (
    ('FIT201', 2, 'REAL'),
    ('MV201', 2, 'INT'),
    # no interlocks
)
PLC2_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC2_TAGS
}
PLC2_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC2_SERVER
}

PLC3_ADDR = IP['plc3']
PLC3_TAGS = (
    ('LIT301', 3, 'REAL'),
    # no interlocks
)
PLC3_SERVER = {
    'address': PLC3_ADDR,
    'tags': PLC3_TAGS
}
PLC3_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC3_SERVER
}

# }}}

# state {{{1

# NOTE: pid field is used just to keep same tuple to address enip and state
#       however is does not make sense to have a FIT101 2 record on the db
#       because there is just one FIT101 sensor in the real system

PATH = 'swat_ta_db.sqlite'
NAME = 'swat_ta'

STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE swat_ta (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

# TODO: Add alarms and HMI
SCHEMA_INIT = """
    INSERT INTO swat_ta VALUES ('FIT101',   1, '2.55');
    INSERT INTO swat_ta VALUES ('MV101',    1, '0');
    INSERT INTO swat_ta VALUES ('LIT101',   1, '0.500');
    INSERT INTO swat_ta VALUES ('P101',     1, '1');
    INSERT INTO swat_ta VALUES ('FIT201',   2, '2.45');
    INSERT INTO swat_ta VALUES ('MV201',    2, '0');
    INSERT INTO swat_ta VALUES ('LIT301',   3, '0.500');
"""

# }}}

# tags {{{1

# NOTE: naming is NAMEPID_PLCID

FIT101_1 = ('FIT101', 1)
MV101_1 = ('MV101', 1)
LIT101_1 = ('LIT101', 1)
P101_1 = ('P101', 1)

FIT201_1 = ('FIT201', 1)
FIT201_2 = ('FIT201', 2)
MV201_1 = ('MV201', 1)
MV201_2 = ('MV201', 2)

LIT301_1 = ('LIT301', 1)
LIT301_3 = ('LIT301', 3)


# }}}
