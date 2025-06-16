"""
modbus honeypot topology
"""
from mininet import net
from mininet.link import Intf
from mininet.topo import Topo as TopoBase


from srvm import Srvm
from clim import Clim
from clim2 import Clim2

# Defines network topology for this simulation. All nodes
# (Srvm, Clim, Clim2) are connected to a single switch 's1'.
class Topom(TopoBase):
    NETMASK = '/24'
    NODES = [Srvm, Clim, Clim2]

    def build(self):
        #dumbswitch from mininet, static routing required on the VPS
        switch = self.addSwitch('s1', inNamespace=False, mac='06:07:38:00:14:eb')

        for node in Topom.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topom.NETMASK,
                mac=node.MAC
            #    ,inNamespace=False
            )
            self.addLink(host, switch)
