"""
Use MiniCPS to simulate the first SWaT subprocess.

A state_db is used to represent the actual state of the system

graph_name functions are used to build networkx graphs representing the
topology you want to build.
"""

import time
import sys
import os
sys.path.append(os.getcwd())

from minicps.devices import PLC, HMI, DumbSwitch, Histn, Attacker, Workstn, POXSwat
from minicps.links import EthLink
from minicps.topologies import TopoFromNxGraph
from minicps import constants as c

from constants import logger, L1_PLCS_IP, L1_NETMASK, PLCS_MAC, L2_HMI
from constants import OTHER_MACS, L3_PLANT_NETWORK
from constants import LIT_101, init_swat

# used to separate different log sessions
logger.debug('----------'+time.asctime()+'----------')

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

import networkx as nx
import matplotlib.pyplot as plt


def nxgraph_sub1(attacker=False):
    """
    Build plc1-3, s1, hmi SWaT network graph

    :attacker: add an additional Attacker device to the graph

    :returns: networkx graph
    """

    graph = nx.Graph()

    graph.name = 'swat_level1'

    # Init switch
    s1 = DumbSwitch('s1')
    graph.add_node('s1', attr_dict=s1.get_params())

    # Create nodes and connect edges
    nodes = {}
    count = 0
    # plcs
    for i in range(1, 4):
        key = 'plc'+str(i)
        nodes[key] = PLC(key, L1_PLCS_IP[key], L1_NETMASK, PLCS_MAC[key])
        graph.add_node(key, attr_dict=nodes[key].get_params())
        link = EthLink(id=str(count), bw=30, delay=0, loss=0)
        graph.add_edge(key, 's1', attr_dict=link.get_params())
        count += 1
    # hmi
    nodes['hmi'] = HMI('hmi', L2_HMI['hmi'], L1_NETMASK, OTHER_MACS['hmi'])
    graph.add_node('hmi', attr_dict=nodes['hmi'].get_params())
    link = EthLink(id=str(count), bw=30, delay=0, loss=0)
    graph.add_edge('hmi', 's1', attr_dict=link.get_params())
    count += 1
    # optional attacker
    if attacker:
        nodes['attacker'] = Attacker('attacker', L1_PLCS_IP['attacker'], L1_NETMASK,
        OTHER_MACS['attacker'])
        graph.add_node('attacker', attr_dict=nodes['attacker'].get_params())
        link = EthLink(id=str(count), bw=30, delay=0, loss=0)
        graph.add_edge('attacker', 's1', attr_dict=link.get_params())

    return graph


def minicps_tutorial(net):
    """
    Settings used for tutorial

    :net: Mininet instance reference

    """

    init_swat()
    time.sleep(2)

    # Start mininet
    net.start()


    # Get references to nodes (each node is a Linux container)
    plc1, plc2, plc3, hmi, s1 = net.get('plc1', 'plc2', 'plc3', 'hmi', 's1')

    ## Comment out one of the two plc1x lines
    # plc1a_pid = plc1.cmd("python examples/swat/plc1a.py 2> examples/swat/err/plc1a.err &")
    plc1_pid = plc1.cmd("python examples/swat/plc1.py 2> examples/swat/err/plc1.err &")

    plc2_pid = plc2.cmd("python examples/swat/plc2.py 2> examples/swat/err/plc2.err &")
    plc3_pid = plc3.cmd("python examples/swat/plc3.py 2> examples/swat/err/plc3.err &")
    hmi_pid = hmi.cmd("python examples/swat/hmi.py 2> examples/swat/err/hmi.err &")

    # Start the physical process
    s1.cmd("python examples/swat/physical_process.py 2> examples/swat/err/pp.err &")

    ## Uncomment if you're running an xserver 
    ## or redirecting command to host xserver (ssh -Y ...)
    # Displays an image to monitor the physical process activity
    # That it will refresh every 200 ms
    os.system("python examples/swat/ImageContainer.py examples/swat/hmi/plc1.png 1200 2> examples/swat/err/ImageContainer.err &")

    CLI(net)

    net.stop()


if __name__ == '__main__':
    swat_graph = nxgraph_sub1(attacker=False)
    topo = TopoFromNxGraph(swat_graph)

    net = Mininet(topo=topo, link=TCLink, listenPort=6634)
    ## comment above and uncomment below to enable POXSwat SDN controller
    # controller = POXSwat
    # net = Mininet(topo=topo, controller=controller, link=TCLink, listenPort=6634)

    minicps_tutorial(net)
