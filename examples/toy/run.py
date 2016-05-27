"""
toy run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from topo import ToyTopo

import sys


class ToyCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        self.net.start()

        # start devices
        # plc1, plc2 = self.net.get('plc1', 'plc2')
        # plc1.cmd(sys.executable + ' plc1.py &')
        # plc2.cmd(sys.executable + ' plc2.py &')

        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = ToyTopo()
    net = Mininet(topo=topo)

    toycps = ToyCPS(
        name='toyCPS',
        net=net)
