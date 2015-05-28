#!/bin/bash

# can be used for single read and write cmds
# $1 error.log path
# $2 ip address of the server
# $3 tagname[index] to read
#    tagname[index]=value to write
# $4 output.log path

enip_client -p -l $1 -a $2 $3 | tee -a $4

