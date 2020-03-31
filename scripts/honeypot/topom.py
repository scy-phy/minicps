"""
modbus honezpot topology
"""

from mininet.topo import Topo as TopoBase

from srvm import Srvm
from clim import Clim

class Topom(TopoBase):
    NETMASK = '/24'
    NODES = [Srvm, Clim]

    def build(self):
        #dumbswitch from mininet
        switch = self.addSwitch('s1')
        #addhosts
        for node in Topom.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topom.NETMASK,
                mac=node.MAC)
            self.addLink(host, switch)
