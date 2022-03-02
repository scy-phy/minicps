#********************************************************************
#        _       _         _
#  _ __ | |_  _ | |  __ _ | |__   ___
# | '__|| __|(_)| | / _` || '_ \ / __|
# | |   | |_  _ | || (_| || |_) |\__ \
# |_|    \__|(_)|_| \__,_||_.__/ |___/
#
# http://www.rt-labs.com
# Copyright 2017 rt-labs AB, Sweden.
# See LICENSE file in the project root for full license information.
#*******************************************************************/

find_package (SQLite3)

target_include_directories(pn_dev
  PRIVATE
  ${PROFINET_SOURCE_DIR}/src
  ${PROFINET_BINARY_DIR}/src
  )

include_directories(${SQLite3_INCLUDE_DIRS})

target_link_libraries (pn_dev PUBLIC profinet ${SQLite3_LIBRARIES})

install (TARGETS pn_dev DESTINATION bin)
