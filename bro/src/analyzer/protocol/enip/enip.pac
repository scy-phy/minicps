%include binpac.pac
%include bro.pac

%extern{
#include "events.bif.h"
%}

analyzer ENIP withcontext {
	connection:	ENIP_Conn;
	flow:		ENIP_Flow;
};

%include enip-protocol.pac
%include enip-analyzer.pac