##! Implements base functionality for EtherNet/IP analysis.
##! Generates the enip.log file, containing some information about the ENIP headers.

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

		## Name of the sent ENIP command.
		command:	string	&log &optional;
		## Length of the ENIP packet.
		length:		count	&log &optional;
		## LOL
		session_handler: count &log &optional;
		## Status of the command.
		status:	string	&log &optional;
		## LOL
		sender_context: index_vec &log &optional;
		## LOL
		options: count &log &optional;
	};

	## Event that can be handled to access the enip record as it is sent on
	## to the loggin framework.
	global log_enip: event(rec: Info);
}

redef record connection += {
	enip: Info &optional;
};

const ports = { 44818/tcp, 44818/udp, 2222/udp, 2222/tcp };
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
	c$enip$length = len;
	c$enip$session_handler = sh;
	c$enip$status = status[st];
	c$enip$sender_context = sc; # Useless, always 0
	c$enip$options = opt;	    # Useless, always 0

	Log::write(LOG, c$enip);
}

event connection_state_remove(c: connection) &priority=-5{
	if(!c?$enip)
		return;

	Log::write(LOG, c$enip);
	delete c$enip;
}