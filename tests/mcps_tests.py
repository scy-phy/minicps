"""
mcps_tests.

Contains functional tests.
"""

from mininet.topo import Topo, LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
# from mininet.cli import CLI

from minicps.mcps import MiniCPS

from nose.plugins.skip import SkipTest


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)


@SkipTest
def test_MininetLinearTopo():
    """Dump and pingall a mininet linear topology."""

    net = Mininet(topo=LinearTopo(n=5),
                  link=TCLink)
    net.start()

    print "Dumpingg host connections"
    dumpNodeConnections(net.hosts)

    print "Testing network connectivity"
    net.pingAll()

    # CLI(net)

    net.stop()


def test_MiniCPS():

    print
    topo = SingleSwitchTopo(n=4)
    net = Mininet(
        topo=topo)

    mcps = MiniCPS(
        name='name',
        net=net)


@SkipTest  # TODO
def test_MiniCPS_TCLink():

    print
    topo = TODO
    net = Mininet(
        topo=topo,
        link=TCLink)

    mcps = MiniCPS(
        name='name',
        net=net)


@SkipTest  # TODO
def test_MiniCPS_CPULimitedHost():

    print
    topo = TODO
    net = Mininet(
        topo=topo,
        host=CPULimitedHost)

    mcps = MiniCPS(
        name='name',
        net=net)
