##! Implements base functionality for ethernet-ip analysis.
##! Generates the Enip.log file.

module Enip;

@load ./consts

export {
	redef enum Log::ID += { LOG };

	type Info: record {
		## Timestamp for when the event happened.
		ts:     time    &log;
		## Unique ID for the connection.
		uid:    string  &log;
		## The connection's 4-tuple of endpoint addresses/ports.
		id:     conn_id &log;

		## The name of the ENIP command that was sent.
		command:	string	&log &optional;
		## The status.
		status:	string	&log &optional;
	};

	## Event that can be handled to access the enip record as it is sent on
	## to the loggin framework.
	global log_enip: event(rec: Info);
}

redef record connection += {
	enip: Info &optional;
};

const ports = { 44818/tcp, 44818/udp };
redef likely_server_ports += { ports };

event bro_init() &priority=5{
	Log::create_stream(Enip::LOG, [$columns=Info, $ev=log_enip, $path="enip"]);
	Analyzer::register_for_ports(Analyzer::ANALYZER_ENIP, ports);
}

event enip_header(c: connection, is_orig: bool, cmd: count, len: count, sh: count, st: count, sc: index_vec, opt: count){
	if(!c?$enip){
		c$enip = [$ts=network_time(), $uid=c$uid, $id=c$id];
	}
	c$enip$ts = network_time();
	c$enip$command = commands[cmd];
	c$enip$status = status[st];
}