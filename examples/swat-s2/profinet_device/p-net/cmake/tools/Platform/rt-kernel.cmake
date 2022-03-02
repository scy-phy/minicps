#********************************************************************
#        _       _         _
#  _ __ | |_  _ | |  __ _ | |__   ___
# | '__|| __|(_)| | / _` || '_ \ / __|
# | |   | |_  _ | || (_| || |_) |\__ \
# |_|    \__|(_)|_| \__,_||_.__/ |___/
#
# www.rt-labs.com
# Copyright 2017 rt-labs AB, Sweden.
#
# This software is licensed under the terms of the BSD 3-clause
# license. See the file LICENSE distributed with this software for
# full license information.
#*******************************************************************/

include_guard()
cmake_minimum_required (VERSION 3.1.2)

# Avoid warning when re-running cmake
set(DUMMY ${CMAKE_TOOLCHAIN_FILE})

# No support for shared libs
set_property(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS FALSE)

set(UNIX 1)
set(CMAKE_STATIC_LIBRARY_PREFIX "lib")
set(CMAKE_STATIC_LIBRARY_SUFFIX ".a")
set(CMAKE_EXECUTABLE_SUFFIX ".elf")

# Do not build executables during configuration stage. Required
# libraries may not be built yet.
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

# Prefer standard extensions
set(CMAKE_C_OUTPUT_EXTENSION_REPLACE 1)
set(CMAKE_CXX_OUTPUT_EXTENSION_REPLACE 1)
set(CMAKE_ASM_OUTPUT_EXTENSION_REPLACE 1)

# Add machine-specific flags
add_definitions(${MACHINE})
add_link_options(${MACHINE})

if (NOT ${VARIANT} STREQUAL "")
  add_definitions(-D${VARIANT})
endif()

# Common flags
add_definitions(
  -ffunction-sections
  -fomit-frame-pointer
  -fno-strict-aliasing
  -fshort-wchar
  )

# Common includes
list (APPEND INCLUDES
  ${RTK}/bsp/${BSP}/include
  ${RTK}/include
  ${RTK}/include/arch/${ARCH}
  ${RTK}/lwip/src/include
  )
set(CMAKE_ASM_STANDARD_INCLUDE_DIRECTORIES ${INCLUDES})
set(CMAKE_C_STANDARD_INCLUDE_DIRECTORIES ${INCLUDES})
set(CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES ${INCLUDES})

# Linker flags
add_link_options(
  -nostartfiles
  -L${RTK}/lib/${ARCH}/${VARIANT}/${CPU}
  -T${RTK}/bsp/${BSP}/${BSP}.ld
  -Wl,--gc-sections
  )

# Libraries
list (APPEND LIBS
  -l${BSP}
  -l${ARCH}
  -lkern
  -ldev
  -lsio
  -lblock
  -lfs
  -lusb
  -llwip
  -lptpd
  -leth
  -li2c
  -lrtc
  -lcan
  -lnand
  -lspi
  -lnor
  -lpwm
  -ladc
  -ldac
  -ltrace
  -lcounter
  -lshell
  -llua
  -lc
  -lm
  )
list(JOIN LIBS " " LIBS) # Convert list to space separated string
set(CMAKE_C_STANDARD_LIBRARIES ${LIBS})
set(CMAKE_CXX_STANDARD_LIBRARIES "${LIBS} -lstdc++")

# Group libraries when linking

set(CMAKE_C_LINK_EXECUTABLE "<CMAKE_C_COMPILER> <FLAGS> <CMAKE_C_LINK_FLAGS> <LINK_FLAGS> <OBJECTS> -o <TARGET> -Wl,--start-group <LINK_LIBRARIES> -Wl,--end-group")

set(CMAKE_CXX_LINK_EXECUTABLE "<CMAKE_CXX_COMPILER> <FLAGS> <CMAKE_CXX_LINK_FLAGS> <LINK_FLAGS> <OBJECTS> -o <TARGET> -Wl,--start-group <LINK_LIBRARIES> -Wl,--end-group")
