#!/bin/bash

# $1 error.log path
# $2 ip address of the server
# $3 tags list

enip_server -p -l $1 -a $2 $3 &
