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
setLogLevel(c.TEST_LOG_LEVEL)

def L3EthStarMonitoring(controller=POXSwatController, hh_lvl=1000.0, ll_lvl=500.0, timeout=120, timer=1):
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

    # the two tags : flow=REAL and pump=SINT (BOOL, 0 or 1)
    tags_array = {}
    tag1 = "flow1"
    tag2 = "pump1"
    tags_array[tag1] = "REAL"
    tags_array[tag2] = "INT"

    # creates the tag string for the cpppo server
    tags = ""
    for tag_name in tags_array:
        tag_type = tags_array[tag_name]
        tags += "%s=%s " % (
            tag_name,
            tag_type)
        
    # create a cpppo server on plc1
    server_cmd = "python -m cpppo.server.enip -v -l %s %s &" % (
        plc1.name + "/" + plc1.name + "_monitoring_server.log",
        tags)
    output = plc1.cmd(server_cmd)

    # start the plc thread, reading flow level from a file and writing its actions into another, and actualizing its tags accordingly to the flow level
    plc1.cmd("python plc_routine.py %s %s %d %d %f %f %s %s %s %s &" % (
        plc1.name + "/" + plc1.name + "_sensor.txt",
        plc1.name + "/" + plc1.name + "_action.txt",
        timeout,
        timer,
        hh_lvl,
        ll_lvl,
        tag1,
        tag2,
        plc1.IP(),
        plc1.name + "/" + plc1.name + "_monitoring_client.log"))

    # start the hmi which queries the server and draw flow and pump graphs
    logger.info("Please wait " + str(timeout) + " seconds.")
    out = hmi.cmd("python hmi_routine.py %f %f %s %s %s %s" %(
        timeout,
        timer,
        tag1,
        tag2,
        plc1.IP(),
        hmi.name + "/" + hmi.name + "_monitoring.pdf"))

    logger.info(out)
    net.stop()

def main():
    L3EthStarMonitoring()

if __name__ == '__main__':
    main()
