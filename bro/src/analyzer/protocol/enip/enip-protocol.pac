#
# Useful reference for specs: http://odva.org/
#
# Bro's ENIP analyser
#

##############################
#         CONSTANTS          #
##############################

enum cmd_codes {
        NOP                           = 0x0000,
	LIST_SERVICES 	   	      = 0x0004,
	LIST_IDENTITY 	   	      = 0x0063,
	LIST_INTERFACES    	      = 0x0064, # Optional
	REGISTER_SESSION   	      = 0x0065,
	UNREGISTER_SESSION 	      = 0x0066,
	SEND_RR_DATA	   	      = 0x006F,
	SEND_UNIT_DATA 	   	      = 0x0070,
	INDICATE_STATUS    	      = 0x0072, # Optional
	CANCEL 		   	      = 0x0073, # Optional
	# Other values are Reserved for future usage or Reserved for legacy
};

enum err_codes {
     	SUCCESS 		      = 0x0000,
	INVALID_UNSUPPORTED_CMD       = 0x0001,
	INSUFFICIENT_MEMORY	      = 0x0002,
	INCORRECT_DATA		      = 0x0003,
	INVALID_SESSION_HANDLE	      = 0x0064,
	INVALID_LENGTH		      = 0x0065,
	UNSUPPORTED_PROTOCOL_REVISION = 0x0069,
	# Other values are Reserved for future usage or Reserved for legacy
};

##############################
#        RECORD TYPES        #
##############################

type ENIP_Header = record {
	cmd: uint16; 		     # Command identifier
	len: uint16; 		     # Length of everyting (header + data)
	sh:  uint32; 		     # Session handle
	st:  uint32; 		     # Status
	sc:  bytestring &length = 8; # Sender context
	opt: uint32;		     # Option flags
} &byteorder=bigendian;

type ENIP_PDU(is_orig: bool) = record {
	header: ENIP_Header;
	data: 	case is_orig of {
		     true  -> request:  ENIP_Request(header);
		     false -> response: ENIP_Response(header);
	};
} &byteorder=bigendian;

type Target_Item = record {
        type_code: uint16;
	len: uint16;
	data: bytestring &length=len;
};

type Target_Item_Services = record {
        type_code: uint16;
	len: uint16;
	protocol: uint16;
	flags: uint16;
        name: uint8[16];
};

type Command_Specific_Data(header: ENIP_Header) = record {
        item_count: uint16;
	items: case header.cmd of {
	          LIST_INTERFACES -> interface:    Target_Item;
		  LIST_IDENTITY   -> identity:     Target_Item;
		  LIST_SERVICES   -> service: 	   Target_Item_Services;
		  default	  -> item:    	   Target_Item;
	};
};

type RR_Unit = record {
        iface_handle: uint32 &check(iface_handle == 0x00000000);
	timeout: uint16;
	data: bytestring &restofdata;
};

type Register = record {
        protocol: uint16 &check(protocol == 0x0100);
	options:  uint16 &check(options  == 0x0000);
};

type Data_Address = record {
        id: uint16;
	len: uint16;
	data: bytestring &length=len;
};

type Common_Packet_Format = record {
        count: uint16;
	address: Data_Address;
	data: Data_Address;
};

type UCMM = record {
        item_count: uint16;
	addr_type_ID: uint16;
	addr_len: uint16;
	data_type_ID: uint16;
	data_len: uint16;
	MR: uint8[data_len];
};

type Unused_data = record {
        unused: bytestring &restofdata;
};

type ENIP_Request(header: ENIP_Header) = case header.cmd of {
        NOP 		   -> nop: 		 Unused_data;
	LIST_SERVICES 	   -> listServices: 	 Unused_data;
	LIST_IDENTITY 	   -> listIdentity: 	 Unused_data;
	LIST_INTERFACES    -> listInterfaces: 	 Unused_data;
	REGISTER_SESSION   -> registerSession: 	 Register;
	UNREGISTER_SESSION -> unregisterSession: Register;
	SEND_RR_DATA 	   -> sendRRData: 	 RR_Unit;
	SEND_UNIT_DATA 	   -> sendUnitData: 	 RR_Unit;

	# All the rest
	default		   -> unknown:		 bytestring &restofdata;
};

type ENIP_Response(header: ENIP_Header) = case header.cmd of {
	LIST_SERVICES 	   -> listServices: 	 Command_Specific_Data(header);
	LIST_IDENTITY 	   -> listIdentity: 	 Command_Specific_Data(header);
	LIST_INTERFACES    -> listInterfaces: 	 Command_Specific_Data(header);
	REGISTER_SESSION   -> registerSession: 	 Register;
	SEND_RR_DATA 	   -> sendRRData: 	 RR_Unit;

	# All the rest
	default		   -> unknown:		 bytestring &restofdata;
};