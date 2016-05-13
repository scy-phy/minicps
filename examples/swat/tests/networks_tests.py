"""
swat networks tests
"""
from nose.tools import ok_
# from nose.plugins.skip import Skip, SkipTest

from minicps.sdn import OF_MISC

from examples.swat.utils import L1_PLCS_IP, L3_NODES, PLCS_MAC
from examples.swat.utils import L3_PLANT_NETWORK, OTHER_MACS
from examples.swat.networks import L3EthStar

from mininet.net import Mininet
from mininet.link import TCLink
# from mininet.cli import CLI


def test_L3EthStar():
    """Test L3 Ring MACs and IPs"""
    # raise SkipTest

    topo = L3EthStar()
    net = Mininet(
        topo=topo,
        link=TCLink,
        listenPort=OF_MISC['switch_debug_port'])

    net.start()

    n = L3_NODES
    for h in range(n - 2):
        key = 'plc%s' % (h + 1)
        plc = net.get(key)  # get host obj reference by name
        ok_(plc.IP(), L1_PLCS_IP[key])
        ok_(plc.MAC(), PLCS_MAC[key])

    histn = net.get('histn')
    ok_(histn.IP(), L3_PLANT_NETWORK['histn'])
    ok_(histn.MAC(), OTHER_MACS['histn'])

    workstn = net.get('workstn')
    ok_(workstn.IP(), L3_PLANT_NETWORK['workstn'])
    ok_(workstn.MAC(), OTHER_MACS['workstn'])

    # alternative way to obtain IP and MAC
    # params = workstn.params

    net.stop()
