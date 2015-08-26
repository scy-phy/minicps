#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "You need to specify the Bro installation directory."
    echo "Usage: $0 </path/to/bro>"
    exit 1
fi

path=$1

files="scripts/test-all-policy.bro
scripts/base/init-default.bro
src/analyzer/protocol/CMakeLists.txt
README.md
install.sh
"

dirs="
scripts/base/protocols/enip/
scripts/policy/protocols/enip/
src/analyzer/protocol/enip/
testing/btest/scripts/base/protocols/enip/
testing/btest/Baseline/scripts.base.protocols.enip.*/
testing/btest/Traces/enip/
"

for varname in $dirs
do
    if [ ! -d $path$varname ]; then
	echo "Creating $path$varname."
	mkdir -p $path$varname
    fi
    cpy=$path$varname..
    echo "Copying files from $varname."
    cp -r $varname $cpy
done

for varname in $files
do
    cpy=$path$varname
    echo "Copying file $varname."
    cp $varname $cpy
done
