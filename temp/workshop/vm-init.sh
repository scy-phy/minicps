#!/bin/bash

# commands used to init mininet Ubuntu servers

sudo apt-get install zenmap wireshark elinks ettercap-graphical python-nose python-matplotlib python-pip python-sphinx curl

sudo pip install pycomm cpppo nose-cov

cd
git clone https://github.com/mininet/mininet.git
git clone https://github.com/noxrepo/pox.git
git clone git@github.com:scy-phy/minicps.git

python minicps/scripts/pox/init.py -m ~/minicps

# TODO
# xserver otherwise no xterm and wireshark
# test nosetests, pox, ecc...

