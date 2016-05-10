"""
minicps constants.

TEST_LOG_LEVEL affetcs all the tests.
output, info and debug are in increasing order of verbosity.

There is a logger for each module/module_tests pair. Each pair
reference to the same object instance and save log into
minicps/log/modname.log. Log format and filters are hardcoded,
naming is implicit and you can set logs dimensions and number of
rotations through this module.

POX controller logs is stored into dedicated logs/POXControllerName.log file.
Each time the log file is overwritten, unlike minicps module logging facility.
"""

import logging
import logging.handlers
from mininet.util import dumpNodeConnections

from nose.tools import *

import os




# mirrors minicps constants
OF10_MSG_TYPES = {
    0: 'OFPT_HELLO',  # Symmetric
    1: 'OFPT_ERROR',  # Symmetric
    2: 'OFPT_ECHO_REQUEST',  # Symmetric
    3: 'OFPT_ECHO_REPLY',  # Symmetric
    4: 'OFPT_VENDOR',  # Symmetric

    5: 'OFPT_FEATURES_REQUEST',  # Controller -> Switch
    6: 'OFPT_FEATURES_REPLY',  # Switch -> Controller
    7: 'OFPT_GET_CONFIG_REQUEST',  # Controller -> Switch
    8: 'OFPT_GET_CONFIG_REPLY',  # Switch -> Controller
    9: 'OFPT_SET_CONFIG',  # Controller -> Switch

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


## ENIP

ENIP_MISC = {
    'tcp_port': 44818,
    'udp_port': 2222,
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



# LOGGING AND TESTING

# TEST_LOG_LEVEL='output'
TEST_LOG_LEVEL = 'info'
# TEST_LOG_LEVEL='debug'

TEMP_DIR = './temp'

# def _getlog_path():
#     """
#     :returns: path to minicps/logs

#     """
#     cwd = os.getcwd()
#     print 'DEBUG _getlog_path: cwd %s' % cwd
#     log_path = None

#     index = cwd.find('minicps/')

#     if index == -1:
#         log_path = 'logs/'
#     else:
#         log_path = cwd[0:index]+'logs'
#     print 'DEBUG _getlog_path: log_path %s' % log_path

#     return log_path


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

    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)

    # log_path = _getlog_path()
    # assert log_path != None, "No log path found"

    fh = logging.handlers.RotatingFileHandler(
        # log_path+loggername+'.log',
        'logs/' + loggername + '.log',
        maxBytes=maxBytes,
        backupCount=backupCount)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # no thread information
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
