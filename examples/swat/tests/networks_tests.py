"""
swat networks tests
"""

from nose.tools import ok_
from nose.plugins.skip import SkipTest
# from nose.plugins.skip import Skip, SkipTest

from minicps.sdn import OF_MISC
from minicps.utils import TEMP_DIR

from examples.swat.utils import L1_PLCS_IP, L3_NODES, PLCS_MAC
from examples.swat.utils import L3_PLANT_NETWORK, OTHER_MACS
from examples.swat.networks import L3EthStar

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import RemoteController


@SkipTest
def test_L3EthStar():

    topo = L3EthStar(add_attacker=True)
    net = Mininet(
        topo=topo,
        link=TCLink,
        listenPort=OF_MISC['switch_debug_port'])

    net.start()

    net.pingAll()

    n = L3_NODES
    for h in range(n - 2):
        key = 'plc%s' % (h + 1)
        plc = net.get(key)  # get host obj reference by name
        ok_(plc.IP(), L1_PLCS_IP[key])
        ok_(plc.MAC(), PLCS_MAC[key])

    histn = net.get('histn')
    ok_(histn.IP(), L3_PLANT_NETWORK['histn'])
    ok_(histn.MAC(), OTHER_MACS['histn'])

    workstn = net.get('workstn')
    ok_(workstn.IP(), L3_PLANT_NETWORK['workstn'])
    ok_(workstn.MAC(), OTHER_MACS['workstn'])

    # alternative way to obtain IP and MAC
    # params = workstn.params

    net.stop()


# TODO: check
# plc1 is used as a cpppo server listening to port 44818.
# workstn is used as a cpppo client sending couples of
# write/read requests every second.
@SkipTest
def test_L3EthStarEnip():

    open(TEMP_DIR + '/cpppo-server.err', 'w').close()
    open(TEMP_DIR + '/cpppo-client.out', 'w').close()
    open(TEMP_DIR + '/cpppo-client.err', 'w').close()

    topo = L3EthStar()

    net = Mininet(
        topo=topo, link=TCLink,
        listenPort=OF_MISC['switch_debug_port'])
    net.start()

    plc1, workstn = net.get('plc1', 'workstn')

    cpppo_server_cmd = './scripts/cpppo/plc1server.sh'
    plc1.cmd(cpppo_server_cmd)

    cpppo_client_cmd = './scripts/cpppo/client4plc1.sh'
    workstn.cmd(cpppo_client_cmd)

    net.stop()


# TODO: check
# plc1 ARP poisoning MITM attack using ettercap,
# You can pass IP target to the dedicated script.
@SkipTest
def test_L3EthStarArpMitm():

    open(TEMP_DIR + '/l3/plc1arppoisoning.out', 'w').close()

    topo = L3EthStar()
    net = Mininet(
        topo=topo, link=TCLink,
        listenPort=OF_MISC['switch_debug_port'])
    net.start()

    plc1, plc2, plc3 = net.get('plc1', 'plc2', 'plc3')

    target_ip1 = plc2.IP()
    target_ip2 = plc3.IP()
    attacker_interface = 'plc1-eth0'

    plc1_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
        target_ip1,
        target_ip2, attacker_interface)
    plc1.cmd(plc1_cmd)

    plc2_cmd = 'ping -c5 %s' % plc3.IP()
    plc2.cmd(plc2_cmd)

    plc1.cmd('tcpdump &')

    # CLI(net)

    net.stop()


# TODO: check
# It uses remote controller
# attacker ARP poison plc1 and hmi using ettercap.
# passive and active ARP spoofing
@SkipTest
def test_L3EthStarAttackArpEnip():

    topo = L3EthStar(add_attacker=True)

    # built-in mininet controller
    # net = Mininet(
    #     topo=topo, link=TCLink,
    #     listenPort=OF_MISC['switch_debug_port'])
    # logger.info("started mininet default controller")

    net = Mininet(
        topo=topo, link=TCLink,
        controller=None,
        listenPort=OF_MISC['switch_debug_port'])

    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=OF_MISC['controller_port'])

    # then you can create a custom controller class and
    # init automatically when invoking mininet
    # eg: controller = POXAntiArpPoison

    net.start()
    plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
    # assert(type(plc1.IP())==str)

    CLI(net)

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

    CLI(net)

    net.stop()


