"""
Recreate the SWaT network with the highest level of precision.

DMZ AP, L3, L2 L1  wireless star networks and L0 wireless DLR
cannot be simulated because miniet lacks wireless (IEEE 802.11)
simulation support.

Topology syntax follow the new simplified Mininet 2.2 API.
eg: build() insted of __init__() constructor.
"""

from mininet.net import Mininet
from mininet.topo import Topo
# from minicps import constants as c


class DLR(Topo):

    """Device Level Ring Topology."""

    def build(self):
        """TODO: to be defined1. """

        pass


class EthStar(Topo):

    """Docstring for EthStar. """

    def build(self, n=2):
        """Star topology with n host and a single switch."""
        switch = self.addSwitch('s1')

        for h in range(n):
            host = self.addHost('PLC%s' % (h + 1))
            self.addLink(host, switch)


class L3EthStar(Topo):

    """
    Connects Historian, Workstation and process PLCs
    using a 5-port ethernet switch.
    An industrial firewall service router filter the traffic.
    """

    def build(self):
        """TODO: to be defined1. """

        pass


class L2EthStar(Topo):

    """
    Connects HMI and process PLCs
    using a 5-ports ethernet switches and
    16-ports ethernet switches.
    """

    def build(self):
        """TODO: to be defined1. """

        pass


class L1EthStar(Topo):

    """
    Connects process PLCs
    using a 5-ports ethernet switches and
    16-ports ethernet switches.
    """

    def build(self):
        """TODO: to be defined1. """

        pass


class L0DLR(DLR):

    """
    One for each sub-process (6 in total)
    It connects redundant PLCs, sensors and actuators
    using a remote IO adaptor.
    """

    def build(self):
        """TODO: to be defined1. """

        pass


class Minicps(Mininet):

    """Docstring for Minicps. """

    def build(self):
        """TODO: to be defined1. """

        pass
