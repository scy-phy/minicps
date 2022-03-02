#********************************************************************
#        _       _         _
#  _ __ | |_  _ | |  __ _ | |__   ___
# | '__|| __|(_)| | / _` || '_ \ / __|
# | |   | |_  _ | || (_| || |_) |\__ \
# |_|    \__|(_)|_| \__,_||_.__/ |___/
#
# www.rt-labs.com
# Copyright 2020 rt-labs AB, Sweden.
#
# This software is licensed under the terms of the BSD 3-clause
# license. See the file LICENSE distributed with this software for
# full license information.
#*******************************************************************/

# Get git revision if available, as projectname_GIT_REVISION

find_package(Git QUIET)
execute_process(COMMAND
  "${GIT_EXECUTABLE}" describe --tags --always --dirty
  WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  OUTPUT_VARIABLE "${CMAKE_PROJECT_NAME}_GIT_REVISION"
  ERROR_QUIET
  OUTPUT_STRIP_TRAILING_WHITESPACE
  )
