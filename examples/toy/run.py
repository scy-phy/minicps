"""
toy run.py
"""

import os
import sys
# TODO: find a nicer way to manage path
sys.path.append(os.getcwd())

from mininet.net import Mininet
from minicps.mcps import MiniCPS
from examples.toy.topo import ToyTopo


if __name__ == "__main__":

    topo = ToyTopo()
    net = Mininet(topo=topo)

    minicps = MiniCPS(
        name='toy',
        net=net)
