#!/usr/bin/env python

"""
s3-mix topology

"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Node
from mininet.log import setLogLevel, info

from utils import IP, MAC, NETMASK
from utils import IP_SWAT, MAC_SWAT, NETMASK_SWAT
from subprocess import call

class AttackerNode(Node):
    """AttackerNode starts an OpenVPN server."""

    def config(self, **params):
        super(AttackerNode, self).config(**params)

        self.cmd('ifconfig attacker-eth1 10.0.0.1')
        self.cmd('sh bridge-start.sh')
        self.cmd('openvpn openvpn-server.conf &')

    def terminate(self):

        self.cmd('pkill openvpn')
        self.cmd('sh bridge-stop.sh')

        super(AttackerNode, self).terminate()


class AttackerNode2(Node):
    """AttackerNode2 starts an OpenVPN server2."""

    def config(self, **params):
        super(AttackerNode2, self).config(**params)

        self.cmd('ifconfig attacker2-eth1 10.0.0.2')
        self.cmd('sh bridge-start2.sh')
        self.cmd('openvpn openvpn-server2.conf &')

    def terminate(self):

        self.cmd('pkill openvpn')
        self.cmd('sh bridge-stop2.sh')

        super(AttackerNode2, self).terminate()


class ClientNode(Node):
    """ClientNode starts an OpenVPN client."""

    def config(self, **params):
        super(ClientNode, self).config(**params)

        self.cmd('openvpn openvpn-client.conf &')

    def terminate(self):

        super(ClientNode, self).terminate()


class ClientNode2(Node):
    """ClientNode starts an OpenVPN client2."""

    def config(self, **params):
        super(ClientNode2, self).config(**params)

        self.cmd('openvpn openvpn-client2.conf &')

    def terminate(self):

        super(ClientNode2, self).terminate()


class MixTopo(Topo):
    """No subnets."""

    def build(self):

        # NOTE: swat
        switch = self.addSwitch('s1')


        plc2 = self.addHost(
            'plc2',
            ip=IP_SWAT['plc2'] + NETMASK_SWAT,
            mac=MAC_SWAT['plc2'])
        self.addLink(plc2, switch)

        plc3 = self.addHost(
            'plc3',
            ip=IP_SWAT['plc3'] + NETMASK_SWAT,
            mac=MAC_SWAT['plc3'])
        self.addLink(plc3, switch)

        attacker = self.addNode(
            'attacker',
            cls=AttackerNode,
            ip=IP_SWAT['attacker'] + NETMASK_SWAT,
            mac=MAC_SWAT['attacker'])
        self.addLink(attacker, switch)

        # NOTE: swat dumb nodes
        plc1 = self.addHost(
            'plc1',
            ip=IP_SWAT['plc1'] + NETMASK_SWAT,
            mac=MAC_SWAT['plc1'])
        self.addLink(plc1, switch)

        plc4 = self.addHost(
            'plc4',
            ip=IP_SWAT['plc4'] + NETMASK_SWAT,
            mac=MAC_SWAT['plc4'])
        self.addLink(plc4, switch)

        plc5 = self.addHost(
            'plc5',
            ip=IP_SWAT['plc5'] + NETMASK_SWAT,
            mac=MAC_SWAT['plc5'])
        self.addLink(plc5, switch)

        plc6 = self.addHost(
            'plc6',
            ip=IP_SWAT['plc6'] + NETMASK_SWAT,
            mac=MAC_SWAT['plc6'])
        self.addLink(plc6, switch)

        shmi = self.addHost(
            'shmi',
            ip=IP_SWAT['shmi'] + NETMASK_SWAT,
            mac=MAC_SWAT['shmi'])
        self.addLink(shmi, switch)


        # NOTE: wadi
        switch2 = self.addSwitch('s2')

        scada = self.addHost(
            'scada',
            ip=IP['scada'] + NETMASK,
            mac=MAC['scada'])
        self.addLink(scada, switch2)

        rtu2a = self.addHost(
            'rtu2a',
            ip=IP['rtu2a'] + NETMASK,
            mac=MAC['rtu2a'])
        self.addLink(rtu2a, switch2)

        rtu2b = self.addHost(
            'rtu2b',
            ip=IP['rtu2b'] + NETMASK,
            mac=MAC['rtu2b'])
        self.addLink(rtu2b, switch2)

        attacker2 = self.addHost(
            'attacker2',
            cls=AttackerNode2,
            ip=IP['attacker2'] + NETMASK,
            mac=MAC['attacker2'])
        self.addLink(attacker2, switch2)

        # NOTE: wadi dumb nodes
        hmi = self.addHost(
            'hmi',
            ip=IP['hmi'] + NETMASK,
            mac=MAC['hmi'])
        self.addLink(hmi, switch2)

        hist = self.addHost(
            'hist',
            ip=IP['hist'] + NETMASK,
            mac=MAC['hist'])
        self.addLink(hist, switch2)

        ids = self.addHost(
            'ids',
            ip=IP['ids'] + NETMASK,
            mac=MAC['ids'])
        self.addLink(ids, switch2)


        switch3 = self.addSwitch('s3')
        self.addLink(switch3, attacker)
        self.addLink(switch3, attacker2)

        # NOTE: remove when done with testing
        # client = self.addNode(
        #     'client',
        #     cls=ClientNode,
        #     ip=IP_SWAT['client'] + NETMASK_SWAT,
        #     mac=MAC_SWAT['client'])
        # self.addLink(switch3, client)

        # client2 = self.addHost(
        #     'client2',
        #     cls=ClientNode2,
        #     ip=IP['client2'] + NETMASK,
        #     mac=MAC['client2'])
        # self.addLink(switch3, client2)

if __name__ == '__main__':
    """Test MixTopo."""

    setLogLevel( 'info' )

    topo = MixTopo()
    net = Mininet(topo=topo)
    net.start()

    CLI(net)

    net.stop()
