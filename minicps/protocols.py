"""
protocols.py.

Ethernet/IP (ENIP) is partially supported using cpppo module
https://github.com/pjkundert/cpppo

Modbus/TCP.
"""

import cpppo

# ENIP {{{1

ENIP_MISC = {
    'tcp_port': 44818,
    'udp_port': 2222,
}
