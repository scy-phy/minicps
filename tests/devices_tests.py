"""
Devices tests

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
def test_POXLearningSwitch():
    """TODO: Docstring for test_LearningSwitch.

    """
    pass
