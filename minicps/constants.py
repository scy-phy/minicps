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

POX controller logs is stored into dedicated logs/POXControllerName.log file. Each time the log file is overwritten, unlike minicps module logging facility.
"""

import logging
import logging.handlers
from mininet.util import dumpNodeConnections

from nose.tools import *

import os

# OPENFLOW

POX_PATH='~/'

POX = {
    './pox.py openflow.of_01 --port=6633 --address=127.0.0.1 log.level --DEBUG swat_controller',
}

def _pox_opts(components, info_level, logfile_opts,
        log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):

    """Generate a string with custom pox options.

    :components: dot notation paths (eg: forwarding.l2_learning web.webcore --port=8888)
    :info_level: DEBUG, INFO, ecc...
    :logfile_opts: path and other options (eg: file.log,w to overwrite each time)
    :returns: options string for ./pox.py command

    """
    info_level = info_level.upper()
    pox_opts = '%s log.level --%s log --file=%s --format="%s" &' % (components,
            info_level, logfile_opts, log_format)
    # print 'DEBUG:', opts

    return pox_opts
    
# mirrors minicps constants
OF10_MSG_TYPES= {
    0:  'OFPT_HELLO',  # Symmetric 
    1:  'OFPT_ERROR',  # Symmetric 
    2:  'OFPT_ECHO_REQUEST',  # Symmetric 
    3:  'OFPT_ECHO_REPLY',  # Symmetric 
    4:  'OFPT_VENDOR',  # Symmetric 

    5:  'OFPT_FEATURES_REQUEST',  # Controller -> Switch
    6:  'OFPT_FEATURES_REPLY',  # Switch -> Controller
    7:  'OFPT_GET_CONFIG_REQUEST',  # Controller -> Switch
    8:  'OFPT_GET_CONFIG_REPLY',  # Switch -> Controller
    9:  'OFPT_SET_CONFIG',  # Controller -> Switch

    10: 'OFPT_PACKET_IN',  # Async, Switch -> Controller
    11: 'OFPT_FLOW_REMOVED',  # Async, Switch -> Controller
    12: 'OFPT_PORT_STATUS',  # Async,  Switch -> Controller

    13: 'OFPT_PACKET_OUT',  # Controller -> Switch
    14: 'OFPT_FLOW_MOD',  # Controller -> Switch
    15: 'OFPT_PORT_MOD',  # Controller -> Switch

    16: 'OFPT_STATS_REQUEST',  # Controller -> Switch
    17: 'OFPT_STATS_REPLY',  # Switch -> Controller

    18: 'OFPT_BARRIER_REQUEST',  # Controller -> Switch
    19: 'OFPT_BARRIER_REPLY',  # Switch -> Controller

    20: 'OFPT_QUEUE_GET_CONFIG_REQUEST',  # Controller -> Switch
    21: 'OFPT_QUEUE_GET_CONFIG_REPLY',  # Switch -> Controller
}


OF_MISC = {
    'user_switch': 'user',
    'kernel_switch': 'ovsk',
    'controller_port': 6633,
    'switch_debug_port': 6634,
    'flood_port': 65531,
}


## MININET

MININET_CMDS = {
    'clear': 'sudo mn -c',
    'linear-remote': 'sudo mn --topo=linear,4 --controller=remote',
}

def _arp_cache_rtts(net, h1, h2):
    """Naive learning check on the first two ping
    ICMP packets RTT.

    :net: Mininet object.
    :h1: first host name.
    :h2: second host name.
    :returns: decimal RTTs from uncached and cacthed arp entries.
    """

    h1, h2 = net.get(h1, h2)

    delete_arp_cache = h1.cmd('ip -s -s neigh flush all')
    logger.debug('delete_arp_cache: %s' % delete_arp_cache)

    ping_output = h1.cmd('ping -c5 %s' % h2.IP())
    logger.debug('ping_output: %s' % ping_output)

    lines = ping_output.split('\n')
    first = lines[1]
    second = lines[2]
    first_words = first.split(' ')
    second_words = second.split(' ')
    first_rtt = first_words[6]
    second_rtt = second_words[6]
    first_rtt = float(first_rtt[5:])
    second_rtt = float(second_rtt[5:])
    logger.debug('first_rtt: %s' % first_rtt)
    logger.debug('second_rtt: %s' % second_rtt)

    return first_rtt, second_rtt

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


## SWAT

# TODO: use real tag name and data types
# basic atomic types are: INT (16-bit), SINT (8-bit) DINT (32-bit) integer
# and REAL (32-bit float)
TAGS = {
    'pump3': 'pump3=INT[10]',
    'flow3': 'flow3=INT[10]',
}


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


def setup_func(test_name):
    logger.info('Inside %s' % test_name)

def teardown_func(test_name):
    logger.info('Leaving %s' % test_name)

def teardown_func_clear(test_name):
    logger.info('Leaving %s' % test_name)
    os.system(MININET_CMDS['clear'])

def with_named_setup(setup=None, teardown=None):
    def wrap(f):
        return with_setup(
            lambda: setup(f.__name__) if (setup is not None) else None, 
            lambda: teardown(f.__name__) if (teardown is not None) else None)(f)
    return wrap
