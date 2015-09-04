"""
Topologies tests

"""


from minicps.topologies import TopoFromNxGraph
from minicps.devices import PLC, HMI, DumbSwitch, Histn
from minicps.links import EthLink
from minicps.constants import _mininet_functests, setup_func, teardown_func, teardown_func_clear, with_named_setup
from minicps.constants import TEST_LOG_LEVEL

from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.cli import CLI

from nose.plugins.skip import Skip, SkipTest

import logging
logger = logging.getLogger('minicps.topologies')
setLogLevel(TEST_LOG_LEVEL)

import networkx as nx

@with_named_setup(setup_func, teardown_func)
def test_TopoFromNxGraph():
    """
    Create a Networkx graph and build a mininet topology object from it.

    """

    graph = nx.Graph()

    graph.name = 'test'

    # Init devices
    links = 0

    s1 = DumbSwitch('s1')
    graph.add_node('s1', attr_dict=s1.get_params())

    plc1 = PLC('plc1', '192.168.1.10')
    graph.add_node('plc1', attr_dict=plc1.get_params())

    link = EthLink(id=links, bw=30, delay=0, loss=0)
    graph.add_edge('plc1', 's1', attr_dict=link.get_params())
    links += 1

    plc2 = PLC('plc2', '192.168.1.20')
    graph.add_node('plc2', attr_dict=plc1.get_params())

    link = EthLink(id=links, bw=30, delay=0, loss=0)
    graph.add_edge('plc2', 's1', attr_dict=link.get_params())
    links += 1

    assert len(graph) == 3, "graph nodes error"
    assert links == 2, "link error"

    topo = TopoFromNxGraph(graph)

    net = Mininet(topo=topo, link=TCLink, listenPort=6634)
    net.start()
    CLI(net)
    net.stop()




# FIXME: move to swat-specific test folder
# @with_named_setup(setup_func, teardown_func)
# def test_L3EthStarBuild():
#     """Test L3EthStar build process with custom L3_LINKOPTS"""
#     raise SkipTest

#     topo = L3EthStar()
#     net = Mininet(topo=topo, link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
#     net.start()

#     CLI(net)
#     # _mininet_functests(net)

#     net.stop()


# @with_named_setup(setup_func, teardown_func)
# def test_L3EthStarEnip():
#     """Test L3EthStar ENIP client/server communications
#     plc1 is used as a cpppo simulated controller listening
#     to from all interfaces at port 44818
#     workstn is used as a cpppo client sending couples of
#     write/read requests every second.
#     """
#     raise SkipTest

#     # TODO: integrate everything into log folder
#     open(c.TEMP_DIR+'/l3/cppposerver.err', 'w').close()
#     open(c.TEMP_DIR+'/l3/cpppoclient.out', 'w').close()
#     open(c.TEMP_DIR+'/l3/cpppoclient.err', 'w').close()

#     topo = L3EthStar()
#     net = Mininet(topo=topo, link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
#     net.start()

#     plc1, workstn = net.get('plc1', 'workstn')

#     server_cmd = './scripts/l3/cpppo_plc1server.sh'
#     plc1.cmd(server_cmd)

#     client_cmd = './scripts/l3/cpppo_client4plc1.sh'
#     out = workstn.cmd(client_cmd)
#     logger.debug(out)

#     net.stop()


# @with_named_setup(setup_func, teardown_func)
# def test_L3EthStarArpMitm():
#     """plc1 ARP poisoning MITM attack using ettercap,
#     You can pass IP target to the dedicated script.
#     """
#     raise SkipTest

#     open(c.TEMP_DIR+'/l3/plc1arppoisoning.out', 'w').close()

#     topo = L3EthStar()
#     net = Mininet(topo=topo, link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
#     net.start()

#     plc1, plc2, plc3 = net.get('plc1', 'plc2', 'plc3')

#     target_ip1 = plc2.IP()
#     target_ip2 = plc3.IP()
#     attacker_interface = 'plc1-eth0'

