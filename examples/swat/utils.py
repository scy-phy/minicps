"""
swat utils.

Network addresses, Common Industrial Protocol (CIP) and devices
"""

PLCS = 13
L1_NODES = 0  # TODO
L2_NODES = 0  # TODO
L3_NODES = 8

# NETWORK {{{1
L0_RING1 = {
    'plc': '192.168.0.10',
    'plcr': '192.168.0.11',
    'rio': '192.168.0.12',
    'rio_ap': '192.168.0.14',
    'sens_wifi_client': '192.168.0.15',
}

L0_RING2 = {
    'plc': '192.168.0.20',
    'plcr': '192.168.0.21',
    'rio': '192.168.0.22',
    'rio_ap': '192.168.0.24',
    'sens_wifi_client': '192.168.0.25',
}

L0_RING3 = {
    'plc': '192.168.0.30',
    'plcr': '192.168.0.31',
    'rio': '192.168.0.32',
    'rio_ap': '192.168.0.34',
    'sens_wifi_client': '192.168.0.35',
}

L0_RING4 = {
    'plc': '192.168.0.40',
    'plcr': '192.168.0.41',
    'rio': '192.168.0.42',
    'rio_ap': '192.168.0.44',
    'sens_wifi_client': '192.168.0.45',
}

L0_RING5 = {
    'plc': '192.168.0.50',
    'plcr': '192.168.0.51',
    'rio': '192.168.0.52',
    'rio_ap': '192.168.0.54',
    'sens_wifi_client': '192.168.0.55',
    'etap_vsd1': '192.168.0.56',
    'vsd1': '192.168.0.57',
    'etap_vsd2': '192.168.0.58',
    'vsd2': '192.168.0.59',
}

L0_RING6 = {
    'plc': '192.168.0.60',
    'plcr': '192.168.0.61',
    'rio': '192.168.0.62',
    'rio_ap': '192.168.0.64',
    'sens_wifi_client': '192.168.0.65',
}

L0_RING7 = {
    'plc': '192.168.0.70',
    'rio': '192.168.0.72',
    'rio_ap': '192.168.0.74',
    'sens_wifi_client': '192.168.0.75',
}

L1_PLCS_IP = {
    'plc1': '192.168.1.10',
    'plc2': '192.168.1.20',
    'plc3': '192.168.1.30',
    'plc4': '192.168.1.40',
    'plc5': '192.168.1.50',
    'plc6': '192.168.1.60',
    'plc1r': '192.168.1.11',
    'plc2r': '192.168.1.21',
    'plc3r': '192.168.1.31',
    'plc4r': '192.168.1.41',
    'plc5r': '192.168.1.51',
    'plc6r': '192.168.1.61',
    # used as central hub
    'plc7': '192.168.1.70',
    'attacker': '192.168.1.77',
}


L1_WIFI_CLIENTS_IP = {
    'c1': '192.168.1.12',
    'c2': '192.168.1.22',
    'c3': '192.168.1.32',
    'c4': '192.168.1.42',
    'c5': '192.168.1.52',
    'c6': '192.168.1.62',
    'c7': '192.168.1.72',
}

L2_HMI = {
    'hmi': '192.168.1.100',
    'wifi_client': '192.168.1.101',
}

CONDUITS = {
    'firewall': '192.168.1.102',
    'pcn_ap': '192.168.1.103',  # plant control network
    'dmz_ap': '192.168.1.104',
}

L3_PLANT_NETWORK = {
    'histn': '192.168.1.200',
    'workstn': '192.168.1.201',
}

L0_NETMASK = ''
L1_NETMASK = '/24'
L2_NETMASK = ''
L3_NETMASK = '/24'

PLCS_MAC = {
    'plc1': '00:1D:9C:C7:B0:70',
    'plc2': '00:1D:9C:C8:BC:46',
    'plc3': '00:1D:9C:C8:BD:F2',
    'plc4': '00:1D:9C:C7:FA:2C',
    'plc5': '00:1D:9C:C8:BC:2F',
    'plc6': '00:1D:9C:C7:FA:2D',
    'plc1r': '00:1D:9C:C8:BD:E7',
    'plc2r': '00:1D:9C:C8:BD:0D',
    'plc3r': '00:1D:9C:C7:F8:3B',
    'plc4r': '00:1D:9C:C8:BC:31',
    'plc5r': '00:1D:9C:C8:F4:B9',
    'plc6r': '00:1D:9C:C8:F5:DB',
    'plc7': 'TODO',
}


OTHER_MACS = {
    'histn': 'B8:2A:72:D7:B0:EC',
    'workstn': '98:90:96:98:CC:49',
    'hmi': '00:1D:9C:C6:72:E8',
    'attacker': 'AA:AA:AA:AA:AA:AA',  # easy to recognize in the capture
}

IPS_TO_MACS = {
    # plcs
    '192.168.1.10': '00:1D:9C:C7:B0:70',
    '192.168.1.20': '00:1D:9C:C8:BC:46',
    '192.168.1.30': '00:1D:9C:C8:BD:F2',
    '192.168.1.40': '00:1D:9C:C7:FA:2C',
    '192.168.1.50': '00:1D:9C:C8:BC:2F',
    '192.168.1.60': '00:1D:9C:C7:FA:2D',
    '192.168.1.11': '00:1D:9C:C8:BD:E7',
    '192.168.1.21': '00:1D:9C:C8:BD:0D',
    '192.168.1.31': '00:1D:9C:C7:F8:3B',
    '192.168.1.41': '00:1D:9C:C8:BC:31',
    '192.168.1.51': '00:1D:9C:C8:F4:B9',
    '192.168.1.61': '00:1D:9C:C8:F5:DB',
    # hist and workstn
    '192.168.1.200': 'B8:2A:72:D7:B0:EC',
    '192.168.1.201': '98:90:96:98:CC:49',
    # hmi
    '192.168.1.100': '00:1D:9C:C6:72:E8',
}



CIP_VENDOR_IDS = {
    'plc1': 'TODO',
    'plc2': 'TODO',
    'plc3': 'TODO',
    'plc4': 'TODO',
    'plc5': 'TODO',
    'plc6': 'TODO',
    'plc1r': 'TODO',
    'plc2r': 'TODO',
    'plc3r': 'TODO',
    'plc4r': 'TODO',
    'plc5r': 'TODO',
    'plc6r': 'TODO',
    'plc7': 'TODO',
    'attacker': 'TODO',
}

CIP_SERIAL_NUMBERS = {
    'plc1': 'TODO',
    'plc2': 'TODO',
    'plc3': 'TODO',
    'plc4': 'TODO',
    'plc5': 'TODO',
    'plc6': 'TODO',
    'plc1r': 'TODO',
    'plc2r': 'TODO',
    'plc3r': 'TODO',
    'plc4r': 'TODO',
    'plc5r': 'TODO',
    'plc6r': 'TODO',
    'plc7': 'TODO',
    'attacker': 'TODO',
}
