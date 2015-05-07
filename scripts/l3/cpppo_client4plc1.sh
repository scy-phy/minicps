#!/bin/bash

n=0
TIMES=5

while [[ $n -le $TIMES ]]; do
    enip_client -p -l temp/l3/cpppoclient.err -a 192.168.1.10 pump3[$n]=$n | tee -a temp/l3/cpppoclient.out
    sleep 1
    n=$((n+1))
done
