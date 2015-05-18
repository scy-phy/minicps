"""
Devices tests

time.sleep is used after net.start() to synch python interpreter with
the mininet init process.
"""

from nose.tools import *
from nose.plugins.skip import Skip, SkipTest

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI

from minicps import constants as c
from minicps.topology import EthStar, Minicps, DLR, L3EthStar
from minicps.devices import POXL2Pairs, POXL2Learning

import os
import time

import logging
logger = logging.getLogger('minicps.devices')
setLogLevel(c.TEST_LOG_LEVEL)


def setup_func(test_name):
    logger.info('Inside %s' % test_name)

def teardown_func(test_name):
    logger.info('Leaving %s' % test_name)

def with_named_setup(setup=None, teardown=None):
    def wrap(f):
        return with_setup(
            lambda: setup(f.__name__) if (setup is not None) else None, 
            lambda: teardown(f.__name__) if (teardown is not None) else None)(f)
    return wrap


def arp_cache_rtts(net, h1, h2):
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


@with_named_setup(setup_func, teardown_func)
def test_POXL2Pairs():
    """Test build-in forwarding.l2_pairs controller
    that adds flow entries using only MAC info.
    """
    # raise SkipTest

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(first_rtt, second_rtt,
                c.ASSERTION_ERRORS['no_learning'])
        deltas.append(first_rtt - second_rtt)
    logger.debug('deltas: %s' % deltas.__str__())

    # CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXL2Learning():
    """Test build-in forwarding.l2_learning controller
    that adds flow entries using only MAC info.
    """
    # raise SkipTest

    topo = L3EthStar()
    controller = POXL2Learning
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(first_rtt, second_rtt,
                c.ASSERTION_ERRORS['no_learning'])
        deltas.append(first_rtt - second_rtt)
    logger.debug('deltas: %s' % deltas.__str__())

    # CLI(net)

    net.stop()
