#!/bin/bash

echo "Starting from home"
cd /home/ubuntu

echo "Installing required deb packages"
sudo apt install openvpn easy-rsa bridge-utils python-pip tree htop wireshark \
ettercap-graphical build-essential libssl-dev libffi-dev python-dev zenmap \
tmux ranger tig ipython iptables-persistent gitk
echo "... Ok"

echo "Installing mininet 2.2.2"
git clone https://github.com/mininet/mininet
cd mininet
git checkout 2.2.2
util/install.sh -a
cd /home/ubuntu
echo "... Ok"

echo "Testing mininet 2.2.2"
sudo mn --test pingall
echo "... Ok"

echo "Installing required pip packages"
sudo pip install flask nose rednose requests
echo "... Ok"

echo "Symlinking  minicps, installing requirements, checkout to enipserver branch"
git clone https://github.com/scy-phy/minicps.git
sudo ln -s /home/ubuntu/minicps/minicps /usr/lib/python2.7/minicps
cd minicps
sudo pip install -r requirements.txt
git checkout -b remmihsorp-feature/enip2 master
git pull https://github.com/remmihsorp/minicps.git feature/enip2
cd /home/ubuntu
echo "... Ok"

echo "Testing minicps protocols"
cd minicps
make test-protocols
cd /home/ubuntu
echo "... Ok"

echo "Cloning s317-minicps repo"
git clone https://github.com/scy-phy/s317-minicps
echo "... Ok"

echo "Symlinking enipserver and using a stable commit"
git clone https://github.com/scy-phy/enipserver.git
sudo ln -s /home/ubuntu/enipserver/enipserver /usr/lib/python3.5/enipserver
ls -la /usr/lib/python3.5/enipserver
cd enipserver
git checkout 2e7dc936e9647985af2a7151f72be2b77deed32c
cd /home/ubuntu
echo "... Ok"

echo "Symlinking pycomm fork"
git clone https://github.com/remmihsorp/pycomm.git
sudo ln -s /home/ubuntu/pycomm/pycomm /usr/lib/python2.7/pycomm
ls -la /usr/lib/python2.7/pycomm
cd pycomm
git checkout 1b1199062bb957d6b24572349f07f487376af738
cd /home/ubuntu
echo "... Ok"

echo "Configuring vimrc"
cp s317-minicps/vimrc ~/.vimrc
echo "... Ok"

echo "Configuring tmux"
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
cp s317-minicps/tmux.conf ~/.tmux.conf
echo "... Ok"

echo "Check the flag files: flag2, flag3, readme2, readme3, wadi1, wadi2"
sudo ls /root/flags
cd /home/ubuntu
echo "... Ok"

cd /home/ubuntu


echo "Please manually check iptables rules and their persistence."
echo "Please manually checkout to minicps remmina branch."
echo "Please manually check that 8080, 1337 and 1338 are opened."
echo "Please run C-b u in tmux and change the theme."
