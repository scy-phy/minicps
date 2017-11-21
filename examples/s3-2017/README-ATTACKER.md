# s317 - MiniCPS challenges

Dear attackers,

This README file contains some basic information about the four presented
challenges.

Remember that the flag format is:

    s3flag{something here}

## Challenges

The four challenges are built using  MiniCPS: a framework for Cyber-Physical
Systems real-time simulation. Feel free to look at our
[repo](https://github.com/scy-phy/minicps) and at the
[docs](https://minicps.readthedocs.io/en/latest/?badge=latest)

The first two challenges involve the Ethernet/IP protocol and they are based
on a forked version of the [`pycomm`](https://github.com/ruscito/pycomm)

To use our fork of the module, first clone our repo:

    git clone https://github.com/remmihsorp/pycomm.git

Then add the module to your `python2` path.
For example, on a Linux machine you can create a soft link:

    sudo ln -s /home/your_username/pycomm/pycomm /usr/lib/python2.7/pycomm
    # make sure that the soft link is pointing to the correct folder
    ls -la /usr/lib/python2.7/pycomm

The last two challenges involve the Modbus protocol and they are based on the
[`pymodbus`](https://github.com/bashwork/pymodbus). Please follow the
instruction in the repo README to install the module for `python2`. For
example type

    sudo pip2 install -U pymodbus

Note that we did not test the challenges with the pymodbus module for `python3`.

## OpenVPN access

Each team is provided with two OpenVPN keys: `static.key` and `static2.key`.
The first key has to be used in combination with `rclient.conf` and the second
with `rclient2.conf` to get access to the different MiniCPS subnetworks.
You will find those files in the provided zip file.

The challenges are built using Linux `openvpn` servers, and they were tested
using Linux `openvpn` clients. For example, assuming that you download all the
required files in a folder with path `/path/to/files` to connect to first server
type:

    cd /path/to/files
    # this folder should contain two keys and two config files
    sudo openvpn openvpn-rclient.conf

Once the connection is established open another terminal and type:

    ifconfig

You should see a `tap0` interface that you can use to send packets.

To connect to the second openvpn server repeat the same steps using `openvpn-rclient2`
as argument for the `openvpn` command. In this case you will get a `tap1`
network interface. Hence, you can use both clients on the same machine :)

Note that, you are allowed to connect only one client at a time for each
openvpn server because we are using a symmetric private keys configuration.

## Web application interaction

We provide a simple, authenticated RESTful web API to *start*, *stop* and *restart*
the MiniCPS challenges. For example, assuming that the webapp is running on
public IP `54.169.210.123` listening on port `8080` and that your username
is `attacker` and your password is `password` then you can type:

    curl -u "attacker:password" http://54.169.210.123:8080/start
    curl -u "attacker:password" http://54.169.210.123:8080/stop
    curl -u "attacker:password" http://54.169.210.123:8080/restart

To start, stop and restart the challenges. For example, if the VPN connection
is not working you might restart the challenge and try to connect again. You
will find your `password` in the provided zip file. You have to substitute the
public IP in the `curl` commands with the one that you are using for the
remote connection of your openvpn client.

## Warnings

Please don't share the OpenVPN server remote IP with the other teams.

## Further help?

For any problem, please contact the challenge author mentioned in the
challenge webpage by email or trough IRC on freenode at `##s317`.

