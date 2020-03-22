"""
swat-s1 topology
"""

from mininet.topo import Topo as TopoBase

from plc2 import Plc2
from plc1 import Plc1


class Topo(TopoBase):
    NETMASK = '/24'
    NODES = [Plc1, Plc2]

    def build(self):

        switch = self.addSwitch('s1')

        for node in Topo.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topo.NETMASK,
                mac=node.MAC)
            self.addLink(host, switch)
