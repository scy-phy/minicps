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

def L3EthStarTraffic(controller=POXSwatController, nb_messages=5, tag_range=10, min=0, max=8, auto_mode=True):
    """
    a L3EthStarAttack topology with some basic cpppo traffic between the plcs.
    2 flags are used PUMP=INT[tag_range] and BOOL=SINT[tag_range].

    the number of exchanges can be set, and also the size of the tag array, and the mini/maxi values the PUMP tag can have
    the default controller used is the swat one. It can be changed or set to None to use a remote controller.

    cpppo is used to simulate enip client/server, nb_messages*nb_plcs*(nb_plcs-1) are sent, randomly either in read or write mode, the pump numbers and the write values are also chosen randomly
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

    # starting capture by user input
    hosts_names = ""
    for host in net.hosts:
        hosts_names += host.name + " "
    logger.info("type the following command to see the traffic on a host: " + "xterm <host name>")
    logger.info("Hosts available: " + hosts_names)
    hosts_ifaces = ""
    for host in net.hosts:
        hosts_ifaces += str(host.intfs) + " "
    logger.info("then on the xterm type: " + "wireshark -k -i <host-interface> &")
    logger.info("Interfaces available: " + hosts_ifaces)
    logger.info("then exit mininet console")
    CLI(net)

    # enip communication between workstn server and other hosts client
    # set the cpppo tags, eg. PUMP=INT[tag_range] BOOL=INT[tag_range]
    tags_array = {}
    tag1 = "PUMP"
    tag2 = "BOOL"
    tags_array[tag1] = "INT", tag_range
    tags_array[tag2] = "INT", tag_range

    tags = ""
    for tag_name in tags_array:
        type, value = tags_array[tag_name]
        tags += "%s=%s[%d] " % (
            tag_name,
            type,
            value)
        
    # create all cpppo server on plcs with the 2 tags
    plc_name = "plc"
    for host in net.hosts:
        if( (host.name).find(plc_name) != -1 ):
            server_cmd = "python -m cpppo.server.enip -vv -l %s %s %s &" % (
                host.name + "/" + host.name + "_traffic_server.log",
                host.IP(),
                tags)
            output = host.cmd(server_cmd)
    logger.info("ENIP servers launched on plcs")

    if(auto_mode):
        # client part, traffic randomly generated
        logger.info("processing ENIP traffic, please wait...")    
        logger.info(str(nb_messages) + " messages to generate")
        for i in range(nb_messages):
            for host in net.hosts:
                if((host.name).find(plc_name) != -1):
                    for other_host in net.hosts:
                        if((other_host != host) and ((other_host.name).find(plc_name) != -1)):
                            # random choice, read a tag or write it (True read and False write)
                            read_write = random.choice([True, False])
                            tags = ""
                            tag_i = random.randrange(0, tag_range)
                            # set the client tags
                            # read instructions
                            if(read_write == True):
                                for tag_name in tags_array:
                                    tags += "%s[%d] " % (
                                        tag_name,
                                        tag_i)
                                    # write instructions
                            else:
                                for tag_name in tags_array:
                                    if(tag_name != tag2):
                                        tag_value = random.randint(min, max)
                                    else:
                                        tag_value = random.getrandbits(1)
                                        # write instructions
                                        tags += "%s[%d]=%d " % (
                                            tag_name,
                                            tag_i,
                                            tag_value)
                            # send them to the server on the other_host
                            # use -m to force use of the Multiple Service Packet request
                            # use -n to force the client to use plain Read/Write Tag commands
                            client_cmd = "python -m cpppo.server.enip.client -vv -l %s -a %s %s" % (
                                host.name + "/" + host.name + "_traffic_client.log",
                                other_host.IP(),
                                tags)
                            output = host.cmd(client_cmd)
            logger.info("message " + str(i+1) + " sent by all hosts")
        logger.info("ENIP traffic from clients to server generated, end of the test.")
    CLI(net)
    net.stop()

def main():
    L3EthStarTraffic()

if __name__ == '__main__':
    main()
