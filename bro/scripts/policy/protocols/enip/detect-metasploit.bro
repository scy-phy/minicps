module ENIP;

export {
	redef enum Notice::Type += {
		## Indicates a host trying to crash PLCs.
		ENIP::Metasploit,
	};

	const STOPCPU_payload = vector(0x52, 0x02, 0x20, 0x06, 0x24, 0x01, 0x03, 0xf0, 0x0c, 0x00, 0x07, 0x02, 0x20, 0x64, 0x24, 0x01, 0xDE, 0xAD, 0xBE, 0xEF, 0xCA, 0xFE, 0x01, 0x00, 0x01, 0x00);

	const CRASHCPU_len = 0x000C;
	const CRASHCPU_opt = 0x000C00B2;
	const CRASHCPU_context = vector(0x20, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00);

	const CRASHETHER_len = 0x001A;
	const CRASHETHER_opt = 0x001A00B2;
	const CRASHETHER_context = vector(0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00);

	const RESETETHER_len = 0x0008;
	const RESETETHER_opt = 0x000800B2;
	const RESETETHER_context = vector(0x00, 0x04, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00);
}

event enip_data_address(c: connection, is_orig: bool, id: count, len: count, data: index_vec){
	local stopcpu = T;

	if(len == |STOPCPU_payload|){
		for(i in data){
			if(data[i] != STOPCPU_payload[i]){
				stopcpu = F;
				break;
			}
		}
		if(stopcpu){
			NOTICE([$note=ENIP::Metasploit,
				$conn=c,
				$msg=fmt("Possible usage of STOPCPU attack from Metasploit ethernet_multi module.")]);
		}
	}
}

event enip_header(c: connection, is_orig: bool, cmd: count, len: count, sh: count, st: count, sc: index_vec, opt: count){
      local attack = T;

      if(len == CRASHCPU_len && opt == CRASHCPU_opt){
	     for(i in sc){
			if(sc[i] != CRASHCPU_context[i]){
				attack = F;
				break;
			}
		}
		if(attack){
			NOTICE([$note=ENIP::Metasploit,
				$conn=c,
				$msg=fmt("Possible usage of CRASHCPU attack from Metasploit ethernet_multi module.")]);
		}
	}else if(len == CRASHETHER_len && opt == CRASHETHER_opt){
	     for(i in sc){
			if(sc[i] != CRASHETHER_context[i]){
				attack = F;
				break;
			}
		}
		if(attack){
			NOTICE([$note=ENIP::Metasploit,
				$conn=c,
				$msg=fmt("Possible usage of CRASHETHER attack from Metasploit ethernet_multi module.")]);
		}
	}else if(len == RESETETHER_len && opt == RESETETHER_opt){
	     for(i in sc){
			if(sc[i] != RESETETHER_context[i]){
				attack = F;
				break;
			}
		}
		if(attack){
			NOTICE([$note=ENIP::Metasploit,
				$conn=c,
				$msg=fmt("Possible usage of RESETETHER attack from Metasploit ethernet_multi module.")]);
		}
	}
}