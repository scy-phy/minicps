#!/bin/bash

# can be used for single read and write cmds
# --print to print to stdout
# -l $1 error.log path
# -a $2 ip address of the server
# $3
#    tagname to read from a scalar tag
#    tagname=value to wirte to scalar tag
#    tagname[index] to read from a vector tag
#    tagname[index]=value to wirte to a vector tag
#    tagname[1-3]=1,2,3 multiple write on a vector tag
#    tagname1 tagname[1-3]=1,2,3 read and write
# $4 output.log path

# enip_client --print -l $1 -a $2 $3 | tee -a $4
python -m cpppo.server.enip.client --print -l $1 -a $2 $3 | tee -a $4

# <tag>=<type>[<length>]   # eg. SCADA=INT[1000]

