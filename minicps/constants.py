"""
minicps constants.

TEST_LOG_LEVEL affetcs all the tests.
output, info and debug are in increasing order of verbosity.

There is a logger for each module/module_tests pair. Each pair
reference to the same object instance and save log into
minicps/log/modname.log. Log format and filters are hardcoded,
naming is implicit and you can set logs dimensions and number of
rotations through this module.

POX controller logs is stored into dedicated logs/POXControllerName.log file.
Each time the log file is overwritten, unlike minicps module logging facility.
"""

import logging
import logging.handlers
from mininet.util import dumpNodeConnections



# mirrors minicps constants
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


OF_MISC = {
    'user_switch': 'user',
    'kernel_switch': 'ovsk',
    'controller_port': 6633,
    'switch_debug_port': 6634,
    'flood_port': 65531,
}


## ENIP

ENIP_MISC = {
    'tcp_port': 44818,
    'udp_port': 2222,
}



## MININET

MININET_CMDS = {
    'clear': 'sudo mn -c',
    'linear-remote': 'sudo mn --topo=linear,4 --controller=remote',
}




def _mininet_functests(net):
    """Common mininet functional tests can be called inside
    each unittest. The function will be ignored by nose
    during automatic test collection because its name is
    not part of nose convention.
    Remember to manually stop the network after this call.

    :net: Mininet object
    """

    logging.info("Dumping host connections")
    dumpNodeConnections(net.hosts)
    logging.info("Testing network connectivity")
    net.pingAll()
    logging.info("Testing TCP bandwidth btw first and last host")
    net.iperf()

L0_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
L1_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
L2_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
L3_LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)

