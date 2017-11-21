"""
run.py
"""

from subprocess import call

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Node

from minicps.mcps import MiniCPS

from topo import MixTopo
from utils import IP

import sys

from time import sleep


if __name__ == '__main__':

    setLogLevel( 'info' )

    topo = MixTopo()
    net = Mininet(topo=topo)

    s1 = net['s1']

    plc2 = net['plc2']
    plc3 = net['plc3']

    s2, rtu2a, scada = net.get('s2', 'rtu2a', 'scada')
    rtu2b, attacker2 = net.get('rtu2b', 'attacker2')
    s3 = net.get('s3')

    # NOTE: root-eth0 interface on the host
    root = Node('root', inNamespace=False)
    intf = net.addLink(root, s3).intf1
    print('DEBUG root intf: {}'.format(intf))
    root.setIP('10.0.0.30', intf=intf)
    # NOTE: all packet from root to the 10.0.0.0 network
    root.cmd('route add -net ' + '10.0.0.0' + ' dev ' + str(intf))


    net.start()

    # NOTE: use for debugging
    #s1.cmd('tcpdump -i s1-eth1 -w /tmp/s1-eth1.pcap &')
    #s1.cmd('tcpdump -i s1-eth2 -w /tmp/s1-eth2.pcap &')

    SLEEP = 0.5

    # NOTE: swat challenge 1 and 2
    plc3.cmd(sys.executable + ' plc3.py &')
    sleep(SLEEP)
    plc2.cmd(sys.executable + ' plc2.py &')
    sleep(SLEEP)

    # NOTE: wadi challenge 1
    scada.cmd(sys.executable + ' scada.py &')
    sleep(SLEEP)
    rtu2a.cmd(sys.executable + ' rtu2a.py &')
    sleep(SLEEP)
    # NOTE: wadi challenge 2
    rtu2b.cmd(sys.executable + ' rtu2b.py &')
    sleep(SLEEP)



    CLI(net)



    net.stop()


    print "*** Running clean.sh"
    call('./clean.sh')
