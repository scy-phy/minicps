#!/bin/bash

# mininet
sudo mn -c

# swat
sudo pkill  -u root -f "python -m cpppo.server.enip"

# wadi
sudo pkill  -u root -f "python /usr/lib/python2.7/minicps/pymodbus"

# others
sudo pkill openvpn
sudo pkill ettercap
