# MiniCPS #

MiniCPS is a lightweight simulatior for accurate network traffic in an
industrial control system, with basic support for physical layer
interaction.

## Installation ##

We recommend the use of a mininet VM (http://mininet.org/download/) to
run minicps. Once the VM is set up, run the following to install the
environment:

    $ cd; mkdir scy-phy; cd scy-phy
    $ git clone https://github.com/scy-phy/minicps
    $ cd; git clone http://github.com/noxrepo/pox
    # apt-get install python-pip python-nose tee
    # pip install cpppo pycomm nose-cov

To symlink minicps pox controller to pox/ext execute the following
script. Notice that `POX_PATH` defaults to `~/pox` and `MINICPS_PATH`
defaults to `~/minicps`.

    $ ~/minicps/script/pox/init.py [-p POX_PATH -m MINICPS_PATH -vv]
    
In order to reduce the network traffic in an IPv4-only environment,
you can **disable** the Linux IPv6 kernel module:

    # vim /etc/default/grub

then add `ipv6.disable=1` as first parameter in the string.
Note that the `...` poriton of the string depends on your grub config.

    GRUB_CMDLINE_LINUX_DEFAULT="ipv6.disable=1 ..."

then

    # update-grub

then reboot your machine and check it with `ifconfig` that no
`inet6` is listed.

Instruction taken from [here](https://github.com/mininet/mininet/issues/454).

## Testing ##


You can intentionally skipe a particular test adding/uncommenting `raise SkipTest`.
You can see skipped test summary in the nosetest output.

To run a single test whitin a script use `/path/to/test:test_name` (witouth parenthesis).

use `-s` opt to prevent nosetest to capture stdout.
use `-v` opt to obtain a more verbose output.
You can even generate coverage report (read `$ nosetests --help`).

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

OpenFlow:
[OFv1.30 spec](https://www.opennetworking.org/images/stories/downloads/sdn-resources/onf-specifications/openflow/openflow-spec-v1.3.0.pdf)
[OF Packet Format](http://archive.openflow.org/wk/images/c/c5/Openflow_packet_format.pdf)
[NOX(POX)](http://www.noxrepo.org/)
[POX wiki](https://openflow.stanford.edu/display/ONL/POX+Wiki)
[Ryu](https://osrg.github.io/ryu/)
[List](http://yuba.stanford.edu/~casado/of-sw.html)

Videos:
[Scott Shenker: why SDN](https://osrg.github.io/ryu/)


