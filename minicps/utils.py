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
import logging.handlers
import os

from mininet.util import dumpNodeConnections
from nose import with_setup

# logging {{{1

# TEST_LOG_LEVEL='output'
TEST_LOG_LEVEL = 'info'
# TEST_LOG_LEVEL='debug'

TEMP_DIR = './temp'


# https://docs.python.org/2/howto/logging.html
def build_debug_logger(
        logger_name,
        bytes_per_file=10000,
        rotating_files=3,
        log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        log_dir='/tmp/',
        suffix='.log'):
    """Build a custom Python debug logger file.

    :logger_name: name of the logger instance
    :bytes_per_file: defaults to 10KB
    :rotating_files: defaults to 3
    :log_format: defaults to time, name, level, message
    :log_dir: defaults to /tmp
    :suffix: defaults to .log
    :returns: logger instance
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # log_path = _getlog_path()
    # assert log_path != None, "No log path found"

    fh = logging.handlers.RotatingFileHandler(
        log_dir + logger_name + suffix,
        maxBytes=bytes_per_file,
        backupCount=rotating_files)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # no thread information
    formatter = logging.Formatter(
        log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


LOG_BYTES = 20000
LOG_ROTATIONS = 5
logger = build_debug_logger(__name__, LOG_BYTES, LOG_ROTATIONS)


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
    pass


def teardown_func(test_name):
    pass


def teardown_func_clear(test_name):
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
