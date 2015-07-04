"""
Recreate the SWaT network with the highest level of precision.

DMZ AP, L3, L2 L1  wireless star networks and L0 wireless DLR
cannot be simulated because miniet lacks wireless (IEEE 802.11)
simulation support.

Topology syntax follow the new simplified Mininet 2.2 API.
eg: build() insted of __init__() constructor.

Switch naming convention: s2 indicates SWaT L2 network, not to
be confused with link layer.
"""

from mininet.net import Mininet
from mininet.topo import Topo

from minicps import constants as c

from minicps.constants import _buildLogger
import logging
logger = _buildLogger(__name__, c.LOG_BYTES, c.LOG_ROTATIONS)

import networkx as nx


# https://networkx.github.io/documentation/latest/reference/readwrite.html
# TODO: add more TopoFrom that convert to NxGraph and reuse this class
#       rename topology into topologies

class TopoFromNxGraph(Topo):

    """
    Construct a topology from an Undirected Simple Graph
    Node (allows self loops but no parallel edges)
    
    Support: start, daisy chain, DLR
    """

    # TODO: add drawing capability
    def build(self, graph):
        """
        Process net_graph and build a mininet topo.
        """
        class_name = type(self).__name__
        logger.info('Inside %s' % class_name)

        # Crate all minicps nodes and save them into a dict
        hosts = {}
        for node in graph.nodes():


            if node.__dict__.has_key('_is_switch'):
                logger.debug('add switch: %s' % node.name)
                hosts[node.name] = self.addSwitch(node.name)
            else:
                logger.debug('add: %s' % node.name)
                hosts[node.name] = self.addHost(node.name,
                    ip=node.ip+node.netmask, mac=node.mac)
                # TODO: check '' ip, mac and netmask

        for edge in graph.edges(data=True):
            logger.debug('edge: %s' % str(edge))
            link_opts = edge[2]['object'].opts
            logger.debug('link_opts: %s' % link_opts)
            self.addLink(hosts[edge[0].name], hosts[edge[1].name], **link_opts)

        logger.info('Leaving %s' % class_name)
        

# class L3EthStar(Topo):

#     """
#     Connects Historian, Workstation and process PLCs
#     using a 5-port ethernet switch.
#     An industrial firewall service router filter the traffic.
#     """

#     def build(self, n=c.L3_NODES):
#         """
#         mininet doesn't like long host names
#         eg: workstion abbreviated to workstn
#         """

#         switch = self.addSwitch('s3')

#         # FIXME: don't know how to use CP
#         # equi_balance = 0.5 / float(n)
#         # print "DEBUG: equi_balance", equi_balance
#         # host = self.addHost('plc%s' % (h + 1), cpu=equi_balance)

#         class_name = type(self).__name__
#         logger.info('Inside %s' % class_name)

#         for h in range(n-2):
#             # compute the key reused to access IP and MAC dicts and to name hosts
#             key = 'plc%s' % (h + 1)
#             host = self.addHost(key, ip=c.L1_PLCS_IP[key]+c.L1_NETMASK, mac=c.PLCS_MAC[key])
#             self.addLink(host, switch, **c.L3_LINKOPTS)

#         histn = self.addHost('histn', ip=c.L3_PLANT_NETWORK['histn']+c.L3_NETMASK,
#                 mac=c.OTHER_MACS['histn'])
#         self.addLink(histn, switch, **c.L3_LINKOPTS)

#         workstn = self.addHost('workstn', ip=c.L3_PLANT_NETWORK['workstn']+c.L3_NETMASK,
#                 mac=c.OTHER_MACS['workstn'])
#         self.addLink(workstn, switch, **c.L3_LINKOPTS)

#         logger.info('Leaving %s' % class_name)


# class L3EthStarAttack(Topo):

#     """
#     Like L3EthStar but with an additional host used
#     as attacker
#     """

#     def build(self, n=c.L3_NODES):
#         """
#         attacker is in the same plc subnet 192.168.1.x
#         see constants module for attacker's IP
#         and MAC

#         link performance are ideal (No TCLink)
#         """

#         switch = self.addSwitch('s3')

#         class_name = type(self).__name__
#         logger.info('Inside %s' % class_name)

#         for h in range(n-2):
#             # compute the key reused to access IP and MAC dicts and to name hosts
#             key = 'plc%s' % (h + 1)
#             host = self.addHost(key, ip=c.L1_PLCS_IP[key]+c.L1_NETMASK, mac=c.PLCS_MAC[key])
#             self.addLink(host, switch)

#         attacker = self.addHost('attacker', ip=c.L1_PLCS_IP['attacker']+c.L1_NETMASK,
#                 mac=c.OTHER_MACS['attacker'])
#         self.addLink(attacker, switch)

#         # TODO: hmi will be in L2
#         hmi = self.addHost('hmi', ip=c.L2_HMI['hmi']+c.L1_NETMASK,
#                 mac=c.OTHER_MACS['hmi'])
#         self.addLink(hmi, switch)

#         histn = self.addHost('histn', ip=c.L3_PLANT_NETWORK['histn']+c.L3_NETMASK,
#                 mac=c.OTHER_MACS['histn'])
#         self.addLink(histn, switch)

#         workstn = self.addHost('workstn', ip=c.L3_PLANT_NETWORK['workstn']+c.L3_NETMASK,
#                 mac=c.OTHER_MACS['workstn'])
#         self.addLink(workstn, switch)

#         logger.info('Leaving %s' % class_name)


# class L2EthStar(Topo):

#     """
#     Connects HMI and process PLCs
#     using a 5-ports ethernet switches and
#     16-ports ethernet switches.
#     """

#     def build(self):
#         """TODO: to be defined1. """
#         switch = self.addSwitch('s2')
#         pass


# class L1EthStar(Topo):

#     """
#     Connects process PLCs
#     using a 5-ports ethernet switches and
#     16-ports ethernet switches.
#     """

#     def build(self):
#         """TODO: to be defined1. """

#         pass


# class L0DLR(DLR):

#     """
#     One for each sub-process (6 in total)
#     It connects redundant PLCs, sensors and actuators
#     using a remote IO adaptor.
#     """

#     def build(self):
#         """TODO: to be defined1. """

#         pass


# class Minicps(Mininet):

#     """Docstring for Minicps. """

#     def build(self):
#         """TODO: to be defined1. """

#         pass
