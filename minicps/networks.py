"""
MiniCPS networks module.

It contains data object used my Mininet to build the topology.

It contains data object used to specify topologies as graph files.
The module is using Vertex and Edge base class names to avoid conflicts with
networkx module. The logic of each device will be specified by the client
"""

from mininet.topo import Topo


# graph abstraction classes
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
        self.is_not_minient_switch = True

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


# TODO: add more TopoFrom that convert to NxGraph and reuse this class
#       rename topology into topologies
# https://networkx.github.io/documentation/latest/reference/readwrite.html
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

        :graph: network information embedded as parameters
        """
        # class_name = type(self).__name__

        # Crate all minicps nodes and save them into a dict
        hosts = {}
        for node in graph.nodes(data=True):
            name = node[0]
            params = node[1]
            # logger.debug(params)
            # if params.has_key('is_not_mininet_switch'):
            if 'is_not_mininet_switch' in params:
                # logger.debug('add switch: %s' % name)
                hosts[name] = self.addSwitch(name)
            else:
                # logger.debug('add: %s' % name)
                hosts[name] = self.addHost(
                    name,
                    ip=params['ip'] + params['netmask'],
                    mac=params['mac'])
                # TODO: check '' ip, mac and netmask

        for edge in graph.edges(data=True):
            # logger.debug('edge: %s' % str(edge))
            link_opts = edge[2]
            # logger.debug('link_opts: %s' % link_opts)
            self.addLink(hosts[edge[0]], hosts[edge[1]], **link_opts)
