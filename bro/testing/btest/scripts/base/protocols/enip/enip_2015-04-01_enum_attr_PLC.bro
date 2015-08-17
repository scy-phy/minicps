#
# @TEST-EXEC: bro -r $TRACES/enip/enip_2015-04-01_enum_attr_PLC.pcapng %DIR/events.bro > output
# @TEST-EXEC: btest-diff output
# @TEST-EXEC: cat output | awk '{print $1}' | sort | uniq | wc -l > covered
# @TEST-EXEC: cat ${DIST}/src/analyzer/protocol/enip/events.bif | grep "^event enip_" | wc -l > total
# @TEST-EXEC: echo `cat covered` of `cat total` events triggered by trace > coverage
# @TEST-EXEC: btest-diff coverage
# @TEST-EXEC: btest-diff enip.log
#