# TODO: check
@SkipTest
def test_L3EthStarAttackDoubleAp():

    topo = L3EthStar(add_attacker=True)

    # net = Mininet(
    #     topo=topo, link=TCLink,
    #     listenPort=OF_MISC['switch_debug_port'])
    # logger.info("started mininet default controller")

    # mininet remote controller
    net = Mininet(
        topo=topo, link=TCLink,
        controller=None,
        listenPort=OF_MISC['switch_debug_port'])
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=OF_MISC['controller_port'])

    net.start()
    plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
    plc2, plc3, plc4 = net.get('plc2', 'plc3', 'plc4')

    CLI(net)

    # PASSIVE remote ARP poisoning
    target_ip1 = plc1.IP()
    target_ip2 = hmi.IP()
    attacker_interface = 'attacker-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
        target_ip1,
        target_ip2, attacker_interface)
    attacker.cmd(attacker_cmd)

    target_ip1 = plc3.IP()
    target_ip2 = plc4.IP()
    attacker_interface = 'plc2-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
        target_ip1,
        target_ip2, attacker_interface)
    plc2.cmd(attacker_cmd)

    CLI(net)

    # taglist = 'pump=INT[10]'
    # server_cmd = "./scripts/cpppo/server.sh %s %s %s %s" % (
    #         './temp/workshop/cppposerver.err',
    #         plc1.IP(),
    #         taglist,
    #         './temp/workshop/cppposerver.out')
    # plc1.cmd(server_cmd)
    # client_cmd = "./scripts/cpppo/client.sh %s %s %s %s" % (
    #         './temp/workshop/cpppoclient.err',
    #         plc1.IP(),
    #         'pump[0]=0',
    #         './temp/workshop/cpppoclient.out')
    # hmi.cmd(client_cmd)

    # logger.info("ENIP traffic from hmi to plc1 generated")
    # CLI(net)

    net.stop()


# TODO: check
@SkipTest
def test_Workshop():

    topo = L3EthStar(add_attacker=True)

    net = Mininet(
        topo=topo, link=TCLink,
        controller=None,
        listenPort=OF_MISC['switch_debug_port'])
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=OF_MISC['controller_port'])

    net.start()
    plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
    plc2, plc3, plc4 = net.get('plc2', 'plc3', 'plc4')

    CLI(net)

    # PASSIVE remote ARP poisoning
    target_ip1 = plc1.IP()
    target_ip2 = hmi.IP()
    attacker_interface = 'attacker-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
        target_ip1,
        target_ip2, attacker_interface)
    attacker.cmd(attacker_cmd)

    target_ip1 = plc3.IP()
    target_ip2 = plc4.IP()
    attacker_interface = 'plc2-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
        target_ip1,
        target_ip2, attacker_interface)
    plc2.cmd(attacker_cmd)

    CLI(net)

    # taglist = 'pump=INT[10]'
    # server_cmd = "./scripts/cpppo/server.sh %s %s %s %s" % (
    #         './temp/workshop/cppposerver.err',
    #         plc1.IP(),
    #         taglist,
    #         './temp/workshop/cppposerver.out')
    # plc1.cmd(server_cmd)
    # client_cmd = "./scripts/cpppo/client.sh %s %s %s %s" % (
    #         './temp/workshop/cpppoclient.err',
    #         plc1.IP(),
    #         'pump[0]=0',
    #         './temp/workshop/cpppoclient.out')
    # hmi.cmd(client_cmd)

    # logger.info("ENIP traffic from hmi to plc1 generated")
    # CLI(net)

    net.stop()
