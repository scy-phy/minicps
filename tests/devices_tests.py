"""
Devices tests

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


def setup():
    # print 'SETUP!'
    setLogLevel(c.TEST_LOG_LEVEL)


def teardown():
    # print 'TEAR DOWN!'
    pass


def assert_learning(ping_output):
    """Naive learning check on the first two ping
    ICMP packets RTT.

    :ping_output: given as a string.
    """
    print 'DEBUG ping_output:\n', ping_output

    lines = ping_output.split('\n')
    first = lines[1]
    second = lines[2]
    first_words = first.split(' ')
    second_words = second.split(' ')
    first_time = first_words[6]
    second_time = second_words[6]

    first_time = float(first_time[5:])
    second_time = float(second_time[5:])

    print 'DEBUG first_time:', first_time
    print 'DEBUG second_time:', second_time

    assert_greater(first_time, second_time,
            c.ASSERTION_ERRORS['no_learning'])


@with_setup(setup, teardown)
def test_POXL2Pairs():
    """Test build-in forwarding.l2_pairs controller
    that adds flow entries using only MAC info.
    """
    # raise SkipTest

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()

    plc1, plc2 = net.get('plc1', 'plc2')
    ping_output = plc1.cmd('ping -c3 %s' % plc2.IP())
    
    assert_learning(ping_output)
    # CLI(net)

    net.stop()
    os.system('sudo mn -c')


@with_setup(setup, teardown)
def test_POXL2Learning():
    """Test build-in forwarding.l2_learning controller
    that adds flow entries using only MAC info.
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXL2Learning
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()

    plc1, plc2 = net.get('plc1', 'plc2')
    output = plc1.cmd('ping -c6 %s' % plc2.IP())
    print 'DEBUG output:\n', output

    # CLI(net)

    net.stop()
    os.system('sudo mn -c')
