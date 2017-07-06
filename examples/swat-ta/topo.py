"""
swat-ta topology
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Node
from mininet.log import setLogLevel, info

from utils import IP, MAC, NETMASK


class SwatTopo(Topo):

    """SWaT L1 with 6 PLCs."""

    def build(self):

        switch = self.addSwitch('s1')

        plc1 = self.addHost(
            'plc1',
            ip=IP['plc1'] + NETMASK,
            mac=MAC['plc1'])
        self.addLink(plc1, switch)

        plc2 = self.addHost(
            'plc2',
            ip=IP['plc2'] + NETMASK,
            mac=MAC['plc2'])
        self.addLink(plc2, switch)

        plc3 = self.addHost(
            'plc3',
            ip=IP['plc3'] + NETMASK,
            mac=MAC['plc3'])
        self.addLink(plc3, switch)

        plc4 = self.addHost(
            'plc4',
            ip=IP['plc4'] + NETMASK,
            mac=MAC['plc4'])
        self.addLink(plc4, switch)

        plc5 = self.addHost(
            'plc5',
            ip=IP['plc5'] + NETMASK,
            mac=MAC['plc5'])
        self.addLink(plc5, switch)

        plc6 = self.addHost(
            'plc6',
            ip=IP['plc6'] + NETMASK,
            mac=MAC['plc6'])
        self.addLink(plc6, switch)


if __name__ == "__main__":
    """Test SwatTopo."""

    topo = SwatTopo()
    net = Mininet(topo=topo)
    net.start()

    CLI(net)

    net.stop()

