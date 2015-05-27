"""
Constants tests

Given implemented minicps/topologies test everything related to
constants module. 
eg: IPs, MACs, netmasks

"""

from nose.tools import *
from nose.plugins.skip import Skip, SkipTest

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI

from minicps import constants as c
from minicps.topology import EthStar, Minicps, DLR, L3EthStar
from minicps.constants import setup_func, teardown_func, teardown_func_clear, with_named_setup

import logging
logger = logging.getLogger('minicps.constants')
setLogLevel(c.TEST_LOG_LEVEL)


@with_named_setup(setup_func, teardown_func)
def test_L3EthStarMapping():
    """Test L3 Ring MACs and IPs"""
    # raise SkipTest

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    # TODO: add log info
    n = c.L3_NODES
    for h in range(n-2):
        key = 'plc%s' % (h + 1)
        plc = net.get(key)  # get host obj reference by name
        assert_equals(plc.IP(), c.L1_PLCS_IP[key])
        assert_equals(plc.MAC(), c.PLCS_MAC[key])

    histn = net.get('histn')
    assert_equals(histn.IP(), c.L3_PLANT_NETWORK['histn'],
            c.ASSERTION_ERRORS['ip_mismatch'])
    assert_equals(histn.MAC(), c.OTHER_MACS['histn'],
            c.ASSERTION_ERRORS['mac_mismatch'])

    workstn = net.get('workstn')
    assert_equals(workstn.IP(), c.L3_PLANT_NETWORK['workstn'],
            c.ASSERTION_ERRORS['ip_mismatch'])
    assert_equals(workstn.MAC(), c.OTHER_MACS['workstn'],
            c.ASSERTION_ERRORS['mac_mismatch'])

    # alternative way to obtain IP and MAC
    # params = workstn.params
    # print 'DEBUG params:', params

    net.stop()
