"""
swat-s1 utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores
values as strings.

Actuator tags are redundant, we will use only the XXX_XXX_OPEN tag ignoring
the XXX_XXX_CLOSE with the following convention:
    - 0 = error
    - 1 = off
    - 2 = on

sqlite uses float keyword and cpppo use REAL keyword.
"""

from minicps.utils import build_debug_logger

swat = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ldir="logs/",
    suffix="",
)

# physical process {{{1
# SPHINX_SWAT_TUTORIAL PROCESS UTILS(
GRAVITATION = 9.81  # m.s^-2
TANK_DIAMETER = 1.38  # m
TANK_SECTION = 1.5  # m^2
PUMP_FLOWRATE_IN = 0.5  # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 3  # m^3/h spec say btw 2.2 and 2.4

# periods in msec
# R/W = Read or Write
T_PLC_R = 100e-3
T_PLC_W = 100e-3

T_PP_R = 200e-3
T_PP_W = 200e-3
T_HMI_R = 100e-3

# ImageTk
DISPLAYED_SAMPLES = 14

# Control logic thresholds
LIT_101_MM = {  # raw water tank mm
    "LL": 250.0,
    "L": 500.0,
    "H": 800.0,
    "HH": 1200.0,
}
LIT_101_M = {  # raw water tank m
    "LL": 0.250,
    "L": 0.500,
    "H": 0.800,
    "HH": 1.200,
}

