"""
Build SWaT testbed with MiniCPS
"""

# TODO: check the log files, merge with swat controller

import sys, os
sys.path.append(os.getcwd())

from minicps.devices import PLC, HMI, DumbSwitch
from minicps.links import EthLink
from minicps.topology import TopoFromNxGraph

from constants import *  # those are SWaT specific constants

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink

import networkx as nx


def std_graph():
    """
    SWaT testbed std graph

    :returns: graph
    """

    # Simple Digraph graph: no self-loops and parallel edges
    # use directed to save time when iterating
    graph = nx.Graph()
    # graph = nx.DiGraph()
    
    # create graph vertices
    plc1 = PLC('plc1', L1_PLCS_IP['plc1'], L1_NETMASK, PLCS_MAC['plc1'])
    plc2 = PLC('plc2', L1_PLCS_IP['plc2'], L1_NETMASK, PLCS_MAC['plc2'])
    hmi = HMI('hmi', L2_HMI['hmi'], L1_NETMASK, OTHER_MACS['hmi'])
    s3 = DumbSwitch('s3')

    # create graph vertices: potentially each one with dedicated parameters
    link = EthLink(10, 0, 0)

    # connect vertices with edgeg
    graph.add_edge(plc1, s3, object=link)
    graph.add_edge(plc2, s3, object=link)
    graph.add_edge(hmi, s3, object=link)

    return graph

def laucher():
    """Launch the miniCPS SWaT simulation"""


    # Build miniCPS topo
    swat_graph = std_graph()
    topo = TopoFromNxGraph(swat_graph)
    net = Mininet(topo=topo, link=TCLink, listenPort=6634)
    net.start()

    CLI(net)

    net.stop()


if __name__ == '__main__':
    laucher()
