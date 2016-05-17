"""
Build SWaT testbed with MiniCPS.

Graph_name functions are used to build networkx graphs representing the
topology you want to build.

Mininet_name functions are used to setup mininet configs
eg: preload webservers, enip servers, attacks, ecc...

Launcher interacts with MiniCPS topologies module and optionally plot and/or
have a graph representation in the examples/swat folder.
"""

# TODO: check the log files, merge with swat controller
# TODO: remove function importable from utils

import time
import sys
import os
# sys.path.append(os.getcwd())

from minicps.sdn import POXSwat
from minicps.networks import PLC, HMI, DumbSwitch, Histn, Attacker, Workstn, POXSwat
from minicps.networks import EthLink, TopoFromNxGraph
from minicps import constants as c

from constants import logger, init_swat
from utils import L1_PLCS_IP, L1_NETMASK, PLCS_MAC, L2_HMI
from utils import OTHER_MACS, L3_PLANT_NETWORK


from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink

import networkx as nx
import matplotlib.pyplot as plt


def nxgraph_level1(attacker=False):
    """
    SWaT testbed L1 graph + L2 hmi + L3 histn and L3 workstn + optional
    attacker

    :attacker: add an additional Attacker device to the graph

    :returns: networkx graph
    """

    graph = nx.Graph()
    # graph = nx.DiGraph()

    graph.name = 'swat_level1'

    # Init switches
    s3 = DumbSwitch('s3')
    graph.add_node('s3', attr_dict=s3.get_params())

    # Create nodes and connect edges
    nodes = {}
    count = 0
    for i in range(1, 7):
        key = 'plc' + str(i)
        nodes[key] = PLC(key, L1_PLCS_IP[key], L1_NETMASK, PLCS_MAC[key])
        graph.add_node(key, attr_dict=nodes[key].get_params())
        link = EthLink(label=str(count), bandwidth=30, delay=0, loss=0)
        graph.add_edge(key, 's3', attr_dict=link.get_params())
        count += 1
    assert len(graph) == 7, "plc nodes error"

    nodes['hmi'] = HMI('hmi', L2_HMI['hmi'], L1_NETMASK, OTHER_MACS['hmi'])
    graph.add_node('hmi', attr_dict=nodes['hmi'].get_params())
    link = EthLink(label=str(count), bandwidth=30, delay=0, loss=0)
    graph.add_edge('hmi', 's3', attr_dict=link.get_params())
    count += 1

    nodes['histn'] = Histn(
        'histn', L3_PLANT_NETWORK['histn'], L1_NETMASK,
        OTHER_MACS['histn'])
    graph.add_node('histn', attr_dict=nodes['histn'].get_params())
    link = EthLink(label=str(count), bandwidth=30, delay=0, loss=0)
    graph.add_edge('histn', 's3', attr_dict=link.get_params())
    count += 1

    nodes['workstn'] = Histn(
        'workstn', L3_PLANT_NETWORK['workstn'], L1_NETMASK,
        OTHER_MACS['workstn'])
    graph.add_node('workstn', attr_dict=nodes['workstn'].get_params())
    link = EthLink(label=str(count), bandwidth=30, delay=0, loss=0)
    graph.add_edge('workstn', 's3', attr_dict=link.get_params())
    count += 1

    if attacker:
        nodes['attacker'] = Attacker(
            'attacker', L1_PLCS_IP['attacker'], L1_NETMASK,
            OTHER_MACS['attacker'])
        graph.add_node('attacker', attr_dict=nodes['attacker'].get_params())
        link = EthLink(label=str(count), bandwidth=30, delay=0, loss=0)
        graph.add_edge('attacker', 's3', attr_dict=link.get_params())
        assert len(graph) == 11, "attacker node error"

    return graph


def mininet_std(net):
    """Launch the miniCPS SWaT simulation"""

    net.start()

    CLI(net)
    # launch device simulation scripts

    net.stop()


def minicps_tutorial(net):
    """
    Settings used for the Think-in workshop

    :net: Mininet instance reference

    """

    init_swat()

    net.start()

    # Start the physical process
    os.system(
        "python examples/swat/physical_process.py 2> examples/swat/pp.err &")

    plc1, plc2, plc3, hmi, s3 = net.get('plc1', 'plc2', 'plc3', 'hmi', 's3')

    # Monitoring on the switch
    # bro_cmd = "bro -C "
    # switch_ifaces =  s3.intfList()
    # for iface in switch_ifaces:
    #     bro_cmd += "-i %s " % iface.name
    # bro_cmd += "&"
    # s3_pid = s3.cmd(bro_cmd)

    # Init cpppo enip servers and run main loop
    plc1_pid = plc1.cmd(
        "python examples/swat/plc1.py 2> examples/swat/plc1.err &")
    plc2_pid = plc2.cmd(
        "python examples/swat/plc2.py 2> examples/swat/plc2.err &")
    plc3_pid = plc3.cmd(
        "python examples/swat/plc3.py 2> examples/swat/plc3.err &")
    hmi_pid = hmi.cmd(
        "python examples/swat/hmi.py 2> examples/swat/hmi.err &")

    CLI(net)

    net.stop()


def laucher(graph, mininet_config, draw_mpl=False, write_gexf=False):
    """
    Launch the miniCPS SWaT simulation

    :graph: networkx graph
    :mininet_config: function pointer to the mininet configuration
    :draw_mpl: flag to draw and save the graph using matplotlib
    """

    # TODO: use different color for plcs, switch and attacker
    if draw_mpl:
        nx.draw_networkx(graph)
        plt.axis('off')
        # plt.show()
        plt.savefig("examples/swat/%s.pdf" % graph.name)

    if write_gexf:
        g_gexf = nx.write_gexf(graph, "examples/swat/l1_gexf.xml")
        # g2 = nx.read_gexf("examples/swat/g_gexf.xml")

    # Build miniCPS topo
    topo = TopoFromNxGraph(graph)
    controller = POXSwat
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink,
        listenPort=6634)

    mininet_config(net)

if __name__ == '__main__':
    swat_graph = nxgraph_level1(attacker=True)
    # laucher(swat_graph, mininet_std, draw_mpl=False)

    # test nx -> gexf
    nx.write_gexf(swat_graph, "examples/swat/l1_gexf.xml", prettyprint=True)
    # test gexf -> nx
    rgraph = nx.read_gexf("examples/swat/l1_gexf.xml", relabel=False)
    laucher(rgraph, minicps_tutorial, draw_mpl=False)
