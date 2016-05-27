"""
toy topology
"""

from mininet.topo import Topo

from utils import PLC1_MAC, PLC2_MAC
from utils import PLC1_ADDR, PLC2_ADDR


class ToyTopo(Topo):

    def build(self):

        switch = self.addSwitch('s1')

        plc1 = self.addHost(
            'plc1',
            ip=PLC1_ADDR,
            mac=PLC1_MAC)
        self.addLink(plc1, switch)

        plc2 = self.addHost(
            'plc2',
            ip=PLC2_ADDR,
            mac=PLC2_MAC)
        self.addLink(plc2, switch)
