"""
Use MiniCPS to simulate the first SWaT subprocess.

A state_db is used to represent the actual state of the system

Graph_name functions are used to build networkx graphs representing the
topology you want to build.
"""

import time
import os
import sys


from minicps.networks import MininetTopoFromNxGraph
from minicps.sdn import POXSwat

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink

from utils import init_swat, nxgraph_sub1


def minicps_tutorial(net):
    """
    Settings used for tutorial

    :net: Mininet instance reference

    """

    init_swat()
    time.sleep(2)

    # Start mininet
    net.start()

    # Get references to nodes (each node is a Linux container)
    plc1, plc2, plc3, hmi, s1 = net.get('plc1', 'plc2', 'plc3', 'hmi', 's1')

    # SPHINX_SWAT_TUTORIAL SET PLC1
    # plc1.cmd(
    #     "python examples/swat/plc1a.py 2> examples/swat/err/plc1a.err &")
    plc1.cmd("python examples/swat/plc1.py 2> examples/swat/err/plc1.err &")
    # SPHINX_SWAT_TUTORIAL END SET PLC1

    plc2.cmd("python examples/swat/plc2.py 2> examples/swat/err/plc2.err &")
    plc3.cmd("python examples/swat/plc3.py 2> examples/swat/err/plc3.err &")
    hmi.cmd("python examples/swat/hmi.py 2> examples/swat/err/hmi.err &")

    # Start the physical process
    s1.cmd(
        "python examples/swat/physical_process.py "
        "2> examples/swat/err/pp.err &")

    # SPHINX_SWAT_TUTORIAL SET POPUP
    # Displays an image to monitor the physical process activity
    # That it will refresh every 200 ms
    os.system(
        "python examples/swat/ImageContainer.py examples/swat/hmi/plc1.png "
        "1200 2> examples/swat/err/ImageContainer.err &")
    # SPHINX_SWAT_TUTORIAL END SET POPUP

    CLI(net)

    net.stop()


if __name__ == '__main__':

    # SPHINX_SWAT_TUTORIAL SET ATTACKER
    # swat_graph = nxgraph_sub1(attacker=False)
    # SPHINX_SWAT_TUTORIAL END ATTACKER

    # topo = MininetTopoFromNxGraph(swat_graph)

    # SPHINX_SWAT_TUTORIAL SET SDN CONTROLLER
    # net = Mininet(topo=topo, link=TCLink, listenPort=6634)
    # comment above and uncomment below to enable POXSwat SDN controller
    # controller = POXSwat
    # net = Mininet(
    #     topo=topo, controller=controller,
    #     link=TCLink, listenPort=6634)
    # SPHINX_SWAT_TUTORIAL END SET SDN CONTROLLER

    # minicps_tutorial(net)

    print 'DEBUG: redo'
