"""
MiniCPS Software Defined Networking (SDN) module.

It contains OpenFlow data objects.

It contains platform-specific SDN controller e.g., pox.
POX prefixed ClassNames indicate controller coded into script/pox dir
and symlinked to ~/pox/pox/forwarding dir.
Minicps assumes that pox is cloned into your $HOME dir.
For more information visit:
https://openflow.stanford.edu/display/ONL/POX+Wiki

By default Mininet runs Open vSwitch in OpenFlow mode,
which requires an OpenFlow controller.
Controller subclasses are started and stopped automatically by Mininet.
RemoteController must be started and stopped by the user.
Controller that enables learning switches doesn't work natively on
topologies that contains loops and multiple paths (eg: fat trees)
but they work fine with spanning tree topologies.

"""

from mininet.node import Controller

# pox {{{1
POX_PATH = '~/'

POX = {
    './pox.py openflow.of_01 --port=6633 --address=127.0.0.1' +
    'log.level --DEBUG swat_controller',
}


def set_pox_opts(
        components, info_level, logfile_opts,
        log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):

    """Generate a string with custom pox options.

    :components: dot notation paths (eg: forwarding.l2_learning web.webcore --port=8888)
    :info_level: DEBUG, INFO, etc.
    :logfile_opts: path and other options (eg: file.log,w to overwrite each time)
    :returns: options string for ./pox.py command

    """
    info_level = info_level.upper()
    pox_opts = '%s log.level --%s log --file=%s --format="%s" &' % (
        components,
        info_level, logfile_opts, log_format)
    # print 'DEBUG:', opts

    return pox_opts


class POXL2Pairs(Controller):

    """MAC-learning controller."""

    def start(self):
        self.pox = '%s/pox/pox.py' % (POX_PATH)
        pox_opts = set_pox_opts(
            'forwarding.l2_pairs', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        self.cmd('kill %' + self.pox)


class POXL2Learning(Controller):

    """Build a controller able to update switches
    flow tables according to flow-based criteria
    (not only MAC-based flow matching)."""

    def start(self):
        self.pox = '%s/pox/pox.py' % (POX_PATH)
        pox_opts = set_pox_opts(
            'forwarding.l2_learning', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        self.cmd('kill %' + self.pox)


class POXProva(Controller):

    """Use it to test components using POX_PATH."""

    def start(self):
        POX_PATH = 'hub'  # pox/ext/ dir

        self.pox = '%s/pox/pox.py' % (POX_PATH)
        pox_opts = set_pox_opts(
            POX_PATH, 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)
        # self.cmd(
        #     self.pox,
        #     'forwarding.prova log.level --DEBUG log --file=./logs/pox.log &')

    def stop(self):
        self.cmd('kill %' + self.pox)


class POXSwat(Controller):

    """Build a controller based on temp/antiarppoison.py"""

    def start(self):
        self.pox = '%s/pox/pox.py' % (POX_PATH)
        pox_opts = set_pox_opts(
            'swat_controller', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        self.cmd('kill %' + self.pox)


class POXAntiArpPoison(Controller):

    """Build a controller based on temp/antiarppoison.py"""

    def start(self):
        self.pox = '%s/pox/pox.py' % (POX_PATH)
        pox_opts = set_pox_opts(
            'antiarppoison', 'DEBUG', 'logs/' +
            type(self).__name__ + '.log,w')
        self.cmd(self.pox, pox_opts)

    def stop(self):
        self.cmd('kill %' + self.pox)


# Openflow {{{1
OF_MISC = {
    'user_switch': 'user',
    'kernel_switch': 'ovsk',
    'controller_port': 6633,
    'switch_debug_port': 6634,
    'flood_port': 65531,
}

OF10_MSG_TYPES = {
    0: 'OFPT_HELLO',  # Symmetric
    1: 'OFPT_ERROR',  # Symmetric
    2: 'OFPT_ECHO_REQUEST',  # Symmetric
    3: 'OFPT_ECHO_REPLY',  # Symmetric
    4: 'OFPT_VENDOR',  # Symmetric

    5: 'OFPT_FEATURES_REQUEST',  # Controller -> Switch
    6: 'OFPT_FEATURES_REPLY',  # Switch -> Controller
    7: 'OFPT_GET_CONFIG_REQUEST',  # Controller -> Switch
    8: 'OFPT_GET_CONFIG_REPLY',  # Switch -> Controller
    9: 'OFPT_SET_CONFIG',  # Controller -> Switch

    10: 'OFPT_PACKET_IN',  # Async, Switch -> Controller
    11: 'OFPT_FLOW_REMOVED',  # Async, Switch -> Controller
    12: 'OFPT_PORT_STATUS',  # Async,  Switch -> Controller

    13: 'OFPT_PACKET_OUT',  # Controller -> Switch
    14: 'OFPT_FLOW_MOD',  # Controller -> Switch
    15: 'OFPT_PORT_MOD',  # Controller -> Switch

    16: 'OFPT_STATS_REQUEST',  # Controller -> Switch
    17: 'OFPT_STATS_REPLY',  # Switch -> Controller

    18: 'OFPT_BARRIER_REQUEST',  # Controller -> Switch
    19: 'OFPT_BARRIER_REPLY',  # Switch -> Controller

    20: 'OFPT_QUEUE_GET_CONFIG_REQUEST',  # Controller -> Switch
    21: 'OFPT_QUEUE_GET_CONFIG_REPLY',  # Switch -> Controller
}
