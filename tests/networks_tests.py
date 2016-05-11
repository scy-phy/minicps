"""
Networks_tests
"""

import networkx

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI

from minicps.utils import setup_func, teardown_func, with_named_setup
from minicps.networks import PLC, DumbSwitch
from minicps.networks import EthLink, TopoFromNxGraph


# TODO: currently not working
@with_named_setup(setup_func, teardown_func)
def test_TopoFromNxGraph():

    """Create a Networkx graph and build a mininet topology object."""

    # Build a test graph
    graph = networkx.Graph()
    graph.name = 'test'

    links = 0

    s1 = DumbSwitch('s1')
    graph.add_node('s1', attr_dict=s1.get_params())

    plc1 = PLC('plc1', '192.168.1.10')
    graph.add_node('plc1', attr_dict=plc1.get_params())

    link = EthLink(label=links, bandwidth=30, delay=0, loss=0)
    graph.add_edge('plc1', 's1', attr_dict=link.get_params())
    links += 1

    plc2 = PLC('plc2', '192.168.1.20')
    graph.add_node('plc2', attr_dict=plc2.get_params())

    link = EthLink(label=links, bandwidth=30, delay=0, loss=0)
    graph.add_edge('plc2', 's1', attr_dict=link.get_params())
    links += 1

    assert len(graph) == 3, "graph nodes error"
    assert links == 2, "link error"

    # Build a test graph
    topo = TopoFromNxGraph(graph)

    net = Mininet(topo=topo, link=TCLink, listenPort=6634)
    net.start()
    CLI(net)
    net.stop()
