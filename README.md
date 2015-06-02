# MiniCPS #
MiniCPS is a lightweight simulatior for accurate network traffic in an industrial control system, with basic support for physical layer interaction.

## Installation ##

We recommend the use of a mininet VM (http://mininet.org/download/) to run minicps. Once the VM is set up, run the following to install the environment:

    cd; mkdir scy-phy; cd scy-phy
    git clone https://github.com/scy-phy/minicps
    cd; git clone http://github.com/noxrepo/pox
    sudo apt-get install python-pip python-nose tee
    sudo pip install cpppo pycomm nose-conver3

In order to reduce the network traffic in an IPv4-only environment, you can disable IPv6 on the mininet VM by running the following commands:

    echo 'net.ipv6.conf.all.disable_ipv6 = 1' | sudo tee /etc/sysctl.d/60-disable-ipv6.conf
    echo 'net.ipv6.conf.default.disable_ipv6 = 1' | sudo tee -a /etc/sysctl.d/60-disable-ipv6.conf
    sysctl -p /etc/sysctl.d/60-disable-ipv6.conf

## Testing ##

Use with_setup decorator to call tests fixtures. It is possible to use different fixtures for different tests.

SkipTest can be used as a switch to intentionally skip a test. You
can see skipped test summary in the nosetest output.

To run a single test whitin a script use /path/to/test:test_name witouth parenthesis.

use -s opt to prevent nosetest to capture stdout.
use -v opt to obtain a more verbose output.

## Ettercap ##

Open `/etc/ettercap/etter.conf`

Change user and group ids (nobody is the default):

    [privs]
    ec_uid = 0
    ec_gid = 0

If you use Linux's `iptables` uncomment:

    redir_command_on = "iptables -t nat -A PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport"
    redir_command_off = "iptables -t nat -D PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport"

## Links ##

SWaT:
[datasheetarchive](http://www.datasheetarchive.com/)
[Allen-Bradley ControlLogix products page](http://ab.rockwellautomation.com/programmable-controllers/controllogix#overview)

SDN:
[thenewstack article series](http://thenewstack.io/defining-software-defined-networking-part-1/)
[ONF repo](http://opennetworkingfoundation.github.io/libfluid/index.html)
[mininet](http://mininet.org/)
[sdnhub](http://sdnhub.org/)

OpenFlow
[NOX(POX)](http://www.noxrepo.org/)
[POX wiki](https://openflow.stanford.edu/display/ONL/POX+Wiki)
[Ryu](https://osrg.github.io/ryu/)
[List](http://yuba.stanford.edu/~casado/of-sw.html)

Videos:
[Scott Shenker: why SDN](https://osrg.github.io/ryu/)


