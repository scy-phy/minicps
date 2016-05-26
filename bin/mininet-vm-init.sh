#!/bin/bash

# TODO: if not installed as module add minicps soft link to /usr/lib/python2.7

# TODO: add parametric installation
# mininet vm is running Ubuntu
cd

echo "Install required dependencies"
sudo apt-get install python-networkx python-matplotlib python-pip python-pil.imagetk
sudo apt-get install python-pymodbus
sudo pip install cpppo web.py

echo "Install optional dependencies"
sudo apt-get install python-nose python-sphinx python-coverage libjs-mathjax
sudo pip install pycomm nose-cov sphinx-rtd-theme

echo "Install additional tools"
sudo apt-get install zenmap wireshark elinks ettercap-graphical 
sudo apt-get install tmux ack-grep tree curl firefox htop
sudo apt-get install sqlite

# echo "Cloning repos"
# git clone https://github.com/mininet/mininet.git
# git clone https://github.com/noxrepo/pox.git
# git clone git@github.com:scy-phy/minicps.git

echo "Init pox"
python minicps/bin/pox_init.py

# TODO
# xserver otherwise no xterm and wireshark
# test nosetests, pox, ecc...

