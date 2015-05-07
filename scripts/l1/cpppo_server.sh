#!/bin/bash

enip_server -p -l temp/l3-cppposerver.err -a 192.168.1.10 pump3=INT[10] flow3=INT[10] > temp/l3-cppposerver.out &

