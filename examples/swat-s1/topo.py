"""
swat-s1 topology
"""

from mininet.topo import Topo

from utils import IP, MAC


# TODO: add netmasks?
class SwatTopo(Topo):

    """SWaT 6 plcs + attacker + private dirs."""

    def build(self):

        switch = self.addSwitch('s1')

        plc1 = self.addHost(
            'plc1',
            ip=IP['plc1'],
            mac=MAC['plc1'])
        self.addLink(plc1, switch)

        plc2 = self.addHost(
            'plc2',
            ip=IP['plc2'],
            mac=MAC['plc2'])
        self.addLink(plc2, switch)

        plc3 = self.addHost(
            'plc3',
            ip=IP['plc3'],
            mac=MAC['plc3'])
        self.addLink(plc3, switch)

        plc4 = self.addHost(
            'plc4',
            ip=IP['plc4'],
            mac=MAC['plc4'])
        self.addLink(plc4, switch)

        plc5 = self.addHost(
            'plc5',
            ip=IP['plc5'],
            mac=MAC['plc5'])
        self.addLink(plc5, switch)

        plc6 = self.addHost(
            'plc6',
            ip=IP['plc6'],
            mac=MAC['plc6'])
        self.addLink(plc6, switch)

        attacker = self.addHost(
            'attacker',
            ip=IP['attacker'],
            mac=MAC['attacker'])
        self.addLink(attacker, switch)
