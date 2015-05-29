"""
Topology tests

logger reference to topology logger.

"""

from nose.plugins.skip import Skip, SkipTest

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

from minicps import constants as c
from minicps.topology import EthStar, Minicps, DLR, L3EthStar, L3EthStarAttack
from minicps.constants import _mininet_functests, setup_func, teardown_func, teardown_func_clear, with_named_setup

from time import sleep

import logging
logger = logging.getLogger('minicps.topology')
setLogLevel(c.TEST_LOG_LEVEL)


@with_named_setup(setup_func, teardown_func)
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
    """ % (c.TEMP_DIR)

    plc1.cmd(cmd)
    sleep(4)  # sec
    plc1.cmd('kill %while')

    with open(c.TEMP_DIR+'/date.out', 'r') as f:
        for line in f.readlines():
            logger.debug(line.strip())  # remove leading and trailing whitespaces
    # file closed automatically by python context manager API

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_L3EthStarBuild():
    """Test L3EthStar build process with custom L3_LINKOPTS"""
    raise SkipTest

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    CLI(net)
    # _mininet_functests(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_L3EthStarEnip():
    """Test L3EthStar ENIP client/server communications
    plc1 is used as a cpppo simulated controller listening
    to from all interfaces at port 44818
    workstn is used as a cpppo client sending couples of
    write/read requests every second.
    """
    raise SkipTest

    # TODO: integrate everything into log folder
    open(c.TEMP_DIR+'/l3/cppposerver.err', 'w').close()
    open(c.TEMP_DIR+'/l3/cpppoclient.out', 'w').close()
    open(c.TEMP_DIR+'/l3/cpppoclient.err', 'w').close()

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    plc1, workstn = net.get('plc1', 'workstn')

    server_cmd = './scripts/l3/cpppo_plc1server.sh'
    plc1.cmd(server_cmd)

    client_cmd = './scripts/l3/cpppo_client4plc1.sh'
    out = workstn.cmd(client_cmd)
    logger.debug(out)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_L3EthStarArpMitm():
    """plc1 ARP poisoning MITM attack using ettercap,
    You can pass IP target to the dedicated script.
    """
    raise SkipTest

    open(c.TEMP_DIR+'/l3/plc1arppoisoning.out', 'w').close()

    topo = L3EthStar()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    plc1, plc2, plc3 = net.get('plc1', 'plc2', 'plc3')

    target_ip1 = plc2.IP()
    target_ip2 = plc3.IP()
    attacker_interface = 'plc1-eth0'

    plc1_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % ( target_ip1,
            target_ip2, attacker_interface)
    plc1.cmd(plc1_cmd)

    plc2_cmd = 'ping -c5 %s' % plc3.IP()
    plc2_out = plc2.cmd(plc2_cmd)
    logger.debug(plc2_out)

    plc1_out = plc1.cmd('tcpdump &')
    logger.debug(plc1_out)

    # CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_L3EthStarAttackArpEnip():
    """
    attacker ARP poison plc1 and hmi using ettercap. 
    passive and active ARP spoofing

    cpppo is used to simulate enip client/server
    
    remote controller (eg: pox) 
    can be used to mitigate ARP poisoning.

    """
    # raise SkipTest

    topo = L3EthStarAttack()

    # built-in mininet controller
    net = Mininet(topo=topo, link=TCLink)

    # net = Mininet(topo=topo, link=TCLink, controller=None)
    # net.addController( 'c0',
    #         controller=RemoteController,
    #         ip='127.0.0.1',
    #         port=c.OF_MISC['controller_port'] )

    # then you can create a custom controller class and
    # init automatically when invoking mininet
    # eg: controller = POXAntiArpPoison

    net.start()
    plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
    # assert(type(plc1.IP())==str)

    # PASSIVE remote ARP poisoning
    target_ip1 = plc1.IP()
    target_ip2 = hmi.IP()
    attacker_interface = 'attacker-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
            target_ip1,
            target_ip2, attacker_interface)
    attacker.cmd(attacker_cmd)

    # enip communication btw plc1 server and hmi client
    # TODO: work with multiple realistic tags
    CLI(net)
    taglist = 'pump=INT[10]'
    server_cmd = "./scripts/cpppo/server.sh %s %s %s %s" % (
            './temp/workshop/cppposerver.err',
            plc1.IP(),
            taglist,
            './temp/workshop/cppposerver.out')
    plc1.cmd(server_cmd)
    client_cmd = "./scripts/cpppo/client.sh %s %s %s %s" % (
            './temp/workshop/cpppoclient.err',
            plc1.IP(),
            'pump[0]=0',
            './temp/workshop/cpppoclient.out')
    hmi.cmd(client_cmd)

    # CLI(net)

    net.stop()
