connection ENIP_Conn(bro_analyzer: BroAnalyzer) {
	upflow   = ENIP_Flow(true);
	downflow = ENIP_Flow(false);
};

%header{
	#define SIZE 8
%}

flow ENIP_Flow(is_orig: bool) {
	datagram = ENIP_PDU(is_orig) withcontext(connection, this);
	# flowunit

	function enip_header(cmd: uint16, len: uint16, sh: uint32, st: uint32, sc: bytestring, opt: uint32): bool%{
		if(::enip_header){
			VectorVal* sclist = new VectorVal(internal_type("index_vec")->AsVectorType());

			for(unsigned int i = 0; i < SIZE; ++i)
				sclist->Assign(i, new Val(sc[i], TYPE_COUNT));

			BifEvent::generate_enip_header(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), cmd, len, sh, st, sclist, opt);
		}

		return true;
	%}

	function enip_data_address(id: uint16, len: uint16, data: bytestring): bool%{
		if(::enip_data_address){
			VectorVal* data_val = new VectorVal(internal_type("index_vec")->AsVectorType());

			for(unsigned int i = 0; i < len; ++i)
				data_val->Assign(i, new Val(data[i], TYPE_COUNT));

			BifEvent::generate_enip_data_address(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), id, len, data_val);
		}

		return true;
	%}

	function enip_common_packet_format(count: uint16): bool%{
		if(::enip_common_packet_format){
			BifEvent::generate_enip_common_packet_format(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), count);
		}

		return true;
	%}

	function enip_target_item(type_code: uint16, len: uint16): bool%{
		if(::enip_target_item){
			BifEvent::generate_enip_target_item(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), type_code, len);
		}

		return true;
	%}

	function enip_target_item_services(type_code: uint16, len: uint16, protocol: uint16, flags: uint16): bool%{
		//TODO name: uint8[]
		if(::enip_target_item_services){
			// VectorVal* name_val = new VectorVal(internal_type("index_vec")->AsVectorType());

			// for(unsigned int i = 0; i < 16; ++i)
			// 	name_val->Assign(i, new Val(name, TYPE_COUNT));

			BifEvent::generate_enip_target_item_services(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), type_code, len, protocol, flags);
		}

		return true;
	%}

	function enip_register(protocol: uint16, options: uint16): bool%{
		if(::enip_register){
			BifEvent::generate_enip_register(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), protocol, options);
		}

		return true;
	%}

	function enip_rr_unit(iface_handle: uint32, timeout: uint16): bool%{
		if(::enip_rr_unit){
			BifEvent::generate_enip_rr_unit(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), iface_handle, timeout);
		}

		return true;
	%}

	function enip_list(item_count: uint16): bool%{
		if(::enip_list){
			BifEvent::generate_enip_list(
				connection()->bro_analyzer(),
				connection()->bro_analyzer()->Conn(),
				is_orig(), item_count);
		}

		return true;
	%}
};

refine typeattr ENIP_Header += &let {
	enip_header: bool = $context.flow.enip_header(cmd, len, sh, st, sc, opt);
};

refine typeattr Data_Address += &let {
	enip_data_address: bool = $context.flow.enip_data_address(id, len, data);
};

refine typeattr Common_Packet_Format += &let {
	enip_common_packet_format: bool = $context.flow.enip_common_packet_format(count);
};

refine typeattr Target_Item += &let {
	enip_target_item: bool = $context.flow.enip_target_item(type_code, len);
};

refine typeattr Target_Item_Services += &let {
	enip_target_item_services: bool = $context.flow.enip_target_item_services(type_code, len, protocol, flags);
};

refine typeattr Register += &let {
	enip_register: bool = $context.flow.enip_register(protocol, options);
};

refine typeattr RR_Unit += &let {
	enip_rr_unit: bool = $context.flow.enip_rr_unit(iface_handle, timeout);
};

refine typeattr List_I += &let {
	enip_list: bool = $context.flow.enip_list(item_count);
};

refine typeattr List_Services += &let {
	enip_list: bool = $context.flow.enip_list(item_count);
};