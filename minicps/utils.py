"""
utils.py.

MiniCPS use a shared logger called mcps_logger.

It contains testing data objects.
TEST_LOG_LEVEL affects all the tests,
output, info and debug are in increasing order of verbosity.

It contains all the others data objects.
"""

import logging
import logging.handlers
import time
import os

from mininet.util import dumpNodeConnections

# logging {{{1
# https://docs.python.org/2/howto/logging.html

# TODO: add a parametric logging level
def build_debug_logger(
        name='log_name',
        bytes_per_file=10000,
        rotating_files=3,
        lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        ldir='/tmp/',
        suffix=''):
    """Build a custom Python debug logger file.

    :name: name of the logger instance
    :bytes_per_file: defaults to 10KB
    :rotating_files: defaults to 3
    :lformat: defaults to time, name, level, message
    :ldir: defaults to /tmp
    :suffix: defaults to .log

    :returns: logger instance
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # log_path = _getlog_path()
    # assert log_path != None, "No log path found"

    fh = logging.handlers.RotatingFileHandler(
        ldir + name + suffix,
        maxBytes=bytes_per_file,
        backupCount=rotating_files)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # no thread information
    formatter = logging.Formatter(
        lformat)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


TEMP_DIR = '/tmp'

LOG_DIR = 'logs/'
LOG_BYTES = 20000
LOG_ROTATIONS = 5

# MiniCPS global logger
mcps_logger = build_debug_logger(
    name=__name__,
    bytes_per_file=LOG_BYTES,
    rotating_files=LOG_ROTATIONS,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir=LOG_DIR,
    suffix='')


# multi-process {{{1

# http://stackoverflow.com/questions/1359383/python-run-a-process-and-kill-it-if-it-doesnt-end-within-one-hour
def wait_timeout(proc, seconds):

    """Wait for a process to finish, or raise exception after timeout

    :proc: subprocess.Popen instance
    :seconds: before raising the exception
    """

    start = time.time()
    end = start + seconds
    interval = min(seconds / 1000.0, .25)

    while True:
        result = proc.poll()
        if result is not None:
            return result
        if time.time() >= end:
            raise RuntimeError("Process timed out")
        time.sleep(interval)

# testing {{{1

def setup_func(test_name):
    pass


def teardown_func(test_name):
    pass


# TODO: test it
def _arp_cache_rtts(net, h1, h2):
    """Learning check on the first two ping ICMP packets RTT.

    :net: Mininet object.
    :h1: first host name.
    :h2: second host name.
    :returns: decimal RTTs from uncached and cacthed arp entries.
    """

    h1, h2 = net.get(h1, h2)

    delete_arp_cache = h1.cmd('ip -s -s neigh flush all')

    ping_output = h1.cmd('ping -c5 %s' % h2.IP())

    lines = ping_output.split('\n')
    first = lines[1]
    second = lines[2]
    first_words = first.split(' ')
    second_words = second.split(' ')
    first_rtt = first_words[6]
    second_rtt = second_words[6]
    first_rtt = float(first_rtt[5:])
    second_rtt = float(second_rtt[5:])

    return first_rtt, second_rtt
