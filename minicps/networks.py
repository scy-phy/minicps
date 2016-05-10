"""
MiniCPS networks module

It contains data object used my Mininet to build the topology.

It contains data object used to specify topologies as graph files.
The module is using Vertex and Edge base class names to avoid conflicts with
networkx module.
"""


# graph abstraction classes

class Vertex(object):

    """Base class used to model devices as vertices in a graph"""

    # TODO: finish doc
    def __init__(self, label, ip='', netmask='', mac='', cpu_alloc=0.0):
        """

        :label: node unique id used also as mininet hostname
        :ip: ipv4
        :mac: ethernet address
        :netmask: CIDR notation eg: /24
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

    """PLC"""

    # FIXME: delegate plc logic code to mininet?


class Attacker(Vertex):

    """Attacker"""

    def ettercap_mitm_pap(self, target_ip1, target_ip2, attacker_interface):
        """
        Mount a ettercap Man in the Middle passive ARP poisoning attack

        :target_ip1: ip address of the first target
        :target_ip2: ip address of the second target
        :attacker_interface: attacker interface

        """
        pass
        # FIXME: delegate attack to mininet code?


class DumbSwitch(Vertex):

    """
    is_switch bool is used to discriminate btw mininet switch requiring
    addSwitch method and normal hosts requiring addHost method.
    """

    def __init__(self, label, ip='', netmask='', mac='', cpu_alloc=0.0):
        Vertex.__init__(self, label, ip='', netmask='', mac='', cpu_alloc=0.0)

        self.is_switch = True  # used to discriminate btw node types

    def get_params(self):
        """Wrapper around __dict__"""

        return self.__dict__


class HMI(Vertex):

    """HMI"""

    # TODO: add logic


class Workstn(Vertex):

    """Workstn"""

    # TODO: add logic


class Histn(Vertex):

    """Histn"""

    # TODO: add logic


class DumbRouter(Vertex):

    """Docstring for DumbRouter. """

    # TODO: add logic


class Firewall(Vertex):

    """Docstring for Firewall. """

    # TODO: add logic


class SCADA(Vertex):

    """Docstring for SCADA. """

    # TODO: add logic


class Historian(Vertex):

    """Docstring for Historian. """

    # TODO: add logic


class AccessPoint(Vertex):

    """Docstring for AccessPoint. """

    # TODO: add logic


class Edge(object):

    """Base class used to model links as edges in a graph"""

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

    """EthLink"""
    pass


class WiFi(Edge):

    """EthLink"""
    pass
