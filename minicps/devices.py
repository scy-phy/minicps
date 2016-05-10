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


# SDN
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
