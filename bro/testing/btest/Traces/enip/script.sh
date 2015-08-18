#!/bin/bash

protocol=enip
extension=pcapng

test="# @TEST-EXEC: btest-diff output\n# @TEST-EXEC: cat output | awk '{print $1}' | sort | uniq | wc -l > covered\n# @TEST-EXEC: cat \${DIST}/src/analyzer/protocol/$protocol/events.bif | grep \"^event "$protocol"_\" | wc -l > total\n# @TEST-EXEC: echo \`cat covered\` of \`cat total\` events triggered by trace > coverage\n# @TEST-EXEC: btest-diff coverage\n# @TEST-EXEC: btest-diff $protocol.log\n#"

for i in $( ls ); do
    if [[ $i = *."$extension" ]]; then
	file=`echo $i| cut -d'.' -f 1`
	test0="#\n# @TEST-EXEC: bro -r \$TRACES/$protocol/$file.pcapng > output\n$test"
	echo -e $test0 > ../../scripts/base/protocols/enip/$file.bro
    fi
done
