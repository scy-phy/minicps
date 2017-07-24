"""
swat-s1 tests.
"""

# from mininet.cli import CLI
from mininet.net import Mininet

from utils import STATE, RWT_INIT_LEVEL
from utils import TANK_SECTION
from topo import SwatTopo
from physical_process import RawWaterTank


# import subprocess
# import sys


def test_init():

    pass


def test_topo():

    topo = SwatTopo()
    net = Mininet(topo=topo)

    net.start()
    net.pingAll()
    net.stop()


def test_raw_water_tank():

    RawWaterTank(
        name='test_rwt',
        state=STATE,
        protocol=None,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )
