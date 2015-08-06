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
	LIST_SERVICES 	   	      = 0x0400,
	LIST_IDENTITY 	   	      = 0x6300,
	LIST_INTERFACES    	      = 0x6400, # Optional
	REGISTER_SESSION   	      = 0x6500,
	UNREGISTER_SESSION 	      = 0x6600,
	SEND_RR_DATA	   	      = 0x6F00,
	SEND_UNIT_DATA 	   	      = 0x7000,
	INDICATE_STATUS    	      = 0x7200, # Optional
	CANCEL 		   	      = 0x7300, # Optional
	# Other values are Reserved for future usage or Reserved for legacy
};

enum err_codes {
     	SUCCESS 		      = 0x0000,
	INVALID_UNSUPPORTED_CMD       = 0x0100,
	INSUFFICIENT_MEMORY	      = 0x0200,
	INCORRECT_DATA		      = 0x0300,
	INVALID_SESSION_HANDLE	      = 0x6400,
	INVALID_LENGTH		      = 0x6500,
	UNSUPPORTED_PROTOCOL_REVISION = 0x6900,
	# Other values are Reserved for future usage or Reserved for legacy
};

enum item_ID {
	ADDRESS				= 0x0000,
	LIST_IDENTITY_RESPONSE		= 0x0C00,
	CONNECTION_BASED		= 0xA100,
	CONNECTED_TRANSPORT_PACKET	= 0xB100,
	UNCONNECTED_MESSAGE		= 0xB200,
	LIST_SERVICES_RESPONSE		= 0x0001,
	SOCKADDR_INFO_O_T		= 0x0080,
	SOCKADDR_INFO_T_O		= 0x0180,
	SEQUENCED_ADDRESS_ITEM		= 0x0280,
	# Other values are Reserved for future usage or Reserved for legacy
}

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

type ENIP_PDU(is_orig: bool) = case is_orig of {
	true  -> request:  ENIP_Request;
	false -> response: ENIP_Response;
} &byteorder=bigendian;

type ENIP_Request = record {
	header: ENIP_Header;
	data: case(header.cmd) of {
		NOP 		   -> nop: 		 Nop;
		LIST_SERVICES 	   -> listServices: 	 List_Services;
		LIST_IDENTITY 	   -> listIdentity: 	 List_I;
		LIST_INTERFACES    -> listInterfaces: 	 List_I;
		REGISTER_SESSION   -> registerSession: 	 Register;
		UNREGISTER_SESSION -> unregisterSession: Register;
		SEND_RR_DATA 	   -> sendRRData: 	 RR_Unit(header);
		SEND_UNIT_DATA 	   -> sendUnitData: 	 RR_Unit(header);

		# All the rest
		default		   -> unknown:		 bytestring &restofdata;
	};
} &byteorder=bigendian;

type ENIP_Response = record {
	header: ENIP_Header;
	data: case(header.cmd) of {
		LIST_SERVICES 	   -> listServices: 	List_Services;
		LIST_IDENTITY 	   -> listIdentity: 	List_I;
		LIST_INTERFACES    -> listInterfaces: 	List_I;
		REGISTER_SESSION   -> registerSession: 	Register;
		SEND_RR_DATA 	   -> sendRRData: 	RR_Unit(header);

		# All the rest
		default		   -> unknown:		bytestring &restofdata;
	};
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
        protocol: uint16;
	options:  uint16;
} &byteorder=bigendian;

type RR_Unit(header: ENIP_Header) = record {
        iface_handle: uint32 &check(iface_handle == 0x00000000);
	timeout: uint16;
	data: Common_Packet_Format;
} &byteorder=bigendian;

type List_I = record {
        item_count: uint16;
	data: Target_Item[item_count];
} &byteorder=bigendian;

type List_Services = record {
        item_count: uint16;
	data: Target_Item_Services[item_count];
};

type UCMM = record {
      item_count: uint16;
	addr_type_ID: uint16;
	addr_len: uint16;
	data_type_ID: uint16;
	data_len: uint16;
	MR: uint8[data_len];
} &byteorder=bigendian;

# CIP Identity item ?

type sockaddr = record {
	sin_family: int16;
	sin_port: uint16;
	sin_addr: uint32;
	sin_zero: uint8[8];
};

type Nop = record {
        unused: bytestring &restofdata;
};

type List_Services_Request = record {
        unused: bytestring &restofdata;
};

type List_I_Request = record {
        unused: bytestring &restofdata;
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