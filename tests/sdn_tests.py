"""
sdn_tests.
"""

import time

# TODO: move to swat
from mininet.net import Mininet
from mininet.node import RemoteController  # CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI

from nose.plugins.skip import SkipTest  # Skip

from minicps.sdn import OF_MISC, POXL2Pairs
from minicps.utils import _arp_cache_rtts
# from minicps.networks import L3EthStar  # TODO from topology


@SkipTest
def test_POXL2Pairs():
    """Test build-in forwarding.l2_pairs controller
    that adds flow entries using only MAC info.
    """

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=OF_MISC['switch_debug_port'])
    net.start()

    CLI(net)

    net.stop()


@SkipTest
def test_RemoteController():
    """Test L3EthStar with a remote controller
    eg: pox controller
    """

    topo = L3EthStarAttack()
    net = Mininet(
        topo=topo,
        controller=None,
        link=TCLink, listenPort=OF_MISC['switch_debug_port'])
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=OF_MISC['controller_port'])
    net.start()

    CLI(net)

    net.stop()


@SkipTest
def test_POXSwatController():
    """See /logs folder for controller info"""

    topo = L3EthStar()
    net = Mininet(
        topo=topo,
        controller=POXSwatController,
        link=TCLink, listenPort=OF_MISC['switch_debug_port'])
    net.start()

    CLI(net)

    net.stop()


@SkipTest
def test_POXAntiArpPoison():
    """TODO Test AntiArpPoison controller."""

    topo = L3EthStar()
    controller = POXAntiArpPoison
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=OF_MISC['switch_debug_port'])
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


@SkipTest
def test_POXL2PairsRtt():
    """Test build-in forwarding.l2_pairs controller RTT
    that adds flow entries using only MAC info.
    """

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=OF_MISC['switch_debug_port'])
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = _arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(
            first_rtt, second_rtt,
            c.ASSERTION_ERRORS['no_learning'])
        deltas.append(first_rtt - second_rtt)

    # CLI(net)

    net.stop()


@SkipTest
def test_POXL2LearningRtt():
    """Test build-in forwarding.l2_learning controller RTT
    that adds flow entries using only MAC info.
    """

    topo = L3EthStar()
    controller = POXL2Learning
    net = Mininet(
        topo=topo,
        controller=controller,
        link=TCLink, listenPort=OF_MISC['switch_debug_port'])
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = _arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(
            first_rtt, second_rtt,
            c.ASSERTION_ERRORS['no_learning'])
        deltas.append(first_rtt - second_rtt)

    # CLI(net)

    net.stop()


@SkipTest
def test_Workshop():
    """Ideal link double MITM"""

    topo = L3EthStarAttack()
    net = Mininet(
        topo=topo, link=TCLink,
        listenPort=OF_MISC['switch_debug_port'])
    net.start()

    plc1, attacker, hmi = net.get('plc1', 'attacker', 'hmi')
    plc2, plc3, plc4 = net.get('plc2', 'plc3', 'plc4')

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

    target_ip1 = plc3.IP()
    target_ip2 = plc4.IP()
    attacker_interface = 'plc2-eth0'
    attacker_cmd = 'scripts/attacks/arp-mitm.sh %s %s %s &' % (
        target_ip1,
        target_ip2,
        attacker_interface)
    plc2.cmd(attacker_cmd)

    CLI(net)

    net.stop()
