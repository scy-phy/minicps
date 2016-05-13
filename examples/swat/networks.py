"""
swat networks module

Mininet does not like long hostname,
e.g., workstation is truncated to workstn
"""

from mininet.topo import Topo

from examples.swat.utils import L1_PLCS_IP, PLCS_MAC
from examples.swat.utils import L3_PLANT_NETWORK, OTHER_MACS
from examples.swat.utils import L1_NETMASK, L3_LINKOPTS, L3_NETMASK

# TODO: try to use mininet CPU balancing
# equi_balance = 0.5 / float(n)
# print "DEBUG: equi_balance", equi_balance
# host = self.addHost('plc%s' % (h + 1), cpu=equi_balance)


class L3EthStar(Topo):

    """Build swat layer 3 network.

    Connects Historian, Workstation and process PLCs
    using a 5-port ethernet switch.
    An industrial firewall service router filter the traffic.
    """

    def build(self, n=8):

        switch = self.addSwitch('s3')

        for h in range(n - 2):
            # key reused to access IP and MAC dicts and to name hosts
            key = 'plc%s' % (h + 1)
            host = self.addHost(
                key, ip=L1_PLCS_IP[key] + L1_NETMASK,
                mac=PLCS_MAC[key])
            self.addLink(host, switch, **L3_LINKOPTS)

        histn = self.addHost(
            'histn',
            ip=L3_PLANT_NETWORK['histn'] + L3_NETMASK,
            mac=OTHER_MACS['histn'])
        self.addLink(histn, switch, **L3_LINKOPTS)

        workstn = self.addHost(
            'workstn',
            ip=L3_PLANT_NETWORK['workstn'] + L3_NETMASK,
            mac=OTHER_MACS['workstn'])
        self.addLink(workstn, switch, **L3_LINKOPTS)


class L3EthStarAttack(Topo):

    """
    Like L3EthStar but with an additional host used
    as attacker
    """

    def build(self, n=8):
        """
        attacker is in the same plc subnet 192.168.1.x
        see constants module for attacker's IP
        and MAC

        link performance are ideal (No TCLink)
        """

        switch = self.addSwitch('s3')

        class_name = type(self).__name__
        logger.info('Inside %s' % class_name)

        for h in range(n-2):
            # compute the key reused to access IP and MAC dicts and to name hosts
            key = 'plc%s' % (h + 1)
            host = self.addHost(key, ip=c.L1_PLCS_IP[key]+c.L1_NETMASK, mac=c.PLCS_MAC[key])
            self.addLink(host, switch)

        attacker = self.addHost('attacker', ip=c.L1_PLCS_IP['attacker']+c.L1_NETMASK,
                mac=c.OTHER_MACS['attacker'])
        self.addLink(attacker, switch)

        # TODO: hmi will be in L2
        hmi = self.addHost('hmi', ip=c.L2_HMI['hmi']+c.L1_NETMASK,
                mac=c.OTHER_MACS['hmi'])
        self.addLink(hmi, switch)

        histn = self.addHost('histn', ip=c.L3_PLANT_NETWORK['histn']+c.L3_NETMASK,
                mac=c.OTHER_MACS['histn'])
        self.addLink(histn, switch)

        workstn = self.addHost('workstn', ip=c.L3_PLANT_NETWORK['workstn']+c.L3_NETMASK,
                mac=c.OTHER_MACS['workstn'])
        self.addLink(workstn, switch)

        logger.info('Leaving %s' % class_name)


class L2EthStar(Topo):

    """
    Connects HMI and process PLCs
    using a 5-ports ethernet switches and
    16-ports ethernet switches.
    """

    def build(self):
        """TODO: to be defined1. """
        switch = self.addSwitch('s2')
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
