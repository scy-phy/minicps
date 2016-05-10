"""
Devices tests

time.sleep is used after net.start() to synch python interpreter with
the mininet init process.

POX prefixed ClassNames indicate controller coded into script/pox dir
and symlinked to ~/pox/pox/forwarding dir.
"""

from nose.plugins.skip import Skip, SkipTest

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

from minicps import constants as c
from minicps.devices import *
from minicps.constants import _arp_cache_rtts, setup_func, teardown_func
from minicps.constants import teardown_func_clear, with_named_setup

import time
import logging
logger = logging.getLogger('minicps.devices')
setLogLevel(c.TEST_LOG_LEVEL)


# review pierre
# @with_named_setup(setup_func, teardown_func)
# def test_ControlDevice():
#     """
#     Test concurrency
#     """
#     # raise SkipTest

#     fs1 = FlowSensor.start('temp/phy-layer/fs1', flow_level=1).proxy()
#     fs2 = FlowSensor.start('temp/phy-layer/fs2', flow_level=2).proxy()
#     mv = MotorizedValve.start('temp/phy-layer/mv2', True).proxy()
#     plc1_logic = PLCLogic1.start('temp/phy-layer/plc1_logic').proxy()
#     sub1 = SWATSub1.start('temp/phy-layer/sub1').proxy()

#     try:
#         future = fs1.append('wow')
#         answer = future.get()
#         print answer

#     finally:
#         fs1.stop()
#         fs2.stop()
#         mv.stop()
#         plc1_logic.stop()
#         sub1.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXL2Pairs():
    """Test build-in forwarding.l2_pairs controller
    that adds flow entries using only MAC info.
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
    net.start()

    CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func_clear)
def test_RemoteController():
    """Test L3EthStar with a remote controller
    eg: pox controller
    """
    raise SkipTest

    topo = L3EthStarAttack()
    net = Mininet(
        topo=topo,
        controller=None,
        link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=c.OF_MISC['controller_port'])
    net.start()

    CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXSwatController():
    """See /logs folder for controller info"""
    raise SkipTest

    topo = L3EthStar()
    net = Mininet(
        topo=topo,
        controller=POXSwatController,
        link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
    net.start()

    CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXAntiArpPoison():
    """TODO Test AntiArpPoison controller."""
    raise SkipTest

    topo = L3EthStar()
    controller = POXAntiArpPoison
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
    net.start()
    time.sleep(1)  # allow mininet to init processes

    plc1, plc2, plc3 = net.get('plc1', 'plc2', 'plc3')

    target_ip1 = plc2.IP()
    target_ip2 = plc3.IP()
    attacker_interface = 'plc1-eth0'

    # plc1_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s' % ( target_ip1,
    #         target_ip2, attacker_interface)
    # plc1.cmd(plc1_cmd)

    CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXL2PairsRtt():
    """Test build-in forwarding.l2_pairs controller RTT
    that adds flow entries using only MAC info.
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = _arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(
            first_rtt, second_rtt,
            c.ASSERTION_ERRORS['no_learning'])
        deltas.append(first_rtt - second_rtt)
    logger.debug('deltas: %s' % deltas.__str__())

    # CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXL2LearningRtt():
    """Test build-in forwarding.l2_learning controller RTT
    that adds flow entries using only MAC info.
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXL2Learning
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=c.OF_MISC['switch_debug_port'])
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = _arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(
            first_rtt, second_rtt,
            c.ASSERTION_ERRORS['no_learning'])
        deltas.append(first_rtt - second_rtt)
    logger.debug('deltas: %s' % deltas.__str__())

    # CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_Workshop():
    """Ideal link double MITM"""
    raise SkipTest

    topo = L3EthStarAttack()
    net = Mininet(
        topo=topo, link=TCLink,
        listenPort=c.OF_MISC['switch_debug_port'])
    net.start()

    plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
    plc2, plc3, plc4 = net.get('plc2', 'plc3', 'plc4')

    logger.info("pre-arp poisoning phase (eg open wireshark)")
    CLI(net)

    # PASSIVE remote ARP poisoning
    target_ip1 = plc1.IP()
    target_ip2 = hmi.IP()
    attacker_interface = 'attacker-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s &' % (
        target_ip1,
        target_ip2,
        attacker_interface)
    attacker.cmd(attacker_cmd)
    logger.info("attacker arp poisoned hmi and plc1")

    target_ip1 = plc3.IP()
    target_ip2 = plc4.IP()
    attacker_interface = 'plc2-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s &' % (
        target_ip1,
        target_ip2,
        attacker_interface)
    plc2.cmd(attacker_cmd)
    logger.info("plc2 arp poisoned plc3 and plc4")

    CLI(net)

    net.stop()
