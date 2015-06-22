#!/usr/bin/python

"""
Workshop script used to demo mininet, cpppo and minicps.
"""

import sys
sys.path.append("../../")

import signal
from time import time
from time import sleep
import random

from mininet.topo import Topo
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

LINKOPTS = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)

NETMASK = '/24'

PLCS_IP = {
    'plc1':  '192.168.1.10',
    'plc2':  '192.168.1.20',
    'plc3':  '192.168.1.30',
    'plc4':  '192.168.1.40',
    'plc5':  '192.168.1.50',
    'plc6':  '192.168.1.60',
    'plc7':  '192.168.1.70',
    'attacker': '192.168.1.77',
}

PLCS_MAC = {
    'plc1':  '00:1D:9C:C7:B0:70',
    'plc2':  '00:1D:9C:C8:BC:46',
    'plc3':  '00:1D:9C:C8:BD:F2',
    'plc4':  '00:1D:9C:C7:FA:2C',
    'plc5':  '00:1D:9C:C8:BC:2F',
    'plc6':  '00:1D:9C:C7:FA:2D',
    'plc1r': '00:1D:9C:C8:BD:E7',
    'plc2r': '00:1D:9C:C8:BD:0D',
    'plc3r': '00:1D:9C:C7:F8:3B',
    'plc4r': '00:1D:9C:C8:BC:31',
    'plc5r': '00:1D:9C:C8:F4:B9',
    'plc6r': '00:1D:9C:C8:F5:DB',
}

L3_PLANT_NETWORK = {
    'histn':   '192.168.1.200',
    'workstn': '192.168.1.201',
}

OTHER_MACS = {
    'histn':   'B8:2A:72:D7:B0:EC',
    'workstn': '98:90:96:98:CC:49',
    'hmi':     '00:1D:9C:C6:72:E8',
    'attacker': 'AA:AA:AA:AA:AA:AA',  # easy to recognize in the capture
}

L2_HMI = {
    'hmi': '192.168.1.100',
    'wifi_client': '192.168.1.101',
}


class EthStar(Topo):

    """Ethernet star topology with n hosts.
    ovsc and ovss default controller and switch
    that runs on kernel space (faster than user space).
    """

    def build(self, n=2):
        """build the topo"""
        switch = self.addSwitch('s1')

        for h in range(n):
            host = self.addHost('plc%s' % (h + 1))
            self.addLink(host, switch)


class L3EthStar(Topo):

    """
    Use link performance variation
    """

    def build(self, n=8):

        switch = self.addSwitch('s3')

        for h in range(n-2):
            # compute the key reused to access IP and MAC dicts and to name hosts
            key = 'plc%s' % (h + 1)
            host = self.addHost(key, ip=PLCS_IP[key]+NETMASK, mac=PLCS_MAC[key])
            self.addLink(host, switch, **LINKOPTS)

        histn = self.addHost('histn', ip=L3_PLANT_NETWORK['histn']+NETMASK,
                mac=OTHER_MACS['histn'])
        self.addLink(histn, switch)

        workstn = self.addHost('workstn', ip=L3_PLANT_NETWORK['workstn']+NETMASK,
                mac=OTHER_MACS['workstn'])
        self.addLink(workstn, switch)

        hmi = self.addHost('hmi', ip=L2_HMI['hmi']+NETMASK,
                mac=OTHER_MACS['hmi'])
        self.addLink(hmi, switch)


class L3EthStarAttack(Topo):

    """
    Link are ideal

    attacker has aa:aa:aa:aa:aa:aa MAC address
    and 192.168.1.77 IP address
    """

    def build(self, n=8):
        """
        attacker is in the same plc subnet 192.168.1.x
        see constants module for attacker's IP
        and MAC

        link performance are ideal (No TCLink)
        """

        switch = self.addSwitch('s3')


        for h in range(n-2):
            key = 'plc%s' % (h + 1)
            host = self.addHost(key, ip=PLCS_IP[key]+NETMASK, mac=PLCS_MAC[key])
            self.addLink(host, switch)

        attacker = self.addHost('attacker', ip=PLCS_IP['attacker']+NETMASK,
                mac=OTHER_MACS['attacker'])
        self.addLink(attacker, switch)

        # TODO: hmi will be in L2
        hmi = self.addHost('hmi', ip=L2_HMI['hmi']+NETMASK,
                mac=OTHER_MACS['hmi'])
        self.addLink(hmi, switch)

        histn = self.addHost('histn', ip=L3_PLANT_NETWORK['histn']+NETMASK,
                mac=OTHER_MACS['histn'])
        self.addLink(histn, switch)

        workstn = self.addHost('workstn', ip=L3_PLANT_NETWORK['workstn']+NETMASK,
                mac=OTHER_MACS['workstn'])
        self.addLink(workstn, switch)

def handler(signum, frame):
   print "Flow picture available at http://192.168.1.100."

def mininetLauncher(number, timeout=120, timer=1):

    if number == 0:
        topo = L3EthStar()
    elif number == 1:
        topo = L3EthStarAttack()
    else:
        exit("ERROR: Please enter either 0 or 1")

    print "Launch experiment %d" % number

    net = Mininet(topo=topo, link=TCLink, listenPort=6634)

    net.start()

    hosts = net.items()
    plc1, hmi = net.get('plc1', 'hmi')
    
    # set the enip tags
    flow = "flow"
    pump1 = "pump1"
    pump2 = "pump2"

    tags = {}
    tags[flow] = "REAL"
    tags[pump1] = "INT"
    tags[pump2] = "INT"

    # starts enip and web servers on each plc and run a fill/empty tank
    for i in range(1, 7):
        key = 'plc'+str(i)
        plc = net.get(key)
        plc.cmd("python plc_routine.py %s %s %f %f %s %s %d %s %s %s %s %s %s &" % (
            plc.IP(),
            plc.name + "/",
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

    client_errlog = "hmi/hmi_enip_client.err"
    client_log = "hmi/hmi_enip_client.log"
    open(client_errlog, 'w').close()
    open(client_log, 'w').close()

    # write and read
    enip_client = "python -m cpppo.server.enip.client --print -l %s -a %s %s %s %s %s >> %s" % (
        client_errlog,
        PLCS_IP['plc1'],
        "pump1=1",
        "pump1",
        "flow=2",
        "flow",
        client_log
    )

    if number == 0:
        hmi.cmd(enip_client)
    elif number == 1:
        # start a ENIP client on hmi that periodically read from plc1 enip server and monitors the result in a http web page
        hmi.cmd("python hmi_routine.py %s %s %f %f %s %s %s %s %s %s %s &" %(
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
        print "HMI is quering plc1 every %3.2f seconds." % timer
        print "Each plcX runs an cpppo ENIP server with pump1, pump2 (INT) and flow (REAL) tags."
        print "Each plc and the hmi runs a SimpleHTTPServer on port 80."
        print "Please wait %3.2f seconds before trying to see the hmi output." % timeout
        # Call receive_alarm in 2 seconds
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)
    CLI(net)
    thread.join()
    net.stop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print sys.argv[0]
        print sys.argv[1]
        number = sys.argv[1]
        mininetLauncher(int(number))
    else:
        exit("ERROR: Please pass either a command line argument [0] or [1]")
