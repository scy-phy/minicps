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
from minicps.topology import EthStar, Minicps, DLR


def setup():
    print 'SETUP!'


def teardown():
    print 'TEAR DOWN!'


def test_DLR():
    """Test DLR ring"""

    setLogLevel(c.TEST_LOG_LEVEL)

    topo = DLR(n=2)
    net = Mininet(topo)
    net.start()
    print "DEBUG: Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: stopping the network"
    net.stop()


def test_EthStar():
    """Test EthStar and index a couple of common test commands"""

    setLogLevel(c.TEST_LOG_LEVEL)

    topo = EthStar(n=2)
    net = Mininet(topo)
    net.start()
    print "DEBUG: Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: stopping the network"
    net.stop()
    
    topo = EthStar(n=6)
    net = Mininet(topo)  # TODO: subclass Mininet with Minicps and replace it
    net.start()
    print "DEBUG: Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: Testing TCP bandwidth"
    net.pingAll()
    print "DEBUG: stopping the network"
    net.stop()