#     plc1_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % ( target_ip1,
#             target_ip2, attacker_interface)
#     plc1.cmd(plc1_cmd)

#     plc2_cmd = 'ping -c5 %s' % plc3.IP()
#     plc2_out = plc2.cmd(plc2_cmd)
#     logger.debug(plc2_out)

#     plc1_out = plc1.cmd('tcpdump &')
#     logger.debug(plc1_out)

#     # CLI(net)

#     net.stop()


# @with_named_setup(setup_func, teardown_func)
# def test_L3EthStarAttackArpEnip():
#     """
#     attacker ARP poison plc1 and hmi using ettercap. 
#     passive and active ARP spoofing

#     cpppo is used to simulate enip client/server
    
#     remote controller (eg: pox) 
#     can be used to mitigate ARP poisoning.

#     """
#     raise SkipTest

#     topo = L3EthStarAttack()

#     # built-in mininet controller
#     # net = Mininet(topo=topo, link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
#     # logger.info("started mininet default controller")

#     net = Mininet(topo=topo, link=TCLink, controller=None, listenPort=c.OF_MISC['switch_debug_port'])
#     net.addController( 'c0',
#             controller=RemoteController,
#             ip='127.0.0.1',
#             port=c.OF_MISC['controller_port'] )
#     logger.info("started remote controller")

#     # then you can create a custom controller class and
#     # init automatically when invoking mininet
#     # eg: controller = POXAntiArpPoison

#     net.start()
#     plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
#     # assert(type(plc1.IP())==str)

#     logger.info("pre-arp poisoning phase (eg open wireshark)")
#     CLI(net)

#     # PASSIVE remote ARP poisoning
#     target_ip1 = plc1.IP()
#     target_ip2 = hmi.IP()
#     attacker_interface = 'attacker-eth0'
#     attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
#             target_ip1,
#             target_ip2, attacker_interface)
#     attacker.cmd(attacker_cmd)

#     # enip communication btw plc1 server and hmi client
#     # TODO: work with multiple realistic tags

#     logger.info("attacker arp poisoned hmi and plc1")
#     CLI(net)

#     taglist = 'pump=INT[10]'
#     server_cmd = "./scripts/cpppo/server.sh %s %s %s %s" % (
#             './temp/workshop/cppposerver.err',
#             plc1.IP(),
#             taglist,
#             './temp/workshop/cppposerver.out')
#     plc1.cmd(server_cmd)
#     client_cmd = "./scripts/cpppo/client.sh %s %s %s %s" % (
#             './temp/workshop/cpppoclient.err',
#             plc1.IP(),
#             'pump[0]=0',
#             './temp/workshop/cpppoclient.out')
#     hmi.cmd(client_cmd)

#     logger.info("ENIP traffic from hmi to plc1 generated")
#     CLI(net)

#     net.stop()


# @with_named_setup(setup_func, teardown_func_clear)
# def test_L3EthStarAttackDoubleAp():
#     """
#     plc2 ARP poison plc3 and plc4 (passive internal)
#     swat external attacker ARP poison plc1 and hmi (passive external)

#     cpppo is used to simulate enip client/server
    
#     remote controller (eg: pox) 
#     can be used to mitigate ARP poisoning.

#     """
#     raise SkipTest

#     topo = L3EthStarAttack()

#     # net = Mininet(topo=topo, link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
#     # logger.info("started mininet default controller")


#     # mininet remote controller
#     net = Mininet(topo=topo, link=TCLink, controller=None, listenPort=c.OF_MISC['switch_debug_port'])
#     net.addController( 'c0',
#             controller=RemoteController,
#             ip='127.0.0.1',
#             port=c.OF_MISC['controller_port'] )
#     logger.info("started remote controller")

#     net.start()
#     plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
#     plc2, plc3, plc4 = net.get('plc2', 'plc3', 'plc4')

