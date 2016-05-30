"""
swat-s1 tests.
"""

# from mininet.cli import CLI
from mininet.net import Mininet

from physical_process import RawWaterTank

from nose.plugins.skip import SkipTest

from topo import SwatTopo

from utils import STATE, RWT_INIT_LEVEL
from utils import TANK_SECTION

# import subprocess
# import sys


@SkipTest
def test_init():

    pass


def test_topo():

    topo = SwatTopo()
    net = Mininet(topo=topo)

    net.start()
    net.pingAll()
    net.stop()


def test_raw_water_tank():

    rwt = RawWaterTank(
        name='test_rwt',
        state=STATE,
        protocol=None,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )
