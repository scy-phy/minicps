"""
modbus honeypot topology
"""
from mininet import net
from mininet.link import Intf
from mininet.topo import Topo as TopoBase


from srvm import Srvm
from clim import Clim
from clim2 import Clim2

class Topom(TopoBase):
    NETMASK = '/24'
    NODES = [Srvm, Clim, Clim2]

    def build(self):
        #dumbswitch from mininet
        switch = self.addSwitch('s1', inNamespace=False, mac='06:07:38:00:14:eb')
        #s1 = net.addSwitch('s1')
        #Intf('enp0s8', node=s1)

        #switch = self.addSwitch('s1'
        #                        , inNamespace=False
        #                        )
        #addhosts
        for node in Topom.NODES:
            host = self.addHost(
                node.NAME,
                ip=node.IP + Topom.NETMASK,
                mac=node.MAC
            #    ,inNamespace=False
            )
            self.addLink(host, switch)
06