#     logger.info("pre-arp poisoning phase (eg open wireshark)")
#     CLI(net)

#     # PASSIVE remote ARP poisoning
#     target_ip1 = plc1.IP()
#     target_ip2 = hmi.IP()
#     attacker_interface = 'attacker-eth0'
#     attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
#             target_ip1,
#             target_ip2, attacker_interface)
#     attacker.cmd(attacker_cmd)
#     logger.info("attacker arp poisoned hmi and plc1")

#     target_ip1 = plc3.IP()
#     target_ip2 = plc4.IP()
#     attacker_interface = 'plc2-eth0'
#     attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
#             target_ip1,
#             target_ip2, attacker_interface)
#     plc2.cmd(attacker_cmd)
#     logger.info("plc2 arp poisoned plc3 and plc4")

#     CLI(net)

#     # taglist = 'pump=INT[10]'
#     # server_cmd = "./scripts/cpppo/server.sh %s %s %s %s" % (
#     #         './temp/workshop/cppposerver.err',
#     #         plc1.IP(),
#     #         taglist,
#     #         './temp/workshop/cppposerver.out')
#     # plc1.cmd(server_cmd)
#     # client_cmd = "./scripts/cpppo/client.sh %s %s %s %s" % (
#     #         './temp/workshop/cpppoclient.err',
#     #         plc1.IP(),
#     #         'pump[0]=0',
#     #         './temp/workshop/cpppoclient.out')
#     # hmi.cmd(client_cmd)

#     # logger.info("ENIP traffic from hmi to plc1 generated")
#     # CLI(net)

#     net.stop()


# @with_named_setup(setup_func, teardown_func_clear)
# def test_Workshop():
#     """
#     workshop

#     """
#     # raise SkipTest

#     topo = L3EthStarAttack()

#     net = Mininet(topo=topo, link=TCLink, controller=None, listenPort=c.OF_MISC['switch_debug_port'])
#     net.addController( 'c0',
#             controller=RemoteController,
#             ip='127.0.0.1',
#             port=c.OF_MISC['controller_port'] )
#     logger.info("started remote controller")

#     net.start()
#     plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
#     plc2, plc3, plc4 = net.get('plc2', 'plc3', 'plc4')

#     logger.info("./pox.py openflow.of_01 --port=6633 --address=127.0.0.1 log.level --DEBUG swat_controller")

#     logger.info("pre-arp poisoning phase (eg open wireshark)")
#     CLI(net)

#     # PASSIVE remote ARP poisoning
#     target_ip1 = plc1.IP()
#     target_ip2 = hmi.IP()
#     attacker_interface = 'attacker-eth0'
#     attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
#             target_ip1,
#             target_ip2, attacker_interface)
#     attacker.cmd(attacker_cmd)
#     logger.info("attacker arp poisoned hmi and plc1")

#     target_ip1 = plc3.IP()
#     target_ip2 = plc4.IP()
#     attacker_interface = 'plc2-eth0'
#     attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % (
#             target_ip1,
#             target_ip2, attacker_interface)
#     plc2.cmd(attacker_cmd)
#     logger.info("plc2 arp poisoned plc3 and plc4")

#     CLI(net)

#     # taglist = 'pump=INT[10]'
#     # server_cmd = "./scripts/cpppo/server.sh %s %s %s %s" % (
#     #         './temp/workshop/cppposerver.err',
#     #         plc1.IP(),
#     #         taglist,
#     #         './temp/workshop/cppposerver.out')
#     # plc1.cmd(server_cmd)
#     # client_cmd = "./scripts/cpppo/client.sh %s %s %s %s" % (
#     #         './temp/workshop/cpppoclient.err',
#     #         plc1.IP(),
#     #         'pump[0]=0',
#     #         './temp/workshop/cpppoclient.out')
#     # hmi.cmd(client_cmd)

#     # logger.info("ENIP traffic from hmi to plc1 generated")
#     # CLI(net)

#     net.stop()
