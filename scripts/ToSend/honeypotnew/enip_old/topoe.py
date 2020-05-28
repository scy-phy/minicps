"""
swat-s1 topology
"""

from mininet.topo import Topo as TopoBase

from srve import Srve
from clie import Clie

class Topoe(TopoBase):
    NETMASK = '/24'
    NODES = [Srve, Clie]

    def build(self):

        switch = self.addSwitch('s1')

        for node in Topoe.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topoe.NETMASK,
                mac=node.MAC)
            self.addLink(host, switch)
