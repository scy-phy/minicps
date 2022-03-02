#********************************************************************
#        _       _         _
#  _ __ | |_  _ | |  __ _ | |__   ___
# | '__|| __|(_)| | / _` || '_ \ / __|
# | |   | |_  _ | || (_| || |_) |\__ \
# |_|    \__|(_)|_| \__,_||_.__/ |___/
#
# www.rt-labs.com
# Copyright 2021 rt-labs AB, Sweden.
#
# This software is licensed under the terms of the BSD 3-clause
# license. See the file LICENSE distributed with this software for
# full license information.
#*******************************************************************/

include_guard()
cmake_minimum_required (VERSION 3.1.2)
enable_language(ASM)

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

# Common flags
add_definitions(
  -fdata-sections
  -ffunction-sections
  )

# Common includes
list (APPEND INCLUDES
  # nothing yet
  )

set(CMAKE_ASM_STANDARD_INCLUDE_DIRECTORIES ${INCLUDES})
set(CMAKE_C_STANDARD_INCLUDE_DIRECTORIES ${INCLUDES})
set(CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES ${INCLUDES})

# Linker flags
add_link_options(
  -Wl,--gc-sections
  )

# Libraries
list (APPEND LIBS
  -lc
  -lm
  -lnosys
  )
list(JOIN LIBS " " LIBS) # Convert list to space separated string
set(CMAKE_C_STANDARD_LIBRARIES ${LIBS})
set(CMAKE_CXX_STANDARD_LIBRARIES "${LIBS} -lstdc++")

# Macro to add .bin output
macro(generate_bin TARGET)
  add_custom_command(TARGET ${TARGET} POST_BUILD
    COMMAND ${OBJCOPY}
    ARGS -O binary ${TARGET}.elf ${TARGET}.bin
    )
endmacro()
