#!/bin/bash

# -l $1 error.log path
# -a $2 ip address of the server
# $3 tags list
#   tagname=TYPE[range]
#   scalar_tag=TYPE 
#   vector_tag=TYPE[range]
#   cpppo supported TYPES = INT(16-bit), SINT(8-bit),REAL(32-bit), DINT(32-bit)
# $4 output.log path

# enip_server -p -l $1 -a $2 $3 | tee -a $4 &
python -m cpppo.server.enip -p -l $1 -a $2 $3 | tee -a $4 &
