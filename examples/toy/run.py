"""
toy run.py
"""

import os
import sys
# TODO: find a nicer way to manage path
sys.path.append(os.getcwd())

from mininet.topo import Topo
from mininet.net import Mininet

from minicps.mcps import MiniCPS

from examples.toy.utils import PLC1_MAC, PLC2_MAC
from examples.toy.utils import PLC1_ADDR, PLC2_ADDR


class ToyTopo(Topo):

    """Single switch connected to n hosts."""

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


if __name__ == "__main__":

    topo = ToyTopo()
    net = Mininet(
        topo=topo)

    MiniCPS(
        name='toy',
        net=net)
