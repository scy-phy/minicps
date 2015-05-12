"""
Devices tests

By default Mininet runs Open vSwitch in OpenFlow mode,
which requires an OpenFlow controller.

Controller subclasses are started and stopped automatically by Mininet.

RemoteController must be started and stopped by the user.

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


@with_setup(setup, teardown)
def test_POXL2Pairs():
    """Test build-in forwarding.l2_pairs controller
    that adds flow entries using only MAC info.
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()

    plc1, plc2 = net.get('plc1', 'plc2')
    output = plc1.cmd('ping -c3 %s' % plc2.IP())
    print 'DEBUG output:\n', output
    # CLI(net)

    net.stop()
    os.system('sudo mn -c')


@with_setup(setup, teardown)
def test_POXL2Learning():
    """Test build-in forwarding.l2_learning controller
    that adds flow entries using only MAC info.
    """
    # raise SkipTest

    topo = L3EthStar()
    controller = POXL2Learning
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()

    # plc1, plc2 = net.get('plc1', 'plc2')
    # output = plc1.cmd('ping -c3 %s' % plc2.IP())
    # print 'DEBUG output:\n', output
    CLI(net)

    net.stop()
    os.system('sudo mn -c')
