#!/bin/bash

n=0
TIMES=5

while [[ $n -le $TIMES ]]; do
    enip_client -p -l tmp/cpppo-client.err \
        -a 192.168.1.10 pump3[$n]=$n | tee -a tmp/cpppo-client.out
    sleep 1
    n=$((n+1))
done
