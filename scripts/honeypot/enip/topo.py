from mininet.topo import Topo as TopoBase

from plc1 import SwatPLC1
from plc2 import SwatPLC2

# Defines network topology for this simulation. All nodes
# (SwatPLC1 & SwatPLC2) are connected to a single switch 's1'.
class Topo(TopoBase):
    NETMASK = '/24'
    NODES = [SwatPLC1, SwatPLC2]

    def build(self):

        switch = self.addSwitch('s1', inNamespace=False, mac='06:07:38:00:14:eb')

        for node in Topo.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topo.NETMASK,
                mac=node.MAC)
            self.addLink(host, switch)
