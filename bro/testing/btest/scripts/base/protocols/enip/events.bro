#
# @TEST-EXEC: bro -r $TRACES/enip/enip_read_tags.pcapng %INPUT > output
# @TEST-EXEC: btest-diff output
# @TEST-EXEC: cat output | awk '{print $1}' | sort | uniq | wc -l > covered
# @TEST-EXEC: cat ${DIST}/src/analyzer/protocol/enip/events.bif | grep "^event enip_" | wc -l > total
# @TEST-EXEC: echo `cat covered` of `cat total` events triggered by trace > coverage
# @TEST-EXEC: btest-diff coverage
# @TEST-EXEC: btest-diff enip.log
#
event enip_header(c: connection, is_orig: bool, cmd: count, len: count, sh: count, st: count, sc: index_vec, opt: count){
      print "enip_header", is_orig, cmd, len, sh, st, sc, opt;
}

event enip_data_address(c: connection, is_orig: bool, id: count, len: count, data: index_vec){
      print "enip_data_address", is_orig, id, len, data;
}

event enip_common_packet_format(c: connection, is_orig: bool, item_count: count){
      print "enip_common_packet_format", is_orig, item_count;
}

event enip_target_item(c: connection, is_orig: bool, type_code: count, len: count){
      print "enip_target_item", is_orig, type_code, len;
}

event enip_target_item_services(c: connection, is_orig: bool, type_code: count, len: count, protocol: count, flags: count, name: index_vec){
      print "enip_target_item_services", is_orig, type_code, len, protocol, flags, name;
}

event enip_register(c: connection, is_orig: bool, protocol: count, options: count){
      print "enip_register", is_orig, protocol, options;
}

event enip_rr_unit(c: connection, is_orig: bool, iface_handle: count, time_out: count){
      print "enip_rr_unit", is_orig, iface_handle, time_out;
}

event enip_list(c: connection, is_orig: bool, item_count: count){
      print "enip_list", is_orig, item_count;
}