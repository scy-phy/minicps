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

# Find OSAL library. This module supports three use-cases:
#
# 1) OSAL sibling project
#
# If a target named OSAL exists then this module does nothing. This
# would be the case if OSAL is managed by a superproject.
#
# 2) External OSAL
#
# Search for and use an external OSAL. CMake will find the external
# OSAL library if it is installed in a default location such as
# /usr/include or /usr/local/include. You can also give a search hint
# by setting the Osal_DIR variable. This could be the case for a
# native build or a cross-compiled Linux system with a staging folder.
#
# 3) Automatic download and build of OSAL
#
# Finally, if OSAL is not found in the system it will be downloaded
# and built automatically.

cmake_minimum_required(VERSION 3.14)

if (NOT TARGET osal)
  # Attempt to find externally built OSAL
  find_package(Osal QUIET)

  if (NOT Osal_FOUND)
    # Download and build OSAL locally as a static library
    include(FetchContent)
    FetchContent_Declare(
      osal
      GIT_REPOSITORY      https://github.com/rtlabs-com/osal.git
      GIT_TAG             88784fc
      )
    FetchContent_GetProperties(osal)
    if(NOT osal_POPULATED)
      FetchContent_Populate(osal)
      set(BUILD_SHARED_LIBS_OLD ${BUILD_SHARED_LIBS})
      set(BUILD_SHARED_LIBS OFF CACHE INTERNAL "" FORCE)
      add_subdirectory(${osal_SOURCE_DIR} ${osal_BINARY_DIR} EXCLUDE_FROM_ALL)
      set(BUILD_SHARED_LIBS ${BUILD_SHARED_LIBS_OLD} CACHE BOOL "" FORCE)
    endif()

    # Hide Osal_DIR to avoid confusion, as it is not used in this
    # configuration
    mark_as_advanced(Osal_DIR)
  endif()
endif()
