"""
swat-s1 topology
"""

from mininet.topo import Topo as TopoBase

from plc1 import SwatPLC1
from plc2 import SwatPLC2
from srve import Srve
from clie import Clie

class Topo(TopoBase):
    NETMASK = '/24'
    NODES = [SwatPLC1, SwatPLC2]

    def build(self):

        switch = self.addSwitch('s1')

        for node in Topo.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topo.NETMASK,
                mac=node.MAC)
            self.addLink(host, switch)
