"""
Mininet

Vertex is the base device class, its subclasses represent a particular network
device.

By default Mininet runs Open vSwitch in OpenFlow mode,
which requires an OpenFlow controller.


Pox

Minicps assumes that pox is cloned into your $HOME dir,
for more information visit:
https://openflow.stanford.edu/display/ONL/POX+Wiki

Controller subclasses are started and stopped automatically by Mininet.
RemoteController must be started and stopped by the user.

Controller that enables learning switches doesn't work natively on
topologies that contains loops and multiple paths (eg: fat trees)
but they work fine with spanning tree topologies.
"""


# from mininet.net import Mininet
from mininet.node import Controller  # , Host, Node
# from mininet.topo import SingleSwitchTopo

from minicps import constants as c

from minicps.constants import _buildLogger, _pox_opts

# import os
# import sys
# import logging
logger = _buildLogger(__name__, c.LOG_BYTES, c.LOG_ROTATIONS)


# netwrokx: use Edge and Vertex to avoid conflicts with mininet terminology
class Vertex(object):

    """
    Base networkx -> mininet host object

    """

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


# Mininet
class POXL2Pairs(Controller):

    """Build a controller able to update switches
    flow tables according to MAC learning."""

    def start(self):
        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts(
            'forwarding.l2_pairs', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class POXL2Learning(Controller):

    """Build a controller able to update switches
    flow tables according to flow-based criteria
    (not only MAC-based flow matching)."""

    def start(self):
        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts(
            'forwarding.l2_learning', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class POXProva(Controller):

    """Use it to test components using POX_PATH."""

    def start(self):
        POX_PATH = 'hub'  # pox/ext/ dir

        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts(
            POX_PATH, 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)
        # self.cmd(
        #     self.pox,
        #     'forwarding.prova log.level --DEBUG log --file=./logs/pox.log &')

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class POXSwat(Controller):

    """Build a controller based on temp/antiarppoison.py"""

    def start(self):
        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts(
            'swat_controller', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class POXAntiArpPoison(Controller):

    """Build a controller based on temp/antiarppoison.py"""

    def start(self):
        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts(
            'antiarppoison', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)
