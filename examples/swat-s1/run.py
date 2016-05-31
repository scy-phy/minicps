"""
swat-s1 run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS

from topo import SwatTopo

import sys


class SwatS1CPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        self.net.start()

        # start devices
        plc1, plc2, plc3 = self.net.get('plc1', 'plc2', 'plc3')

        # TODO: start physical process in background using Popen
        # plc2.cmd(sys.executable + ' plc2.py &')
        # plc3.cmd(sys.executable + ' plc3.py &')
        # plc1.cmd(sys.executable + ' plc1.py &')

        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    toycps = SwatS1CPS(
        name='swat_s1',
        net=net)
