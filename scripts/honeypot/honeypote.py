

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from enip_old.topoe import Topoe

import sys
from mininet.log import lg

class Honeypote(MiniCPS):
    """Main container used to run the simulation."""

    def __init__(self):
        self.name = 'honeypote'
        self.net = Mininet(topo=Topoe())

        lg.setLogLevel('debug')
        self.net.start()
        self.net.pingAll()

        # start devices
        for node_class in Topoe.NODES:
            node = self.net.get(node_class.NAME)
            node.cmd(sys.executable + ' {}.py &'.format(node_class.NAME))

        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":
    honeypot = Honeypote()
