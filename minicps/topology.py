"""
Recreate the SWaT network with the highest level of precision.

DMZ AP, L3, L2 L1  wireless star networks and L0 wireless DLR
cannot be simulated because miniet lacks wireless (IEEE 802.11)
simulation support.
"""

from mininet.net import Mininet
from mininet.topo import Topo
# from minicps import constants as c


class DLR(Topo):

    """Device Level Ring Topology."""

    def __init__(self):
        """TODO: to be defined1. """
        Topo.__init__(self)

        pass


class EthStar(Topo):

    """Docstring for EthStar. """

    def __init__(self):
        """TODO: to be defined1. """
        Topo.__init__(self)

        pass


class L3EthStar(Topo):

    """
    Connects Historian, Workstation and process PLCs
    using a 5-port ethernet switch.
    An industrial firewall service router filter the traffic.
    """

    def __init__(self):
        """TODO: to be defined1. """
        Topo.__init__(self)


class L2EthStar(Topo):

    """
    Connects HMI and process PLCs
    using a 5-ports ethernet switches and
    16-ports ethernet switches.
    """

    def __init__(self):
        """TODO: to be defined1. """
        Topo.__init__(self)


class L1EthStar(Topo):

    """
    Connects process PLCs
    using a 5-ports ethernet switches and
    16-ports ethernet switches.
    """

    def __init__(self):
        """TODO: to be defined1. """
        Topo.__init__(self)


class L0DLR(DLR):

    """
    One for each sub-process (6 in total)
    It connects redundant PLCs, sensors and actuators
    using a remote IO adaptor.
    """

    def __init__(self):
        """TODO: to be defined1. """
        Topo.__init__(self)


class Minicps(Mininet):

    """Docstring for Minicps. """

    def __init__(self):
        """TODO: to be defined1. """
        Mininet.__init__(self)

        pass
