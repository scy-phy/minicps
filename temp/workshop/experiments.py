#!/usr/bin/python

"""
TODO: test
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
    Connects Historian, Workstation and process PLCs
    using a 5-port ethernet switch.
    An industrial firewall service router filter the traffic.
    """

    def build(self, n=8):
        """
        mininet doesn't like long host names
        eg: workstion abbreviated to workstn
        """

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


class L3EthStarAttack(Topo):

    """
    Like L3EthStar but with an additional host used
    as attacker
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


def mininetLauncher():

    # topo = EthStar()
    # topo = L3EthStar()
    topo = L3EthStarAttack()
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
        # tag_bool = "pump%d=SINT[%d]" % (i, 1)  # represent a bool
        tag_bool = "pump%d=SINT" % i  # represent a bool

        print tag_int
        print tag_bool

        # default listen port is 44818
        # notice that in the loop im' cd'ing to plci folder
        log_path = "%s_enip_server.log" % key
        enip_server = "python -m cpppo.server.enip -l %s %s %s &" % (
                log_path,
                tag_int,
                tag_bool
                )
        plc.cmd(enip_server)
        # check server with plc1 ps, take note of the PID and than
        # query it again


    CLI(net)

    net.stop()


if __name__ == '__main__':
    mininetLauncher()
