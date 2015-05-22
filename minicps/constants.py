"""
minicps constants.

TEST_LOG_LEVEL affetcs all the tests. 
output, info and debug are in increasing order of verbosity.

L0 rings are isolated dicts.
L1 network devices are divided into dicts according to the device type.
Devices are mapped with actual SWaT IP, MAC and netmasks.

Dedicated dict map and set each SWaT network level link parameters.
It is also possible to fine tune each link in a single network level.

Network level node numbers are stored in constats eg: L3_NODES, and
they are used for example to distribute evenly CPU processing power.

Dict key mirror where possible mininet device names, indeed it is
super easy to create a new Topo class using those dictionaries.

There is a logger for each module/module_tests pair. Each pair
reference to the same object instance and save log into
minicps/log/modname.log. Log format and filters are hardcoded,
naming is implicit and you can set logs dimensions and number of
rotations through this module.

POX controller logs is stored into dedicated logs/POXControllerName.log
file. Each time the log file is overwritten, unlike minicps module logging
facility.
"""

import logging
import logging.handlers
from mininet.util import dumpNodeConnections


# LOGGING AND TESTING

# TEST_LOG_LEVEL='output'
TEST_LOG_LEVEL='info'
# TEST_LOG_LEVEL='debug'

TEMP_DIR = './temp'

def _buildLogger(loggername, maxBytes, backupCount):
    """Build a logger obj named loggername that generates
    loggername.log[.n] rotating log files with every level
    (log, file, console) hardcoded to DEBUG.
    The format is hardcoded as well.

    :loggername: name of the logger instance
    :maxBytes: maximum bytes per rotating log file
    :backupCount: maximum number of rotating files
    :returns: logger instance

    """

    # TODO: find a way to not hardcode the level
    
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)

    fh = logging.handlers.RotatingFileHandler(
            './logs/'+loggername+'.log',
            maxBytes=maxBytes,
            backupCount=backupCount)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

LOG_BYTES = 20000
LOG_ROTATIONS = 5
logger = _buildLogger(__name__, LOG_BYTES, LOG_ROTATIONS)

ASSERTION_ERRORS = {
    'ip_mismatch': 'IP mismatch',
    'mac_mismatch': 'MAC mismatch',
    'no_learning': 'No learning',
}


# OPENFLOW

POX_PATH='~/'

def _pox_opts(mod_path, info_level, logfile_opts,
        log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):

    """Generate a string with custom pox options.

    :mod_path: dot notation path to the pox controller implementation
    :info_level: DEBUG, INFO, ecc...
    :logfile_opts: path and other options (eg: file.log,w to overwrite each time)
    :returns: options string for ./pox.py command

    """
    info_level = info_level.upper()
    pox_opts = '%s log.level --%s log --file=%s --format="%s" &' % (mod_path,
            info_level, logfile_opts, log_format)
    # print 'DEBUG:', opts

    return pox_opts
    
OF_TYPES = {
    '0': 'of_hello',
    '2': 'of_echo_request',
    '3': 'of_echo_reply',
    '5': 'of_feature_request',
    '6': 'of_feature_reply',
    '9': 'of_set_config',
    '10': 'of_packet_in',
    '13': 'of_packet_out',
    '14': 'of_flow_add',
    'xx': 'of_join',
    'xx': 'of_port_change',
}

OF_MISC = {
    'user_switch': 'user',
    'kernel_switch': 'ovsk',
    'controller_port': '6633',
}


## MININET

def _mininet_functests(net):
    """Common mininet functional tests can be called inside
    each unittest. The function will be ignored by nose
    during automatic test collection because its name is
    not part of nose convention.
    Remember to manually stop the network after this call.

    :net: Mininet object
    """

    logging.info("Dumping host connections")
    dumpNodeConnections(net.hosts)
    logging.info("Testing network connectivity")
    net.pingAll()
    logging.info("Testing TCP bandwidth btw first and last host")
    net.iperf()
    
L0_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
L1_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
L2_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
L3_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)


## NETWORK CONSTANTS

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
    'plc1': '192.168.1.10',
    'plc2': '192.168.1.20',
    'plc3': '192.168.1.30',
    'plc4': '192.168.1.40',
    'plc5': '192.168.1.50',
    'plc6': '192.168.1.60',
    'plc1r': '192.168.1.11',
    'plc2r': '192.168.1.21',
    'plc3r': '192.168.1.31',
    'plc4r': '192.168.1.41',
    'plc5r': '192.168.1.51',
    'plc6r': '192.168.1.61',
    # used as central hub
    'plc7': '192.168.1.70',
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
    'pcn_ap': '192.168.1.103',  # plant control network
    'dmz_ap': '192.168.1.104',
}

L3_PLANT_NETWORK = {
    'histn': '192.168.1.200',
    'workstn': '192.168.1.201',
}

L0_NETMASK = ''
L1_NETMASK = '/24'
L2_NETMASK = ''
L3_NETMASK = '/24'

PLCS_MAC = {
    'plc1': '00:1D:9C:C7:B0:70',
    'plc2': '00:1D:9C:C8:BC:46',
    'plc3': '00:1D:9C:C8:BD:F2',
    'plc4': '00:1D:9C:C7:FA:2C',
    'plc5': '00:1D:9C:C8:BC:2F',
    'plc6': '00:1D:9C:C7:FA:2D',
    'plc1r': '00:1D:9C:C8:BD:E7',
    'plc2r': '00:1D:9C:C8:BD:0D',
    'plc3r': '00:1D:9C:C7:F8:3B',
    'plc4r': '00:1D:9C:C8:BC:31',
    'plc5r': '00:1D:9C:C8:F4:B9',
    'plc6r': '00:1D:9C:C8:F5:DB',
    'plc7': 'TODO',
}

OTHER_MACS = {
    'histn': 'B8:2A:72:D7:B0:EC',
    'workstn': '98:90:96:98:CC:49',
}

PLCS = len(PLCS_MAC)
L1_NODES = 0 # TODO
L2_NODES = 0 # TODO
L3_NODES = PLCS/2 + 2  # 13/2 gives 6


## SWAT

# TODO: use real tag name and data types
# basic atomic types are: INT (16-bit), SINT (8-bit) DINT (32-bit) integer
# and REAL (32-bit float)
TAGS = {
    'pump3': 'pump3=INT[10]',
    'flow3': 'flow3=INT[10]',
}
