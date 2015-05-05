"""
Topology tests

with_setup decorator calls setup before each test and teardown after
each tests. It is possible to use different fixtures for different
tests.

SkipTest can be used as a switch to intentionally skip a test. You
can see skipped test summary in the nosetest output.
"""

from nose.tools import *
from nose.plugins.skip import Skip, SkipTest

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink

from minicps import constants as c
from minicps.topology import EthStar, Minicps, DLR, L3EthStar


def setup():
    # print 'SETUP!'
    setLogLevel(c.TEST_LOG_LEVEL)


def teardown():
    # print 'TEAR DOWN!'
    pass


@with_setup(setup, teardown)
def test_EthStar():
    """Test EthStar and index a couple of common test commands"""
    raise SkipTest

    topo = EthStar(n=6)
    net = Mininet(topo)  # TODO: subclass Mininet with Minicps and replace it
    net.start()
    print "DEBUG: Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: Testing TCP bandwidth btw PLC1 and PLC2"
    plc1, plc2 = net.get('plc1', 'plc2')  # get host obj reference by name
    net.iperf((plc1, plc2))  # passed as a tuple
    print "DEBUG: stopping the network"
    net.stop()


@with_setup(setup, teardown)
def test_L3EthStar():
    """Test L3EthStar with custom L3_LINKOPTS"""
    # raise SkipTest

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    print "DEBUG: Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: Testing TCP bandwidth btw PLC1 and PLC2"
    plc1, plc2 = net.get('plc1', 'plc2')
    net.iperf((plc1, plc2))
    print "DEBUG: stopping the network"
    net.stop()


@with_setup(setup, teardown)
def test_DLR():
    """Test DLR ring"""
    raise SkipTest

    topo = DLR(n=2)
    net = Mininet(topo)
    net.start()
    print "DEBUG: Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: stopping the network"
    net.stop()


    
