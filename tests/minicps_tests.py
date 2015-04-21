"""
Functional test
"""

from nose.tools import *

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink


def setup():
    print 'SETUP!'


def teardown():
    print 'TEAR DOWN!'


def test_basic():
    """ Pingall a linear topology. """

    net = Mininet(topo=LinearTopo(n=5),
                  link=TCLink)
    net.start()

    print "Dumpingg host connections"
    dumpNodeConnections(net.hosts)

    print "Testing network connectivity"
    net.pingAll()

    net.stop()
