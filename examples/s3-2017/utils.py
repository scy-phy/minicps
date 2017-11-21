"""
s317 wadi utils.py

sqlite3 db will store tags using type, offset, and pid primary key.

Values are stored as strings:
    - bits are encoded with 0/1 to represent False/True
    - registers are encoded storing the integer value as a string
    - Eg: if coil is '0' then is considered False
    - Eg: if register is '34' then is considered 34

pymodbus servers will store data TODO

Eg: TODO
"""

from minicps.utils import build_debug_logger

# log {{{1
wadi = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix=''
)
# }}}

# tags {{{1
CO_0_2a = ('CO', 0, '2a')
CO_1_2a = ('CO', 1, '2a')
CO_2_2a = ('CO', 2, '2a')
CO_3_2a = ('CO', 3, '2a')
HR_0_2a = ('HR', 0, '2a')
HR_1_2a = ('HR', 1, '2a')
HR_2_2a = ('HR', 2, '2a')

# IR_0_2a = ('IR', 0, '2a')
# IR_1_2a = ('IR', 1, '2a')
# DI_0_2a = ('DI', 0, '2a')
# DI_1_2a = ('DI', 1, '2a')

CO_0_2b = ('CO', 0, '2b')
CO_1_2b = ('CO', 1, '2b')
CO_2_2b = ('CO', 2, '2b')
CO_3_2b = ('CO', 3, '2b')
HR_0_2b = ('HR', 0, '2b')
HR_1_2b = ('HR', 1, '2b')
HR_2_2b = ('HR', 2, '2b')

# }}}

# s317 {{{1

# wadi {{{2
# wadi1 = 'a'  # 0b 01 10 00 01
# wadi1 = 'abcdefghilmnopqrstuvz'
with open('/root/flags/wadi1', mode="r") as f:
    wadi1 = f.read().strip()
wadi1_bin = ''.join(format(ord(i),'b').zfill(8) for i in wadi1)
# NOTE: sniff aprox 180 bits

with open('/root/flags/wadi2', mode="r") as f:
    wadi2 = f.read().strip()
wadi2_list = []
for c in wadi2:
    wadi2_list.append(ord(c))
# NOTE: 12 rounds with 4 hoppings
# }}}

# }}}

# constants {{{1

# swat {{{2
GRAVITATION = 9.81             # m.s^-2
TANK_DIAMETER = 1.38           # m
TANK_SECTION = 1.5             # m^2

PUMP_FLOWRATE_IN = 2.55        # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 2.55       # m^3/h spec say btw 2.2 and 2.4

# Control logic thresholds
LIT_101_MM = {  # raw water tank mm
    'LL': 250.0,
    'L': 500.0,
    'H': 800.0,
    'HH': 1200.0,
    'MAX': 1600.0,
}
LIT_101_M = {  # raw water tank m
    'LL': 0.250,
    'L': 0.500,
    'H': 0.800,
    'HH': 1.200,
    'MAX': 1.600,
}

LIT_301_MM = {  # ultrafiltration tank mm
    'LL': 250.0,
    'L': 800.0,
    'H': 1000.0,
    'HH': 1200.0,
    'MAX': 1600.0,
}
LIT_301_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.800,
    'H': 1.000,
    'HH': 1.200,
    'MAX': 1.600,
}

TANK_HEIGHT = 1.600  # m

# PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_SEC = 2  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0

# PP_RESCALING_HOURS = 100
PP_RESCALING_HOURS = 20
# PP_PERIOD_SEC = 0.20  # physical process update rate in seconds
PP_PERIOD_SEC = 1
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS

RWT_INIT_LEVEL = 0.500  # l
UFT_INIT_LEVEL = 0.500  # l

# m^3 / h
FIT_201_THRESH = 1.00
# }}}

# wadi {{{2
PROC2A_PERIOD_SEC = 2.0
PROC2B_PERIOD_SEC = 2.0
RTU_PERIOD_SEC =   2.0
SCADA_PERIOD_SEC = 2.0
# }}}

# }}}

# addresses {{{1

# swat {{{2
IP_SWAT = {
    'plc1': '192.168.1.10',
    'plc2': '192.168.1.20',
    'plc3': '192.168.1.30',
    'plc4': '192.168.1.40',
    'plc5': '192.168.1.50',
    'plc6': '192.168.1.60',
    'shmi': '192.168.1.100',
    'attacker': '192.168.1.77',
    # NOTE: attacker openvpn server remote ip will be 2.2.2.1
    'client': '10.0.0.10',  # remote IP used for openvpn client
}

MAC_SWAT = {
    'plc1': '00:1D:9C:C7:B0:70',
    'plc2': '00:1D:9C:C8:BC:46',
    'plc3': '00:1D:9C:C8:BD:F2',
    'plc4': '00:1D:9C:C7:FA:2C',
    'plc5': '00:1D:9C:C8:BC:2F',
    'plc6': '00:1D:9C:C7:FA:2D',
    'shmi' : '00:1D:9C:C6:72:E8',
    'attacker': 'AA:AA:AA:AA:AA:AA',
    'client': 'AA:AA:AA:AA:AA:AB',
}

NETMASK_SWAT = '/24'
# }}}

