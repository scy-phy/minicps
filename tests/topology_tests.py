"""
Topology tests
"""

from nose.tools import *

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink

from minicps import constants as c
from minicps.topology import EthRing, EthStar


def setup():
    print 'SETUP!'


def teardown():
    print 'TEAR DOWN!'


def test_eth_ring():
    """Test L0 Ethernet ting"""

    net = Mininet(topo=EthRing(n=5),
                  link=TCLink)
    net.start()

    print "Dumpingg host connections"
    dumpNodeConnections(net.hosts)

    print "Testing network connectivity"
    net.pingAll()

    net.stop()


def test_eth_star():
    """Test L1 Ethernet star"""

    net = Mininet(topo=EthStar(n=5),
                  link=TCLink)
    net.start()

    print "Dumpingg host connections"
    dumpNodeConnections(net.hosts)

    print "Testing network connectivity"
    net.pingAll()

    net.stop()
