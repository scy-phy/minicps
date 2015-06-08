"""
Minicps assumes that pox is cloned into your $HOME dir,
for more information visit:
https://openflow.stanford.edu/display/ONL/POX+Wiki

To add a new pox controller code the control plane inside pox module
then add a new Controller subclass and link your script in start()
method with dot notation. 
eg: pox/forwarding/script.py -> forwarding.script &

By default Mininet runs Open vSwitch in OpenFlow mode,
which requires an OpenFlow controller.

Controller subclasses are started and stopped automatically by Mininet.
RemoteController must be started and stopped by the user.

Controller that enables learning switches doesn't work natively on
topologies that contains loops and multiple paths (eg: fat trees)
but they work fine with spanning tree topologies.
"""

from mininet.net import Mininet
from mininet.node import Controller, Host, Node
from mininet.topo import SingleSwitchTopo

from minicps import constants as c

import os

from minicps.constants import _buildLogger, _pox_opts
import logging
logger = _buildLogger(__name__, c.LOG_BYTES, c.LOG_ROTATIONS)


class POXL2Pairs(Controller):

    """Build a controller able to update switches
    flow tables according to MAC learning."""

    def start(self):
        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts('forwarding.l2_pairs', 'DEBUG', './logs/'+type(self).__name__+'.log,w')
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
        pox_opts = _pox_opts('forwarding.l2_learning', 'DEBUG', './logs/'+type(self).__name__+'.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class POXProva(Controller):

    """Use it to test components using POX_PATH."""

    def start(self):
        POX_PATH='hub'  # pox/ext/ dir

        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts(POX_PATH, 'DEBUG', './logs/'+type(self).__name__+'.log,w')
        self.cmd(self.pox, pox_opts)
        # self.cmd(self.pox, 'forwarding.prova log.level --DEBUG log --file=./logs/pox.log &')

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class POXSwatController(Controller):

    """Build a controller based on temp/antiarppoison.py"""

    def start(self):
        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts('swat_controller', 'DEBUG', './logs/'+type(self).__name__+'.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class POXAntiArpPoison(Controller):

    """Build a controller based on temp/antiarppoison.py"""

    def start(self):
        logger.info('Inside %s' % type(self).__name__)
        self.pox = '%s/pox/pox.py' % (c.POX_PATH)
        pox_opts = _pox_opts('antiarppoison', 'DEBUG', './logs/'+type(self).__name__+'.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        logger.info('Leaving %s' % type(self).__name__)
        self.cmd('kill %' + self.pox)


class PLC(Host):

    """Docstring for PLC. """

    def __init__(self):
        """TODO: to be defined1. """
        Host.__init__(self)

        pass


class DumbSwitch(Node):

    """Docstring for DumbSwitch. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class DumbRouter(Node):

    """Docstring for DumbRouter. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class Firewall(Node):

    """Docstring for Firewall. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class SCADA(Node):

    """Docstring for SCADA. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class HMI(Node):

    """Docstring for HMI. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


class Historian(Node):

    """Docstring for Historian. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass


# Wireless devices
class AccessPoint(Node):

    """Docstring for AccessPoint. """

    def __init__(self):
        """TODO: to be defined1. """
        Node.__init__(self)

        pass
