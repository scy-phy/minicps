"""
swat networks module

DMZ AP, L3, L2 L1  wireless star networks and L0 wireless DLR
cannot be simulated because miniet lacks wireless (IEEE 802.11)
simulation support.

Topology syntax follow the new simplified Mininet 2.2 API.
eg: build() insted of __init__() constructor.

Mininet does not like long hostname,
e.g., workstation is truncated to workstn
"""

from mininet.topo import Topo

from examples.swat.utils import L1_PLCS_IP, PLCS_MAC, L2_HMI
from examples.swat.utils import L3_PLANT_NETWORK, OTHER_MACS
from examples.swat.utils import L1_NETMASK, L3_LINKOPTS, L3_NETMASK

# TODO: try to use mininet CPU balancing
# equi_balance = 0.5 / float(n)
# print "DEBUG: equi_balance", equi_balance
# host = self.addHost('plc%s' % (h + 1), cpu=equi_balance)


class L3EthStar(Topo):

    """Build swat layer 3 network.

    It includes: Historian, HMI, Workstation 3 process PLCs
    and an optional attacker.
    """

    def build(
            self,
            link_opts=L3_LINKOPTS,
            add_attacker=False):
        """
        attacker is in the same plc subnet 192.168.1.x
        :add_attacker: defaults to False
        :add_attacker: defaults to False
        """

        switch = self.addSwitch('s3')

        for h in range(6):
            # key reused to access IP and MAC dicts and to name hosts
            key = 'plc%s' % (h + 1)
            host = self.addHost(
                key, ip=L1_PLCS_IP[key] + L1_NETMASK,
                mac=PLCS_MAC[key])
            self.addLink(host, switch, **link_opts)

        histn = self.addHost(
            'histn',
            ip=L3_PLANT_NETWORK['histn'] + L3_NETMASK,
            mac=OTHER_MACS['histn'])
        self.addLink(histn, switch, **link_opts)

        workstn = self.addHost(
            'workstn',
            ip=L3_PLANT_NETWORK['workstn'] + L3_NETMASK,
            mac=OTHER_MACS['workstn'])
        self.addLink(workstn, switch, **link_opts)

        hmi = self.addHost(
            'hmi',
            ip=L2_HMI['hmi'] + L1_NETMASK,
            mac=OTHER_MACS['hmi'])
        self.addLink(hmi, switch)

        if add_attacker:
            attacker = self.addHost(
                'attacker',
                ip=L1_PLCS_IP['attacker'] + L1_NETMASK,
                mac=OTHER_MACS['attacker'])
            self.addLink(attacker, switch)


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


class L0DLR(Topo):

    """
    One for each sub-process (6 in total)
    It connects redundant PLCs, sensors and actuators
    using a remote IO adaptor.
    """

    def build(self):
        """TODO: to be defined1. """
        pass
