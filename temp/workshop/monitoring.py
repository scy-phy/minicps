#!/usr/bin/python

import sys
sys.path.append("../../")

from time import sleep
import random

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, RemoteController, Host
from mininet.link import TCLink
from mininet.cli import CLI

from minicps import constants as c
from minicps.topology import EthStar, Minicps, DLR, L3EthStar, L3EthStarAttack
from minicps.devices import POXSwatController

import logging
logger = logging.getLogger('minicps.topology')
# setLogLevel(TODO)

def L3EthStarMonitoring(controller=POXSwatController, timeout=120, timer=1):
    """
    a L3EthStarAttack topology where plc1 is running a enip server, which reads flow values in a sensor file and writes the according pump behavior in an action file, and actalizes its tags values (pump a sint, and flow a real)
    hmi is running a enip client which frequently queries the plc1 server in order to draw flow graph and pump decisions graph.
    """
    # use the L3EthStarAttack topology
    topo = L3EthStarAttack()
    
    net = Mininet(topo=topo, link=TCLink, controller=controller, listenPort=c.OF_MISC['switch_debug_port'])

    if(controller == None):
        net.addController( 'c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           port=c.OF_MISC['controller_port'] )
        logger.info("started remote controller")

    net.start()
    plc1, hmi = net.get('plc1', 'hmi')


    flow = "flow"
    pump1 = "pump1"
    pump2 = "pump2"

    tags = {}
    tags[flow] = "REAL"
    tags[pump1] = "INT"
    tags[pump2] = "INT"
    
    # start the plc thread, reading flow level from a file and writing its actions into another, and actualizing its tags accordingly to the flow level
    out = plc1.cmd("python plc_routine.py %s %s %f %f %s %s %d %s %s %s %s %s %s &" % (
        plc1.IP(),
        plc1.name + "/",
        timer,
        timeout,
        "out.json",
        "server.log",
        80,
        flow,
        tags[flow],
        pump1,
        tags[pump1],
        pump2,
        tags[pump2]))

    # start the hmi which queries the server and draw flow and pump graphs
    out = hmi.cmd("python hmi_routine.py %s %s %f %f %s %s %s %s %s %s %s &" %(
        plc1.IP(),
        hmi.name + "/",
        timer,
        timeout,
        "graphs.png",
        flow,
        tags[flow],
        pump1,
        tags[pump1],
        pump2,
        tags[pump2]))

    logger.info("Please wait %3.2f seconds." % timeout)
    sleep(timeout)
    logger.info("Test finished, exiting.")
    CLI(net)
    net.stop()

def main():
    L3EthStarMonitoring()

if __name__ == '__main__':
    main()
