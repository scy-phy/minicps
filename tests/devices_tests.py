"""
Devices tests

time.sleep is used after net.start() to synch python interpreter with
the mininet init process.

POX prefixed ClassNames indicate controller coded into script/pox dir
and symlinked to ~/pox/pox/forwarding dir.
"""

from nose.tools import *
from nose.plugins.skip import Skip, SkipTest

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

from minicps import constants as c
from minicps.topology import EthStar, Minicps, DLR, L3EthStar
from minicps.devices import POXL2Pairs, POXL2Learning, POXAntiArpPoison, POXProva
from minicps.constants import _arp_cache_rtts

import os
import time

import logging
logger = logging.getLogger('minicps.devices')
setLogLevel(c.TEST_LOG_LEVEL)


def setup_func(test_name):
    logger.info('Inside %s' % test_name)

def teardown_func(test_name):
    logger.info('Leaving %s' % test_name)

def with_named_setup(setup=None, teardown=None):
    def wrap(f):
        return with_setup(
            lambda: setup(f.__name__) if (setup is not None) else None, 
            lambda: teardown(f.__name__) if (teardown is not None) else None)(f)
    return wrap


@with_named_setup(setup_func, teardown_func)
def test_POXL2Pairs():
    """Test build-in forwarding.l2_pairs controller
    that adds flow entries using only MAC info.
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXL2Pairs
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()

    CLI(net)

    net.stop()



@with_named_setup(setup_func, teardown_func)
def test_RemoteController():
    """Test L3EthStar with a remote controller
    eg: pox controller
    """
    # raise SkipTest

    topo = L3EthStar()
    net = Mininet( topo=topo, controller=None, link=TCLink)
    net.addController( 'c0',
            controller=RemoteController,
            ip='127.0.0.1',
            port=6633 )
    net.start()

    CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXProva():
    """Test forwarding.prova
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXProva
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()

    CLI(net)

    net.stop()


@with_named_setup(setup_func, teardown_func)
def test_POXAntiArpPoison():
    """TODO Test AntiArpPoison controller.
    """
    raise SkipTest

    topo = L3EthStar()
    controller = POXAntiArpPoison
    net = Mininet(topo=topo, controller=controller, link=TCLink)
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
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = _arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(first_rtt, second_rtt,
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
    net = Mininet(topo=topo, controller=controller, link=TCLink)
    net.start()
    time.sleep(1)  # allow mininet to init processes

    deltas = []
    for i in range(5):
        first_rtt, second_rtt = _arp_cache_rtts(net, 'plc1', 'plc2')
        assert_greater(first_rtt, second_rtt,
                c.ASSERTION_ERRORS['no_learning'])
        deltas.append(first_rtt - second_rtt)
    logger.debug('deltas: %s' % deltas.__str__())

    # CLI(net)

    net.stop()


