"""
swat-s1 topology
"""

from mininet.topo import Topo as TopoBase

from srv import Srv
from cli import Cli



class Topo(TopoBase):
    NETMASK = '/24'
    NODES = [Srv, Cli]

    def build(self):

        switch = self.addSwitch('s1')

        for node in Topo.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topo.NETMASK,
                mac=node.MAC)
            self.addLink(host, switch)
