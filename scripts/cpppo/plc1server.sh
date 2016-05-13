#!/bin/bash

enip_server -p -l tmp/cpppo-server.err \
    -a 192.168.1.10 pump3=INT[10] flow3=INT[10] | tee -a tmp/cpppo-server.out &