LIT_301_MM = {  # ultrafiltration tank mm
    "LL": 250.0,
    "L": 800.0,
    "H": 1000.0,
    "HH": 1200.0,
}
LIT_301_M = {  # ultrafiltration tank m
    "LL": 0.250,
    "L": 0.800,
    "H": 1.000,
    "HH": 1.200,
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
FIT_201_THRESH = 1.00
# SPHINX_SWAT_TUTORIAL PROCESS UTILS)

# topo {{{1
IP = {
    "plc1": "192.168.1.10",
    "plc2": "192.168.1.20",
    "plc3": "192.168.1.30",
    "dev1": "192.168.1.40",
    "dev2": "192.168.1.50",
    "dev3": "192.168.1.60",
    "dev4": "192.168.1.70",
    "dev5": "192.168.1.80",
    "dev6": "192.168.1.90",
    "dev7": "192.168.1.100",
    "attacker": "192.168.1.77",
}

NETMASK = "/24"

MAC = {
    "plc1": "00:1D:9C:C7:B0:70",
    "plc2": "00:1D:9C:C8:BC:46",
    "plc3": "00:1D:9C:C8:BD:F2",
    "dev1": "00:1D:9C:C7:B0:11",
    "dev2": "00:1D:9C:C8:BC:12",
    "dev3": "00:1D:9C:C8:BD:13",
    "dev4": "00:1D:9C:C7:B0:14",
    "dev5": "00:1D:9C:C8:BC:15",
    "dev6": "00:1D:9C:C8:BD:16",
    "dev7": "00:1D:9C:C8:BD:17",
    "attacker": "AA:AA:AA:AA:AA:AA",
}


# others
# TODO
PLC1_DATA = {
    "TODO": "TODO",
}
# TODO
PLC2_DATA = {
    "TODO": "TODO",
}
# TODO
PLC3_DATA = {
    "TODO": "TODO",
}
# TODO
DEV1_DATA = {
    "TODO": "TODO",
}
# TODO
DEV2_DATA = {
    "TODO": "TODO",
}
# TODO
DEV3_DATA = {
    "TODO": "TODO",
}
# TODO
DEV4_DATA = {
    "TODO": "TODO",
}
# TODO
DEV5_DATA = {
    "TODO": "TODO",
}
# TODO
DEV6_DATA = {
    "TODO": "TODO",
}

# IO-CONTROLER / PLCs
# SPHINX_SWAT_TUTORIAL PLC1 UTILS(
PLC1_ADDR = IP["plc1"]
PLC1_TAGS = (
    # interlocks does NOT go to the statedb
    ("FIT101", 1, "REAL"),
    ("MV101", 1, "INT"),
    ("LIT101", 1, "REAL"),
    ("P101", 1, "INT"),
    ("FIT201", 1, "REAL"),
    ("MV201", 1, "INT"),
    ("LIT301", 1, "REAL"),
)
PLC1_SERVER = {"address": PLC1_ADDR, "tags": PLC1_TAGS}
PLC1_PROTOCOL = {"name": "enip", "mode": 1, "server": PLC1_SERVER}
# SPHINX_SWAT_TUTORIAL PLC1 UTILS)

PLC2_ADDR = IP["plc2"]
PLC2_TAGS = (
    # interlocks does NOT go to the statedb
    ("FIT201", 2, "REAL"),
    ("MV201", 2, "INT"),
)
PLC2_SERVER = {"address": PLC2_ADDR, "tags": PLC2_TAGS}
PLC2_PROTOCOL = {"name": "enip", "mode": 1, "server": PLC2_SERVER}

PLC3_ADDR = IP["plc3"]
PLC3_TAGS = (
    # interlocks does NOT go to the statedb
    ("LIT301", 3, "REAL"),
)
PLC3_SERVER = {"address": PLC3_ADDR, "tags": PLC3_TAGS}
PLC3_PROTOCOL = {"name": "enip", "mode": 1, "server": PLC3_SERVER}

# IO-DEVICES
DEV1_ADDR = IP["dev1"]
DEV1_TAGS = (("FIT101", 4, "REAL"),)
DEV1_SERVER = {"address": DEV1_ADDR, "tags": DEV1_TAGS}
DEV1_PROTOCOL = {"name": "enip", "mode": 1, "server": DEV1_SERVER}

DEV2_ADDR = IP["dev2"]
DEV2_TAGS = (("MV101", 5, "INT"),)
DEV2_SERVER = {"address": DEV2_ADDR, "tags": DEV2_TAGS}
DEV2_PROTOCOL = {"name": "enip", "mode": 1, "server": DEV2_SERVER}

DEV3_ADDR = IP["dev3"]
DEV3_TAGS = (("LIT101", 6, "REAL"),)
DEV3_SERVER = {"address": DEV3_ADDR, "tags": DEV3_TAGS}
DEV3_PROTOCOL = {"name": "enip", "mode": 1, "server": DEV3_SERVER}

DEV4_ADDR = IP["dev4"]
DEV4_TAGS = (("P101", 7, "INT"),)
DEV4_SERVER = {"address": DEV4_ADDR, "tags": DEV4_TAGS}
DEV4_PROTOCOL = {"name": "enip", "mode": 1, "server": DEV4_SERVER}

DEV5_ADDR = IP["dev5"]
DEV5_TAGS = (("FIT201", 8, "REAL"),)
DEV5_SERVER = {"address": DEV5_ADDR, "tags": DEV5_TAGS}
DEV5_PROTOCOL = {"name": "enip", "mode": 1, "server": DEV5_SERVER}

DEV6_ADDR = IP["dev6"]
DEV6_TAGS = (("LIT301", 9, "REAL"),)
DEV6_SERVER = {"address": DEV6_ADDR, "tags": DEV6_TAGS}
DEV6_PROTOCOL = {"name": "enip", "mode": 1, "server": DEV6_SERVER}


# state {{{1
# SPHINX_SWAT_TUTORIAL STATE(
PATH = "swat_s2_db.sqlite"
NAME = "swat_s2"

STATE = {"name": NAME, "path": PATH}
# SPHINX_SWAT_TUTORIAL STATE)

SCHEMA = """
CREATE TABLE swat_s2 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO swat_s2 VALUES ('FIT101',   4, '2.55');
    INSERT INTO swat_s2 VALUES ('MV101',    5, '0');
    INSERT INTO swat_s2 VALUES ('LIT101',   6, '0.500');
    INSERT INTO swat_s2 VALUES ('P101',     7, '1');

    INSERT INTO swat_s2 VALUES ('FIT201',   8, '2.45');

    INSERT INTO swat_s2 VALUES ('LIT301',   9, '0.500');
"""
