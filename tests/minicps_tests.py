"""
minicps_tests.

Contains functional tests.
"""

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
# from mininet.cli import CLI


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
