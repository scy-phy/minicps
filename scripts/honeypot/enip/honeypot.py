from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from topo import Topo

import sys
from mininet.log import lg

class Honeypot(MiniCPS):
    """Main simulation container"""

    def __init__(self):
        #loglevel & ping mininet topology
        lg.setLogLevel('debug')

        # Start Mininet with our topology defined in Topom
        self.net = Mininet(topo=Topo())

        # You can use the following section to debug settings
        #switch = self.net.getNodeByName('s1')
        #self.intf = Intf('tap0', node=switch)
        #self.net.addNAT().configDefault()

        self.net.start()

        # Verify connectivity
        self.net.pingAll()

        # Execute plc1.py, plc2.py scripts on their respective nodes
        for node_class in Topo.NODES:
            # Get node on which to execute the script
            node = self.net.get(node_class.NAME)

            # Instruct mininet to execute the script on that node
            node.cmd(sys.executable + ' {}.py &'.format(node_class.NAME))

        # Start Mininet command line and let it use our self.net Mininet object
        CLI(self.net)

        # Stop Mininet
        self.net.stop()

if __name__ == "__main__":
    honeypot = Honeypot()
