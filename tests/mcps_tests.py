"""
mcps_tests.

Contains functional tests.
"""

import os

from nose.plugins.skip import SkipTest

from mininet.topo import Topo, LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import Controller, CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
# from mininet.cli import CLI

from minicps.mcps import MiniCPS


# testing helper classes {{{1
# taken from mininet pages
class SingleSwitchTopo(Topo):

    """Single switch connected to n hosts."""

    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)


class SingleSwitchTopoTCLinkCPULimitedHost(Topo):

    """Single switch connected to n hosts."""

    def build(self, n=2):
        switch = self.addSwitch('s1')
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost(
                'h%s' % (h + 1),
                cpu=.5 / n)
            # 10 Mbps, 5ms delay, 10% loss, 1000 packet queue
            self.addLink(
                host, switch,
                bw=10, delay='5ms', loss=10,
                max_queue_size=1000, use_htb=True)


class POXBridge(Controller):

    """Custom Controller class to invoke POX forwarding.l2_learning."""

    def start(self):
        "Start POX learning switc"
        self.pox = '%s/pox/pox.py' % os.environ['HOME']
        self.cmd(self.pox, 'forwarding.l2_learning &')

    def stop(self):
        "Stop POX"
        self.cmd('kill %' + self.pox)


@SkipTest
def test_MininetLinearTopo():

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

    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo=topo)

    try:
        mcps = MiniCPS(
            name='test_MiniCPS',
            net=net)
    except Exception as e:
        print 'TEST test_MiniCPS error: ', e


@SkipTest
def test_MiniCPSTCLinkCPULimitedHost():

    print
    topo = SingleSwitchTopoTCLinkCPULimitedHost(n=4)
    net = Mininet(
        topo=topo,
        link=TCLink)

    mcps = MiniCPS(
        name='name',
        net=net)


@SkipTest
def test_MiniCPSCustomController():

    print
    topo = SingleSwitchTopo(n=4)
    net = Mininet(
        topo=topo,
        controller=POXBridge)

    mcps = MiniCPS(
        name='name',
        net=net)
