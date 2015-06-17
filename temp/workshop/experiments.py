#!/usr/bin/python

"""
Workshop script used to demo mininet, cpppo and minicps.
"""

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI

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


def mininetLauncher(number):

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

    # starts webservers listening on port 80
    # quet it using wget -O - plc_ip
    tag_int_len = 20
    for i in range(1, 7):
        key = 'plc'+str(i)
        plc = net.get(key)
        # hosts[key].cmd(simple_http)
        plc.cmd('cd temp/workshop/%s' % key)

        simple_http = "python -m SimpleHTTPServer 80 &"
        enip_server = ""
        plc.cmd(simple_http)

        # create all cpppo server on plcs with the 2 tags
        # tags_array = {}
        # tags_array["PUMP"] = "INT", tag_range
        # tags_array["BOOL"] = "SINT", tag_range

        tag_int = "flow%d=INT[%d]" % (i, tag_int_len)
        tag_bool = "pump%d=INT[1]" % i  # represent a bool

        # print tag_int
        # print tag_bool

        # default listen port is 44818
        # notice that in the loop im' cd'ing to plci folder
        server_errlog = "%s_enip_server.err" % key
        open(server_errlog, 'w').close()
        enip_server = "python -m cpppo.server.enip -l %s %s %s -a %s &" % (
                server_errlog,
                tag_int,
                tag_bool,
                plc.IP()+':44818'
                )
        plc.cmd(enip_server)
        # check server with plc1 ps, take note of the PID and than
        # query it again


    # start a ENIP client on hmi that periodically read/write from plc1 enip server
    hmi = net.get('hmi')
    client_errlog = "temp/workshop/hmi_enip_client.err"
    client_log = "temp/workshop/hmi_enip_client.log"
    open(client_errlog, 'w').close()
    open(client_log, 'w').close()
    

    # write and read
    enip_client = "python -m cpppo.server.enip.client --print -l %s -a %s %s %s %s %s >> %s" % (
        client_errlog,
        PLCS_IP['plc1'],
        "pump1=1",
        "pump1",
        "flow1[0-3]=0,1,2,3",
        "flow1[0-3]",
        client_log
    )
    # print enip_client

    loop_cmd = """
    while sleep 2; do 
    %s
    done
    """ % (enip_client)

    if number == 0:
        hmi.cmd(enip_client)
    elif number == 1:
        hmi.cmd(loop_cmd)
        print "hmi is quering plc1 every 2 second an logging into temp/workshop/hmi_enip_client.log"

    print "Each plcX runs an cpppo ENIP server with pumpX and flowX[%d] int tags" % tag_int_len
    print "Each plc runs a SimpleHTTPServer on port 80"

    CLI(net)

    net.stop()


if __name__ == '__main__':
    # Change to the top directory
    import os
    import os.path
    import sys

    os.chdir(os.path.join(os.path.dirname(__file__), '..', '..'))

    if len(sys.argv) > 1:
        print sys.argv[0]
        print sys.argv[1]
        number = sys.argv[1]
        mininetLauncher(int(number))
    else:
        exit("ERROR: Please pass either a command line argument [0] or [1]")

