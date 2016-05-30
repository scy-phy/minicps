"""
swat-s1 tests.
"""

from mininet.cli import CLI
from mininet.net import Mininet

from nose.plugins.skip import SkipTest

from topo import SwatTopo

import subprocess
import sys


def test_init():

    pass


def test_topo():

    topo = SwatTopo()
    net = Mininet(topo=topo)

    net.start()
    net.pingAll()
    net.stop()


def test_plcs():

    pass
