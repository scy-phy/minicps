#!/bin/bash

sudo apt-get install zenmap wireshark elinks ettercap-graphical python-nose python-matplotlib python-pip

sudo pip install pycomm cpppo nose-cov

cd
git clone https://github.com/scy-phy/minicps.git
git clone https://github.com/mininet/mininet.git
git clone https://github.com/noxrepo/pox.git

python minicps/scripts/pox/init.py

# TODO
# xserver
# ssh access

