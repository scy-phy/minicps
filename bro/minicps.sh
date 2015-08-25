#!/bin/bash
files="scripts/base/init-default.bro
src/analyzer/protocol/CMakeLists.txt
README.md
minicps.sh
"

dirs="
scripts/base/protocols/enip/
scripts/policy/protocols/enip/
src/analyzer/protocol/enip/
testing/btest/scripts/base/protocols/enip/
testing/btest/Baseline/scripts.base.protocols.enip.*/
testing/btest/Traces/enip/
"

minicps="../minicps/bro/"

for varname in $files
do
    cpy=$minicps$varname
    cp $varname $cpy
done

for varname in $dirs
do
    rm -f $varname*~
    mkdir -p $minicps$varname
    cpy=$minicps$varname..
    cp -r $varname $cpy
done
