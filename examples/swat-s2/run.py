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

        net.start()

        net.pingAll()

        # start devices
        plc1, plc2, plc3, dev1, dev2, dev3, dev4, dev5, dev6, s1 = self.net.get(
            'plc1', 'plc2', 'plc3', 'dev1', 'dev2', 'dev3', 'dev4','dev5', 'dev6', 's1')

        # SPHINX_SWAT_TUTORIAL RUN(
        # dev1.cmd('python2' + ' dev1.py &')
        # dev2.cmd('python2' + ' dev2.py &')
        # dev3.cmd('python2' + ' dev3.py &')
        # dev4.cmd('python2' + ' dev4.py &')
        # dev5.cmd('python2' + ' dev5.py &')
        # dev6.cmd('python2' + ' dev6.py &')
        # plc2.cmd('python2' + ' plc2.py &')
        # plc3.cmd('python2' + ' plc3.py &')
        # plc1.cmd('python2' + ' plc1.py &')
        # s1.cmd(sys.executable + ' physical_process.py &')
        # SPHINX_SWAT_TUTORIAL RUN)

        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    swat_s1_cps = SwatS1CPS(
        name='swat_s1',
        net=net)
