"""
minicps constants.

L0 rings are isolated dicts.

L1 network devices are divided into dicts according to the device type.
"""


L0_RING1 = {
    'plc': '192.168.0.10',
    'plcr': '192.168.0.11',
    'rio': 'TODO',
    'act1': 'TODO',
    'sen1': 'TODO',
    'ap': 'TODO',
    'wireless_rio': 'TODO',
}

L0_RING2 = {
    'plc': '192.168.0.20',
    'plcr': '192.168.0.21',
}

L0_RING3 = {
    'plc': '192.168.0.30',
    'plcr': '192.168.0.31',
}

L0_RING4 = {
    'plc': '192.168.0.40',
    'plcr': '192.168.0.41',
}

L0_RING5 = {
    'plc': '192.168.0.50',
    'plcr': '192.168.0.51',
}

L0_RING6 = {
    'plc': '192.168.0.60',
    'plcr': '192.168.0.61',
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
}

L1_APS_IP = {
    'ap1': 'TODO',  # MOXA
    'ap2': 'TODO',
    'ap3': 'TODO',
    'ap4': 'TODO',
    'ap5': 'TODO',
    'ap6': 'TODO',
    'ap_control_network': 'TODO',  # SCADA and Historian
    'ap_hmi': 'TODO',
}

L3_SCADA = {
}

L3_Historian = {
}

L2_HMI = {
}


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
}
PLCS = len(PLCS_MAC)

APS_MAC = {
    'ap1': 'TODO',  # MOXA
    'ap2': 'TODO',
    'ap3': 'TODO',
    'ap4': 'TODO',
    'ap5': 'TODO',
    'ap6': 'TODO',
    'ap_control_network': 'TODO',  # SCADA and Historian
    'ap_hmi': 'TODO',
}
APS = len(APS_MAC)

