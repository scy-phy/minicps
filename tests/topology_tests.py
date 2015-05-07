"""
Topology tests

with_setup decorator calls setup before each test and teardown after
each tests. It is possible to use different fixtures for different
tests.

SkipTest can be used as a switch to intentionally skip a test. You
can see skipped test summary in the nosetest output.

use -s opt to prevent nosetest to capture stdout.
use -v opt to obtain a more verbose output.
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

from time import sleep

import os


def setup():
    # print 'SETUP!'
    setLogLevel(c.TEST_LOG_LEVEL)


def teardown():
    # print 'TEAR DOWN!'
    pass


def mininet_functests(net):
    """Common mininet functional tests can be called inside
    each unittest. The function will be ignored by nose
    during automatic test collection because its name is
    not part of nose convention.
    Remember to manually stop the network after this call.

    :net: Mininet object
    """

    print "DEBUG: Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "DEBUG: Testing network connectivity"
    net.pingAll()
    print "DEBUG: Testing TCP bandwidth btw PLC1 and PLC2"
    

@with_setup(setup, teardown)
def test_EthStar():
    """Show mininet testing capabilites on an eth star topologies"""
    raise SkipTest

    topo = EthStar(n=6)
    net = Mininet(topo)  # TODO: subclass Mininet with Minicps and replace it
    net.start()

    plc1, plc2 = net.get('plc1', 'plc2')  # get host obj reference by name
    # net.iperf((plc1, plc2))  # passed as a tuple
    # output = plc1.cmd('ifconfig')
    # print output

    # while ... do ... done bash syntax
    cmd = """
    while true
    do date
    sleep 1
    done > %s/date.out &
    """ % (c.LOG_DIR)

    plc1.cmd(cmd)
    sleep(4)  # sec
    plc1.cmd('kill %while')

    with open(c.LOG_DIR+'/date.out', 'r') as f:
        for line in f.readlines():
            print line.strip()  # remove leading and trailing whitespaces
    # file closed automatically by python context manager API

    assert_equals(1+1, 2)

    net.stop()


@with_setup(setup, teardown)
def test_L3EthStarBuild():
    """Test L3EthStar build process with custom L3_LINKOPTS"""
    raise SkipTest

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    CLI(net)

    net.stop()


@with_setup(setup, teardown)
def test_L3EthStarEnip():
    """Test L3EthStar ENIP client/server communications
    plc1 is used as a cpppo simulated controller listening
    to from all interfaces at port 44818
    workstn is used as a cpppo client sending couples of
    write/read requests every second.
    """
    # raise SkipTest

    # (re)create temp log filesystem each time overwrite all files
    # more on http://stackoverflow.com/questions/12654772/create-empty-file-using-python
    open(c.LOG_DIR+'/l3/cppposerver.out', 'w').close()
    open(c.LOG_DIR+'/l3/cppposerver.err', 'w').close()
    open(c.LOG_DIR+'/l3/cpppoclient.out', 'w').close()
    open(c.LOG_DIR+'/l3/cpppoclient.err', 'w').close()

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    plc1, workstn = net.get('plc1', 'workstn')

    server_cmd = './scripts/l3/cpppo_plc1server.sh'
    plc1.cmd(server_cmd)

    client_cmd = './scripts/l3/cpppo_client4plc1.sh'
    workstn.cmd(client_cmd)

    net.stop()
    os.system('sudo mn -c')


@with_setup(setup, teardown)
def test_DLR():
    """Test DLR ring"""
    raise SkipTest

    topo = DLR(n=2)
    net = Mininet(topo)
    net.start()

    net.stop()
