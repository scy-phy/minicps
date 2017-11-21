# s317-minicps

* info
    * 1 session
    * **begin: 6th May 9 AM Singapore time**
    * **end: 7th May 9 AM Singapore time**
    * 10 teams
        * 10 different public IP
        * reuse same shared keys
        * reuse same webapp credentials

* channels
    * kopipackets
    * IRC

* keep in mind
    * Arxiv paper is available (no reuse)
    * If challenges are too simular then players from last year might be advantaged
    * Challenge has to be hard but realistic
    * OpenVPN round trip time will bi higher

## Init

If the first vm is configured correctly then after the duplication
you only need to do the following steps:

* `tmux ls` and attach to the admin session
* rename the admin session to `teamx`
* type `make`
* change `EC2_IP` in the `Makefile`
* test `make start` with the new IP
* change `openvpn-rclient.conf` `remote` to `$EC2_IP`
* change `openvpn-rclient2.conf` `remote` to `$EC2_IP`
* test openvpn connections cd into `teamx` folder

Additional checks:

* `sudo iptables -L -t nat`
* minicps version and branch
* port 8080 open for the webapp
* port 1337 redirected to 10.0.0.1:1194
* port 1338 redirected to 10.0.0.2:1194
* `sudo ls /root/flags`

If some file or software is missing, see `init.sh`.

Provided files to each team

    README.md
    attacker-password
    openvpn-rclient.conf
    openvpn-rclient2.conf
    static.key
    static2.key

See `init.sh`


Check new enip minicps branch:

    git checkout -b remmihsorp-feature/enip2 master
    git pull https://github.com/remmihsorp/minicps.git feature/enip2

Generate shared openvpn key:

    openvpn --genkey --secret static.key
    openvpn --genkey --secret static2.key


Temporary ipv4 forwarding:

    cat /proc/sys/net/ipv4/ip_forward
    sudo su
    echo 1 > /proc/sys/net/ipv4/ip_forward
    exit

Persistent ipv4 forwarding:

    sudo vim /etc/sysctl.conf:
    net.ipv4.ip_forward = 1


* ettercap
    * installation from source
        * `sudo apt-get install debhelper cmake bison flex libgtk2.0-dev
            libltdl3-dev libncurses-dev libncurses5-dev\
             libnet1-dev libpcap-dev libpcre3-dev libssl-dev
             libcurl4-openssl-dev ghostscript`
        * download source file and look at INSTALL file

* etterfilters
    * as ubuntu user
    * `cd ~/s3/online/enip`
    * `make etterfilters`
    * copy the relevant `.ec` file to the relevant location

* bettercap
    * install stable `rvm` with ruby `2.4.1` for simple user
    * `gem install packetfu -v 1.1.11`
    * `git clone https://github.com/evilsocket/bettercap`
    * `cd bettercap`
    * `gem build bettercap.gemspec`
    * `gem install bettercap*.gem`
    * run with `rvmsudo bettercap`



## OpenVPN

* Links
    * https://openvpn.net/index.php/open-source/documentation
    * https://wiki.archlinux.org/index.php/OpenVPN
    * https://wiki.archlinux.org/index.php/Easy-RSA

* Debian packages
    * `sudo apt-get install openvpn easy-rsa`
    * openvpn version 2.4.1

* Actual setup
    * tcp
    * Generate a shared secret key for client-server
        * https://openvpn.net/index.php/open-source/documentation/miscellaneous/78-static-key-mini-howto.html
    * Configure openvpn to use `tap` (bridging, transports L2 traffic eg: ARP)
        * https://openvpn.net/index.php/open-source/documentation/miscellaneous/76-ethernet-bridging.html#linuxscript
    * Disable host service at startup
        * `sudo vim /etc/default/openvpn`
        * uncomment `#AUTOSTART="none"`
        * check with `sudo service openvpn status`


## Wadi challenges

### 1: Coil Width Modulation (CWM) scheme

* TODO
    * check round trip time with openvpn
    * attacker might miss some bits

* Description
    * New secure modulation scheme: Coil Width Modulation (CWM)
    * `rtu2a` periodically send data using this modulation scheme `scada`
      using offset 0 and no encryption
    * The encoding scheme used is ASCII (Eg: 8-bit to represent one character)

* Goal
    * Test man-in-the-middle, synch, ASCII decoding.

* How
    * Send an `ettercap` command

### 2: Three-Holding Registers Width Modulation (3-HRWM) scheme

* Description
    * The `rtu2b` is using internally (without sending traffic into the
        network) a faster and more secure modulation scheme the 3-HRWM
    * The scheme uses 3 holding registers (offset from 0 to 2) and a clever offset
        hopping technique to prevent eavesdropping.
    * The hopping techniques uses 4 masks and each mask is applied to 3
        sequences of 3 bytes (Eg: if the mask is 0-1-2 then the first 3
        sequences will send the three bytes in natural order).
    * Each register contains an ASCII encoded character (Eg: 8-bit to
        represent one character
    * Please try to speak with `rtu2b` to get the flag

* Goal
    * Test Modbus/TCP client that reads multiple registers in parallel.

* How
    * Write modbus tcp client


## Runtime checks

Mixed challenge ping map:

    *** Ping: testing ping reachability
    │
    attacker -> X client X X X X X X
    │
    attacker2 -> X X client2 X X X X X
    │
    client -> attacker X X plc2 plc3 X X X
    │
    client2 -> X attacker2 X X X rtu2a rtu2b scada
    │
    plc2 -> attacker X X X plc3 X X X
    │
    plc3 -> attacker X X X plc2 X X X
    │
    rtu2a -> X attacker2 X X X X rtu2b scada
    │
    rtu2b -> X attacker2 X X X X rtu2a scada
    │
    scada -> X attacker2 X X X X rtu2a rtu2b

* flask webapp status
    * http://blog.luisrei.com/articles/flaskrest.html

* tcpdump single interface to a file
    * `sudo tcpdump -i tap0 -w /tmp/tap0.pcap &`

* tcpdump all interfaces to a file
    * `sudo tcpdump -i any -w /tmp/any.pcap &`
    * Linux cooked interface no ether headers

* check interface status
    * `watch ifconfig ifname`

* check open ports
    * `sudo netstat -tulpn`
    * `nmap localhost`

* check services
    * `sudo service --status-all`
    * `sudo service service_name status`
    * you may need to restart openvswitch switch server
    * type `w` to check who is logged in

* check flags
    * TODO

* start challenges
    * `cd ~/s317-minicps/mix`
    * `make run`
    * from another terminal `make start`

* clean and restart
    * `make restart`

* stop and clean
    * `make stop`

* log file
    * `tail -f /var/log/commands.log`

