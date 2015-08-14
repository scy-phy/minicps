module Enip;

export {
       ## ENIP default commands
       const commands = {
       	     [0x0000] = "NOP",
       	     [0x0400] = "LIST_SERVICES",
       	     [0x6300] = "LIST_IDENTITY",
	     [0x6400] = "LIST_INTERFACES",
       	     [0x6500] = "REGISTER_SESSION",
       	     [0x6600] = "UNREGISTER_SESSION",
       	     [0x6F00] = "SEND_RR_DATA",
       	     [0x7000]   = "SEND_UNIT_DATA",
       	     [0x7200]   = "INDICATE_STATUS",
       	     [0x7300]   = "CANCEL",
       } &default=function(i: count):string { return fmt("unknown-%d", i); } &redef;

       ## ENIP default errors
       const status {
       	     [0x0000] = "SUCCESS",
       	     [0x0100] = "INVALID_UNSUPPORTED_CMD",
       	     [0x0200] = "INSUFFICIENT_MEMORY",
       	     [0x0300] = "INCORRECT_DATA",
       	     [0x6400] = "INVALID_SESSION_HANDLE",
       	     [0x6500] = "INVALID_LENGTH",
       	     [0x6900] = "UNSUPPORTED_PROTOCOL_REVISION",
       } &default=function(i: count):string { return fmt("unknown-%d", i); } &redef;

       ## ENIP default IDs
       const ID {
       	     [0x0000] = "ADDRESS",
       	     [0x0C00] = "LIST_IDENTITY_RESPONSE",
       	     [0xA100] = "CONNECTION_BASED",
       	     [0xB100] = "CONNECTED_TRANSPORT_PACKET",
       	     [0xB200] = "UNCONNECTED_MESSAGE",
       	     [0x0001] = "LIST_SERVICES_RESPONSE",
       	     [0x0080] = "SOCKADDR_INFO_O_T",
       	     [0x0180] = "SOCKADDR_INFO_T_O",
       	     [0x0280] = "SEQUENCED_ADDRESS_ITEM",
       } &default=function(i: count):string { return fmt("unknown-%d", i); } &redef;
}