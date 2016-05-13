"""
MiniCPS networks module.

It contains data object used my Mininet to build the topology.

It contains data object used to specify topologies as graph files.
The module is using Vertex and Edge base class names to avoid conflicts with
networkx module. The logic of each device will be specified by the client

Incoming graphs have to satisfy some constraints to build correctly:
Attributes must be passed as dict using add_edge(name, params=dict) and
add_node(name, params=dict)
"""

import networkx as nx

from mininet.topo import Topo


# graph abstraction classes {{{1
class Vertex(object):

    """Base class used to model devices as vertices in a graph."""

    def __init__(self, label, ip='', netmask='', mac='', cpu_alloc=0.0):
        """

        :label: node unique id used also as mininet hostname
        :ip: IPv4 address
        :mac: Ethernet address
        :netmask: CIDR notation e.g., /24
        :cpu_alloc: floating point percentage of CPU allocation

        """
        self.label = label
        self.ip = ip
        self.netmask = netmask
        self.mac = mac
        self.cpu_alloc = cpu_alloc  # TODO: take a look first in mininet

    def get_params(self):
        """Wrapper around __dict__"""

        return self.__dict__


class PLC(Vertex):

    """Programmable Logic Controller (PLC)."""

    pass


class Attacker(Vertex):

    """Attacker."""

    def ettercap_mitm_pap(self, target_ip1, target_ip2, attacker_interface):
        """
        Set parameters for a ARP poisoning Man-in-the-middle attack.

        :target_ip1: IPv4 address of the first target
        :target_ip2: IPv4 address of the second target
        :attacker_interface: attacker's network interface

        """

        pass


class DumbSwitch(Vertex):

    """Dumb switch alternative to mininet's switch."""

    def __init__(self, label, ip='', netmask='', mac='', cpu_alloc=0.0):
        Vertex.__init__(self, label, ip='', netmask='', mac='', cpu_alloc=0.0)

        # used to discriminate btw Mininet and MiniCPS switches
        self.is_not_mininet_switch = True

    def get_params(self):
        """Wrapper around __dict__"""

        return self.__dict__


class HMI(Vertex):

    """Human Machine Interface (HMI)."""

    pass


class Workstn(Vertex):

    """Workstation."""

    pass


class Histn(Vertex):

    """Historian,"""

    pass


class DumbRouter(Vertex):

    """Dumb router."""

    pass


class Firewall(Vertex):

    """Firewall."""

    pass


class SCADA(Vertex):

    """Docstring for SCADA. """

    pass


class Historian(Vertex):

    """Historian server."""

    pass


class AccessPoint(Vertex):

    """Access Point (AP)."""

    pass


class Edge(object):

    """Base class to model links as edges in a graph."""

    # TODO: finish the doc
    def __init__(
            self, label, bandwidth, delay,
            loss=0, max_queue_size=1000, use_htb=True):
        """
        :label: edge unique label
        :bandwidth: TODO
        :delay: TODO
        :loss: TODO
        :max_queue_size: TODO
        :use_htb: TODO
        """
        self.label = label
        self.bandwidth = bandwidth
        self.delay = delay
        self.loss = loss
        self.max_queue_size = max_queue_size
        self.use_htb = use_htb

    def get_params(self):
        """Wrapper around __dict__"""

        return self.__dict__


class EthLink(Edge):

    """Ethernet link."""

    pass


class WiFiLink(Edge):

    """WiFi 802.11 link."""

    pass


# topology from graphs {{{1
# TODO: add more TopoFrom that convert to NxGraph and reuse this class
#       rename topology into topologies
# https://networkx.github.io/documentation/latest/reference/readwrite.html
def build_nx_graph():

    """Create a networkx graph.

    The graph contains two PLCs connected to a switch
    """

    graph = nx.Graph(name='test')

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

    return graph


class MininetTopoFromNxGraph(Topo):

    """Construct a mininet topology from a nx graph."""

    def build(self, graph):
        """Process net_graph and build a mininet topo.

        :graph: network information embedded as parameters
        """

        hosts = {}
        for node in graph.nodes(data=True):
            name = node[0]
            params = node[1]

            if 'is_not_mininet_switch' in params:
                hosts[name] = self.addSwitch(name)
            else:
                hosts[name] = self.addHost(
                    name,
                    ip=params['ip'] + params['netmask'],
                    mac=params['mac'])
                # TODO: check '' ip, mac and netmask

        for edge in graph.edges(data=True):
            link_opts = edge[2]
            self.addLink(hosts[edge[0]], hosts[edge[1]], **link_opts)
