# MiniCPS #

MiniCPS is a lightweight simulator for accurate network traffic in an
industrial control system, with basic support for physical layer
interaction.

## Installation ##

We recommend the use of a mininet VM (http://mininet.org/download/) to
run minicps. Once the VM is set up, run the following to install the
environment:

    $ cd; mkdir scy-phy; cd scy-phy
    $ git clone https://github.com/scy-phy/minicps
    $ cd; git clone http://github.com/noxrepo/pox
    # apt-get install python-pip python-nose python-matplotlib python-networkx
    # pip install cpppo pycomm nose-cov

To symlink minicps pox controller to pox/ext execute the following
script. Notice that `POX_PATH` defaults to `~/pox` and `MINICPS_PATH`
defaults to `~/minicps`.

    $ ~/minicps/script/pox/init.py [-p POX_PATH -m MINICPS_PATH -vv]
    
In order to reduce the network traffic in an IPv4-only environment,
you can **disable** the Linux IPv6 kernel module:

    # vim /etc/default/grub

then add `ipv6.disable=1` as first parameter in the string.
Note that the `...` portion of the string depends on your grub config.

    GRUB_CMDLINE_LINUX_DEFAULT="ipv6.disable=1 ..."

then

    # update-grub

then reboot your machine and check it with `ifconfig` that no
`inet6` is listed.

Instruction taken from [here](https://github.com/mininet/mininet/issues/454).

## Testing ##

You can intentionally skip a particular test adding/uncommenting `raise SkipTest`.
You can see skipped test summary in the nosetests output.

If you want to run all the tests contained in the `topology_tests` module, type:

    # nosetests tests/topology_tests

To run a single test within a script use:

    # nosetests tests/topology_tests:test_name

use `-s` opt to prevent nosetests to capture stdout.

use `-v` opt to obtain a more verbose output.

You can even generate coverage report (read `$ nosetests --help`).

Every switch listens to `6634` default debugging port. You can change it via `OF_MISC` 
dict in the constants module.

## Ettercap ##

Open `/etc/ettercap/etter.conf`

Change user and group ids (nobody is the default):

    [privs]
    ec_uid = 0
    ec_gid = 0

If you use Linux's `iptables` uncomment:

    redir_command_on = "iptables -t nat -A PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport"
    redir_command_off = "iptables -t nat -D PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport"

## Logging ##

The relevant log files are stored in the `logs` dir.

Each minicps module and its associated testing module is managed by a dedicated `logging` obj,
You can tweak the number of backups file that are automatically rotating and their size, through
the `constants` module.

Each `scripts/pox/component` generate a separate logfile that is overwritten each time you run
a new `mininet` instance.

## Build html sphinx docs ##

Install `python-sphinx` and its dependencies. Install
[sphinx_rtd_theme](https://github.com/snide/sphinx_rtd_theme) or change the
`html_theme` in `docs/conf.py` then `cd` into `minicps/docs` and run

    $ make html

Then open `_build/html/index.html` and navigate the docs.

*Please proofread it and report any issue.*

## Misc ##

TODO: add dependency graph

Snakefood is a nice tool able to generate dependency graphs from Python source code. Take a look at
[it](http://furius.ca/snakefood/doc/snakefood-doc.html#introduction)

## Links ##

Sqlite3:

[SQL](https://www.sqlite.org/lang.html)

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

[Open vSwitch (OVS)](http://openvswitch.org/)

[OpenFlow wireshark support and wiki](https://wiki.wireshark.org/OpenFlow)

[OF Packet Format](http://archive.openflow.org/wk/images/c/c5/Openflow_packet_format.pdf)

[NOX(POX)](http://www.noxrepo.org/)

[POX wiki](https://openflow.stanford.edu/display/ONL/POX+Wiki)

[Ryu](https://osrg.github.io/ryu/)

[More software](http://yuba.stanford.edu/~casado/of-sw.html)

Videos:

[Scott Shenker: why SDN](https://osrg.github.io/ryu/)


