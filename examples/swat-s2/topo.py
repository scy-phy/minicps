"""
swat-s1 topology
"""

from mininet.topo import Topo

from utils import IP, MAC, NETMASK


class SwatTopo(Topo):

    """SWaT 3 plcs + attacker + private dirs."""

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

        dev1 = self.addHost(
            'dev1',
            ip=IP['dev1'] + NETMASK,
            mac=MAC['dev1'])
        self.addLink(dev1, switch)

        dev2 = self.addHost(
            'dev2',
            ip=IP['dev2'] + NETMASK,
            mac=MAC['dev2'])
        self.addLink(dev2, switch)

        dev3 = self.addHost(
            'dev3',
            ip=IP['dev3'] + NETMASK,
            mac=MAC['dev3'])
        self.addLink(dev3, switch)

        dev4 = self.addHost(
            'dev4',
            ip=IP['dev4'] + NETMASK,
            mac=MAC['dev4'])
        self.addLink(dev4, switch)

        dev5 = self.addHost(
            'dev5',
            ip=IP['dev5'] + NETMASK,
            mac=MAC['dev5'])
        self.addLink(dev5, switch)

        dev6 = self.addHost(
            'dev6',
            ip=IP['dev6'] + NETMASK,
            mac=MAC['dev6'])
        self.addLink(dev6, switch)

        dev7 = self.addHost(
            'dev7',
            ip=IP['dev7'] + NETMASK,
            mac=MAC['dev7'])
        self.addLink(dev7, switch)


        attacker = self.addHost(
            'attacker',
            ip=IP['attacker'] + NETMASK,
            mac=MAC['attacker'])
        self.addLink(attacker, switch)
