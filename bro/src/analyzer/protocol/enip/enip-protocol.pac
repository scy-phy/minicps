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

# All multiple byte fields are set in little endian order
# Packets are set in big endian order

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
	data: Common_Packet_Format[len];
} &byteorder=bigendian;

type Target_Item_Services = record {
        type_code: uint16;
	len: uint16;
	protocol: uint16;
	flags: uint16;
        name: uint8[16];
} &byteorder=bigendian;

type Register = record {
        protocol: uint16 &check(protocol == 0x0100);
	options:  uint16 &check(options  == 0x0000);
} &byteorder=bigendian;

type Data_Address = record {
        id: uint16;
	len: uint16;
	data: bytestring &length=len;
} &byteorder=bigendian;

type Data_Item = record {
	address: Data_Address;
	data: Data_Address;
} &byteorder=bigendian;

type Common_Packet_Format = record {
        count: uint16;
	items: Data_Item[count];
} &byteorder=bigendian;

# type UCMM = record {
#       item_count: uint16;
# 	addr_type_ID: uint16;
# 	addr_len: uint16;
# 	data_type_ID: uint16;
# 	data_len: uint16;
# 	MR: uint8[data_len];
# } &byteorder=bigendian;

# CIP Identity item ?
# Socket Addr (all fields are set in bigendian order) ?

type ENIP_Request(header: ENIP_Header) = case header.cmd of {
        NOP 		   -> nop: 		 Nop;
	LIST_SERVICES 	   -> listServices: 	 List_Services_Request;
	LIST_IDENTITY 	   -> listIdentity: 	 List_I_Request;
	LIST_INTERFACES    -> listInterfaces: 	 List_I_Request;
	REGISTER_SESSION   -> registerSession: 	 Register_Request;
	UNREGISTER_SESSION -> unregisterSession: Unregister;
	SEND_RR_DATA 	   -> sendRRData: 	 Send_RR_Data_Request;
	SEND_UNIT_DATA 	   -> sendUnitData: 	 Send_Unit_Data_Request;

	# All the rest
	default		   -> unknown:		 bytestring &restofdata;
} &byteorder=bigendian;

type ENIP_Response(header: ENIP_Header) = case header.cmd of {
	LIST_SERVICES 	   -> listServices: 	 List_Services_Response;
	LIST_IDENTITY 	   -> listIdentity: 	 List_Identity_Response;
	LIST_INTERFACES    -> listInterfaces: 	 List_Interfaces_Response;
	REGISTER_SESSION   -> registerSession: 	 Register_Response;
	SEND_RR_DATA 	   -> sendRRData: 	 Send_RR_Data_Response;

	# All the rest
	default		   -> unknown:		 bytestring &restofdata;
} &byteorder=bigendian;

type Nop = record {
        unused: bytestring &restofdata;
};

type List_Services_Request = record {
        unused: bytestring &restofdata;
};

type List_I_Request = record {
        unused: bytestring &restofdata;
};

type Register_Request = record {
        protocol: uint16 &check(protocol == 0x0100);
	options:  uint16 &check(options  == 0x0000);
};

type Unregister = record {
        protocol: uint16 &check(protocol == 0x0100);
	options:  uint16 &check(options  == 0x0000);
};

type Send_RR_Data_Request = record {
        iface_handle: uint32 &check(iface_handle == 0x00000000);
	timeout: uint16;
	data: Common_Packet_Format;
};

type Send_Unit_Data_Request = record {
        iface_handle: uint32 &check(iface_handle == 0x00000000);
	timeout: uint16;
	data: Common_Packet_Format;
};

type List_Services_Response = record {
        item_count: uint16;
	data: Target_Item_Services[item_count];
};

type List_Interfaces_Response = record {
        item_count: uint16;
	data: Target_Item[item_count];
};

type List_Identity_Response = record {
        item_count: uint16;
	data: Target_Item[item_count];
};

type Register_Response = record {
        protocol: uint16 &check(protocol == 0x0100);
	options:  uint16 &check(options  == 0x0000);
};

type Send_RR_Data_Response = record {
        iface_handle: uint32 &check(iface_handle == 0x00000000);
	timeout: uint16;
	data: Common_Packet_Format;
};