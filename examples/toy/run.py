"""
toy run.py
"""

import os
import sys
from mininet.net import Mininet
from minicps.mcps import MiniCPS

# TODO: find a nicer way to manage examples path
sys.path.append(os.getcwd())
from examples.toy.topo import ToyTopo


if __name__ == "__main__":

    topo = ToyTopo()
    net = Mininet(topo=topo)

    minicps = MiniCPS(
        name='toy',
        net=net,
        path='examples/toy')