# wadi {{{2
IP = {
    'rtu2a': '192.168.10.30',
    'rtu2b': '192.168.10.40',
    'scada': '192.168.10.201',
    'hmi': '192.168.10.100',
    'hist': '192.168.10.200',
    'ids': '192.168.10.204',
    'g2a': '192.168.10.71',
    'g2b': '192.168.10.72',
    'attacker2': '192.168.10.77',
    # NOTE: attacker2 openvpn server remote ip will be 2.2.2.2
    'client2': '10.0.0.20',
    # NOTE: not used
    'plc1': '192.168.10.10',
    'plc2': '192.168.10.20',
    'plc3': '192.168.10.50',
    'gprs1': '192.168.10.11',
    'gprs2': '192.168.10.21',
    'gprs3': '192.168.10.31',
}


MAC = {
    'rtu2a': '00:1D:9C:C8:BC:46',
    'rtu2b': '00:05:21:02:0E:BF',
    'scada': '64:00:6A:70:86:D0',
    'hmi':   '15:9E:EC:6B:28:41',
    'hist':  '8F:02:CB:42:0B:A2',
    'ids':   '66:00:6A:70:86:D0',
    'g2a':   'D1:64:19:A4:26:D9',
    'g2b':   'E3:F6:E5:F8:E6:1B',
    'attacker2': 'AA:AA:AA:AA:AA:A2',
    'client2': 'AA:AA:AA:AA:AA:B2',
}

NETMASK = '/24'
# }}}

# }}}

# protocol {{{1

# swat {{{2
with open('/root/flags/flag2', mode="r") as f:
    flag2 = f.read().strip()
PLC2_ADDR = IP_SWAT['plc2']
PLC2_TAGS = (
    (flag2, 'INT'),
    ('README', 2, 'STRING'),
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


with open('/root/flags/flag3', mode="r") as f:
    flag3 = f.read().strip()
PLC3_ADDR = IP_SWAT['plc3']
PLC3_TAGS = (
    (flag3, 'INT'),
    ('README', 3, 'STRING'),
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

# wadi {{{2

SCADA_ADDR = IP['scada']
SCADA_TAGS = (10, 10, 10, 10)

SCADA_SERVER = {
    'address': SCADA_ADDR,
    'tags': SCADA_TAGS
}
SCADA_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': SCADA_SERVER
}

RTU2A_ADDR = IP['rtu2a']
RTU2A_TAGS = (10, 10, 10, 10)

RTU2A_SERVER = {
    'address': RTU2A_ADDR,
    'tags': RTU2A_TAGS
}
RTU2A_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': RTU2A_SERVER
}

RTU2B_ADDR = IP['rtu2b']
RTU2B_TAGS = (10, 10, 10, 10)
RTU2B_SERVER = {
    'address': RTU2B_ADDR,
    'tags': RTU2B_TAGS
}
RTU2B_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': RTU2B_SERVER
}
# }}}

# }}}

# state {{{1

# swat {{{2
NAME_SWAT = 'enip'
PATH_SWAT = 'enip.sqlite'

STATE_SWAT = {
    'name': NAME_SWAT,
    'path': PATH_SWAT
}

SCHEMA_SWAT = """
CREATE TABLE enip (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT_SWAT = """
    INSERT INTO enip VALUES ('FIT101',   1, '2.55');
    INSERT INTO enip VALUES ('MV101',    1, '0');
    INSERT INTO enip VALUES ('LIT101',   1, '0.500');
    INSERT INTO enip VALUES ('P101',     1, '1');
    INSERT INTO enip VALUES ('FIT201',   2, '2.55');
    INSERT INTO enip VALUES ('MV301',    3, '0');
    INSERT INTO enip VALUES ('LIT301',   3, '0.500');
    INSERT INTO enip VALUES ('P301',     3, '1');
"""

# }}}

# wadi {{{2
NAME = 'wadi'
PATH = '%s.sqlite' % NAME

STATE = {
    'name': NAME,
    'path': PATH
}

SCHEMA = """
CREATE TABLE wadi (
    type              TEXT NOT NULL,
    offset            INT  NOT NULL,
    pid               TEXT  NOT NULL,
    value             TEXT,
    PRIMARY KEY (type, offset, pid)
);
"""

# NOTE: 4 coils and 3 holding registers for each RTU
SCHEMA_INIT = """
    INSERT INTO wadi VALUES ('CO', 0, '2a', '0');
    INSERT INTO wadi VALUES ('CO', 1, '2a', '0');
    INSERT INTO wadi VALUES ('CO', 2, '2a', '0');
    INSERT INTO wadi VALUES ('CO', 3, '2a', '0');
    INSERT INTO wadi VALUES ('HR', 0, '2a', '0');
    INSERT INTO wadi VALUES ('HR', 1, '2a', '0');
    INSERT INTO wadi VALUES ('HR', 2, '2a', '0');
    INSERT INTO wadi VALUES ('CO', 0, '2b', '1');
    INSERT INTO wadi VALUES ('CO', 1, '2b', '1');
    INSERT INTO wadi VALUES ('CO', 2, '2b', '1');
    INSERT INTO wadi VALUES ('CO', 3, '2b', '1');
    INSERT INTO wadi VALUES ('HR', 0, '2b', '1');
    INSERT INTO wadi VALUES ('HR', 1, '2b', '1');
    INSERT INTO wadi VALUES ('HR', 2, '2b', '1');

"""
# }}}

# }}}
