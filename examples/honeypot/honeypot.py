"""
swat-s1 run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS

from topo import Topom

import sys


class Honeypot(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        for node_class in Topom.NODES:
            node = self.net.get(node_class.NAME)
            node.cmd(sys.executable + ' {}.py &'.format(node_class.NAME))

        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = Topom()
    net = Mininet(topo=topo)

    honeypot = Honeypot(
        name='swat_s1',
        net=net)
