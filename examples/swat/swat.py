"""
Build SWaT testbed with MiniCPS

graph_name functions are used to build networkx graphs representing the
topology you want to build.

mininet_name functions are used to setup mininet configs
eg: preload webservers, enip servers, attacks, ecc...

launcher interacts with MiniCPS topologies module and optionally plot and/or
save a graph representation in the examples/swat folder.

"""

# TODO: check the log files, merge with swat controller

import sys, os
sys.path.append(os.getcwd())

from minicps.devices import PLC, HMI, DumbSwitch, Histn, Attacker, Workstn
from minicps.links import EthLink
from minicps.topologies import TopoFromNxGraph
from minicps import constants as c

from constants import *  # those are SWaT specific constants

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

import networkx as nx
import matplotlib.pyplot as plt


def graph_test():
    """
    Two plcs, hmi and s3

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
    link = EthLink(bw=10, delay=0, loss=0)

    # connect vertices with edgeg
    graph.add_edge(plc1, s3, object=link)
    graph.add_edge(plc2, s3, object=link)
    graph.add_edge(hmi, s3, object=link)

    return graph


def graph_level1(attacker=False):
    """
    SWaT testbed L1 graph + L2 hmi + L3 histn and L3 workstn + optional
    attacker

    :attacker: add an additional Attacker device to the graph

    :returns: graph
    """

    graph = nx.Graph()
    # graph = nx.DiGraph()

    graph.name = 'swat_level1'
    
    # Init switches
    s3 = DumbSwitch('s3')

    # Init links
    link = EthLink(bw=30, delay=0, loss=0)

    # Create nodes and connect edges
    nodes = {}
    for i in range(1, 7):
        key = 'plc'+str(i)
        nodes[key] = PLC(key, L1_PLCS_IP[key], L1_NETMASK, PLCS_MAC[key])
        graph.add_edge(nodes[key], s3, object=link)

    nodes['hmi'] = HMI('hmi', L2_HMI['hmi'], L1_NETMASK, OTHER_MACS['hmi'])
    graph.add_edge(nodes['hmi'], s3, object=link)

    nodes['histn'] = Histn('histn', L3_PLANT_NETWORK['histn'], L1_NETMASK,
            OTHER_MACS['histn'])
    graph.add_edge(nodes['histn'], s3, object=link)

    nodes['workstn'] = Histn('workstn', L3_PLANT_NETWORK['workstn'], L1_NETMASK,
            OTHER_MACS['workstn'])
    graph.add_edge(nodes['workstn'], s3, object=link)

    if attacker:
        nodes['attacker'] = Attacker('attacker', L1_PLCS_IP['attacker'], L1_NETMASK,
        OTHER_MACS['attacker'])
        graph.add_edge(nodes['attacker'], s3, object=link)


    return graph


def mininet_std(net):
    """Launch the miniCPS SWaT simulation"""

    net.start()

    CLI(net)

    net.stop()


def mininet_workshop(net):
    """
    Settings used for the Think-in workshop

    :net: TODO

    """
    pass


def laucher(graph, mininet_config, draw_mpl=False):
    """
    Launch the miniCPS SWaT simulation
    
    :graph: networkx graph
    :mininet_config: fucntion pointer to the mininet configuration
    :draw_mpl: flag to draw and save the graph using matplotlib
    """

    # TODO: show only names and list attributes
    if draw_mpl:
        nx.draw_networkx(graph)
        plt.axis('off')
        # plt.show()
        plt.savefig("examples/swat/%s.pdf" % graph.name)

    # Build miniCPS topo
    topo = TopoFromNxGraph(graph)
    net = Mininet(topo=topo, link=TCLink, listenPort=6634)

    mininet_config(net)



if __name__ == '__main__':
    swat_graph = graph_level1(attacker=True)
    laucher(swat_graph, mininet_std, draw_mpl=True)
