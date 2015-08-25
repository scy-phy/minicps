module Enip;

export {
       ## ENIP default commands
       const commands = {
       	     [0x0000] = "NOP",
       	     [0x0004] = "LIST_SERVICES",
       	     [0x0063] = "LIST_IDENTITY",
	     [0x0064] = "LIST_INTERFACES",
       	     [0x0065] = "REGISTER_SESSION",
       	     [0x0066] = "UNREGISTER_SESSION",
       	     [0x006F] = "SEND_RR_DATA",
       	     [0x0070] = "SEND_UNIT_DATA",
       	     [0x0072] = "INDICATE_STATUS",
       	     [0x0073] = "CANCEL",
       } &default=function(i: count):string { return fmt("unknown-%d", i); } &redef;

       ## ENIP default errors
       const status {
       	     [0x0000] = "SUCCESS",
       	     [0x0001] = "INVALID_UNSUPPORTED_CMD",
       	     [0x0002] = "INSUFFICIENT_MEMORY",
       	     [0x0003] = "INCORRECT_DATA",
       	     [0x0064] = "INVALID_SESSION_HANDLE",
       	     [0x0065] = "INVALID_LENGTH",
       	     [0x0069] = "UNSUPPORTED_PROTOCOL_REVISION",
       } &default=function(i: count):string { return fmt("unknown-%d", i); } &redef;

       ## ENIP default IDs
       const ID {
       	     [0x0000] = "ADDRESS",
       	     [0x000C] = "LIST_IDENTITY_RESPONSE",
       	     [0x00A1] = "CONNECTION_BASED",
       	     [0x00B1] = "CONNECTED_TRANSPORT_PACKET",
       	     [0x00B2] = "UNCONNECTED_MESSAGE",
       	     [0x0100] = "LIST_SERVICES_RESPONSE",
       	     [0x8000] = "SOCKADDR_INFO_O_T",
       	     [0x8001] = "SOCKADDR_INFO_T_O",
       	     [0x8002] = "SEQUENCED_ADDRESS_ITEM",
       } &default=function(i: count):string { return fmt("unknown-%d", i); } &redef;
}