"""
utils.py.

It contains logging data objects.
There is a logger for each module/module_tests pair. Each pair
reference to the same object instance and save log into
minicps/log/modname.log. Log format and filters are hardcoded,
naming is implicit and you can set logs dimensions and number of
rotations through this module.
POX controller logs is stored into dedicated logs/POXControllerName.log file.
Each time the log file is overwritten, unlike minicps module logging facility.

It contains testing data objects.
TEST_LOG_LEVEL affects all the tests,
output, info and debug are in increasing order of verbosity.

It contains all the others data objects.
"""

import logging
import os

from mininet.util import dumpNodeConnections
from nose import with_setup

# logging {{{1

# TEST_LOG_LEVEL='output'
TEST_LOG_LEVEL = 'info'
# TEST_LOG_LEVEL='debug'

TEMP_DIR = './temp'


def build_logger(loggername, maxBytes, backupCount):
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
logger = build_logger(__name__, LOG_BYTES, LOG_ROTATIONS)

ASSERTION_ERRORS = {
    'ip_mismatch': 'IP mismatch',
    'mac_mismatch': 'MAC mismatch',
    'no_learning': 'No learning',
}


# testing {{{1

MININET_CMDS = {
    'clear': 'sudo mn -c',
    'linear-remote': 'sudo mn --topo=linear,4 --controller=remote',
}


def mininet_functests(net):
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


# others {{{1
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
