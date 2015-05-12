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


def setup():
    # print 'SETUP!'
    setLogLevel(c.TEST_LOG_LEVEL)


def teardown():
    # print 'TEAR DOWN!'
    pass


@with_setup(setup, teardown)
def test_L3EthStarMapping():
    """Test L3 Ring MACs and IPs"""
    # raise SkipTest

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()


    n = c.L3_NODES
    for h in range(n-2):
        key = 'plc%s' % (h + 1)
        plc = net.get(key)  # get host obj reference by name
        assert_equals(plc.IP(), c.L1_PLCS_IP[key])
        assert_equals(plc.MAC(), c.PLCS_MAC[key])

    histn = net.get('histn')
    assert_equals(histn.IP(), c.L3_PLANT_NETWORK['histn'])
    assert_equals(histn.MAC(), c.OTHER_MACS['histn'])

    workstn = net.get('workstn')
    assert_equals(workstn.IP(), c.L3_PLANT_NETWORK['workstn'])
    assert_equals(workstn.MAC(), c.OTHER_MACS['workstn'])

    # alternative way to obtain IP and MAC
    # params = workstn.params
    # print 'DEBUG params:', params

    net.stop()
