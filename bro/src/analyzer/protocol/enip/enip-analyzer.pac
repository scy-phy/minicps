%header{
	RecordVal* HeaderToBro(ENIP_Header *header);
%}

%code{
	RecordVal* HeaderToBro(ENIP_Header *header){
		RecordVal* enip_header = new RecordVal(BifType::Record::EnipHeaders);
		enip_header->Assign(0, new Val(header->cmd(), TYPE_COUNT));
		enip_header->Assign(1, new Val(header->len(), TYPE_COUNT));
		enip_header->Assign(2, new Val(header->sh(), TYPE_COUNT));
		enip_header->Assign(3, new Val(header->st(), TYPE_COUNT));
		enip_header->Assign(4, bytestring_to_val(header->sc()));
		enip_header->Assign(5, new Val(header->opt(), TYPE_COUNT));
		return enip_header;
	}
%}

refine typeattr ENIP_PDU += &let {
	proc: bool = $context.flow.proc_enip_message(this);
};

refine connection ENIP_Conn += {
	%member{
		// Fields used to determine if the protocol has been confirmed or not.
		bool confirmed;
		bool orig_pdu;
		bool resp_pdu;
	%}

	%init{
		confirmed = false;
		orig_pdu = false;
		resp_pdu = false;
	%}

	function SetPDU(is_orig: bool): bool%{
		if( is_orig )
			orig_pdu = true;
		else
			resp_pdu = true;

		return true;
	%}

	function SetConfirmed(): bool%{
		confirmed = true;
		return true;
	%}

	function IsConfirmed(): bool%{
		return confirmed && orig_pdu && resp_pdu;
	%}
};

refine flow ENIP_Flow += {
	function proc_enip_message(msg: ENIP_PDU): bool%{
		BifEvent::generate_enip_event(connection()->bro_analyzer(), connection()->bro_analyzer()->Conn());
		return true;
	%}

	function deliver_message(header: ENIP_Header): bool%{
		if( ::enip_message ){
			BifEvent::generate_enip_message(connection()->bro_analyzer(),
			                                  connection()->bro_analyzer()->Conn(),
							  HeaderToBro(header),
			                                  is_orig());
		}

		return true;
	%}

	function deliver_ENIP_PDU(message: ENIP_PDU): bool%{
		// We will assume that if an entire PDU from both sides
		// is successfully parsed then this is definitely enip.
		connection()->SetPDU(${message.is_orig});

		if ( !connection()->IsConfirmed() ){
			connection()->SetConfirmed();
			connection()->bro_analyzer()->ProtocolConfirmation();
		}

		return true;
	%}

	function deliver_nop(header: ENIP_Header, message: Nop): bool%{
		if(::enip_nop){
			if(${header.cmd} == NOP){
				if(${header.st} != 0x00){
					connection()->bro_analyzer()->ProtocolViolation(
					fmt("invalid value for status in enip nop message %d", ${header.st}));
					return false;
				}
				if(${header.opt} != 0x00){
					connection()->bro_analyzer()->ProtocolViolation(
					fmt("invalid value for options in enip nop message %d", ${header.opt}));
					return false;
				}
			}
		BifEvent::generate_enip_nop(connection()->bro_analyzer(),
						connection()->bro_analyzer()->Conn(),
						HeaderToBro(header));
		}
		return true;
		%}

	function deliver_list_i_request(header: ENIP_Header): bool%{
		if(::enip_list_i_request){
			if(${header.cmd} == LIST_IDENTITY || ${header.cmd} == LIST_INTERFACES){
				if(${header.len} != 0x00){
					connection()->bro_analyzer()->ProtocolViolation(
					fmt("invalid value for length in enip list identity or interfaces message %d", ${header.len}));
					return false;
				}
				if(${header.st} != 0x00){
					connection()->bro_analyzer()->ProtocolViolation(
					fmt("invalid value for status in enip list identity or interfaces message %d", ${header.st}));
					return false;
				}
				if(${header.opt} != 0x00){
					connection()->bro_analyzer()->ProtocolViolation(
					fmt("invalid value for options in enip list identity or interfaces message %d", ${header.opt}));
					return false;
				}
				for(int i = 0; i < 8; i++){
					if(${header.sc}[i] != 0x00){
					connection()->bro_analyzer()->ProtocolViolation(
					fmt("invalid value for sender context in enip list identity or interfaces message %d", ${header.sc}[i]));
					return false;
					}
				}
			}
		}


		BifEvent::generate_enip_list_i_request(connection()->bro_analyzer(),
						connection()->bro_analyzer()->Conn(),
						HeaderToBro(header));
		return true;
		%}

	function deliver_list_services_request(header: ENIP_Header): bool%{
		if( ::enip_list_services_request ){
		    if(${header.cmd} == LIST_SERVICES){
			if(${header.len} != 0x00){
				connection()->bro_analyzer()->ProtocolViolation(
				fmt("invalid value for length in enip list services message %d", ${header.len}));
				return false;
			}
			if(${header.st} != 0x00){
				connection()->bro_analyzer()->ProtocolViolation(
				fmt("invalid value for status in enip list services message %d", ${header.st}));
				return false;
			}
			if(${header.opt} != 0x00){
				connection()->bro_analyzer()->ProtocolViolation(
				fmt("invalid value for options in enip list services message %d", ${header.opt}));
				return false;
			}
		    }
		}

		BifEvent::generate_enip_list_services_request(connection()->bro_analyzer(),
						connection()->bro_analyzer()->Conn(),
						HeaderToBro(header));
		return true;
		%}

		function deliver_Register_Request(header: ENIP_Header, message: Register_Request): bool%{
		if(${header.len} != 0x0400){
			connection()->bro_analyzer()->ProtocolViolation(
			    fmt("invalid value for enip length in register request %d", ${header.len}));
			return false;
		}
		if(${header.sh} != 0x0000000000){
			connection()->bro_analyzer()->ProtocolViolation(
			    fmt("invalid value for enip session handle in register request %d", ${header.sh}));
			return false;
		}
		if(${header.st} != 0x0000000000){
			connection()->bro_analyzer()->ProtocolViolation(
			    fmt("invalid value for enip status in register request %d", ${header.st}));
			return false;
		}
		if(${header.opt} != 0x0000000000){
			connection()->bro_analyzer()->ProtocolViolation(
			    fmt("invalid value for enip options in register request %d", ${header.opt}));
			return false;
		}


		if(${message.command_specific_data.protocol} != 0x0100){
			connection()->bro_analyzer()->ProtocolViolation(
			    fmt("invalid value for enip protocol version in register request %d", ${message.command_specific_data.protocol}));
			return false;
		}
		if(${message.command_specific_data.options} != 0x0000){
			connection()->bro_analyzer()->ProtocolViolation(
			    fmt("invalid value for enip protocol version in register request %d", ${message.command_specific_data.options}));
			return false;
		}

		if(::enip_register_request){
			BifEvent::generate_enip_register_request(connection()->bro_analyzer(),
			                                                   connection()->bro_analyzer()->Conn(),
			                                                   HeaderToBro(header),
									   ${message.command_specific_data.protocol},
									   ${message.command_specific_data.options});
		}
		return true;
		%}
};
