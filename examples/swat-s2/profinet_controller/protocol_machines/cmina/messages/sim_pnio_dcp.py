import scapy.all as scapy
from scapy.contrib.pnio_dcp import *
from scapy.contrib.pnio import *
import time

scapy.load_contrib("pnio_dcp")
scapy.load_contrib("pnio")


def get_ident_msg(src, name_of_station):
    ether = scapy.Ether(dst="01:0e:cf:00:00:00", src=src, type=0x8892)
    pnio_msg = ProfinetIO(frameID=DCP_IDENTIFY_REQUEST_FRAME_ID)

    if name_of_station == "":
        dcp_data_length = 0
    else:
        dcp_data_length = len(name_of_station)
        +(5 if len(name_of_station) % 2 == 1 else 4)

    pnio_dcp_ident = ProfinetDCP(
        service_id=DCP_SERVICE_ID_IDENTIFY,
        service_type=DCP_REQUEST,
        xid=0x9A,
        reserved=1,
        dcp_data_length=dcp_data_length,  # if set 0, all devices with no name answer
        option=0x02,
        sub_option=0x02,
        dcp_block_length=len(name_of_station),
        name_of_station=name_of_station,
    )
    return ether / pnio_msg / pnio_dcp_ident


def get_set_ip_msg(src, dst, ip, netmask="255.255.255.0", gateway="0.0.0.0"):
    ether = scapy.Ether(dst=dst, src=src, type=0x8892)

    pnio_msg = ProfinetIO(frameID=0xFEFD)

    pnio_dcp_set_ip = ProfinetDCP(
        service_id=0x04,
        service_type=DCP_REQUEST,
        xid=0x04,
        reserved=0,
        dcp_data_length=18,
        option=0x01,
        sub_option=0x02,
        dcp_block_length=14,
        block_qualifier=0x0000,
        ip=ip,
        netmask=netmask,
        gateway=gateway,
    )

    return ether / pnio_msg / pnio_dcp_set_ip


def get_reset_factory_msg(src, dst):
    ether = scapy.Ether(dst=dst, src=src, type=0x8892)

    pnio_msg = ProfinetIO(frameID=0xFEFD)

    pnio_dcp_set_ip = ProfinetDCP(
        service_id=0x04,
        service_type=DCP_REQUEST,
        xid=0x04,
        reserved=0,
        dcp_data_length=6,
        option=0x05,
        sub_option=0x06,
        dcp_block_length=2,
    )

    return ether / pnio_msg / pnio_dcp_set_ip


def get_set_name_msg(
    src, dst, name_of_station, netmask="255.255.255.0", gateway="0.0.0.0"
):
    ether = scapy.Ether(dst=dst, src=src, type=0x8892)

    pnio_msg = ProfinetIO(frameID=0xFEFD)

    pnio_dcp_set_ip = ProfinetDCP(
        service_id=0x04,
        service_type=DCP_REQUEST,
        xid=0x04,
        reserved=0,
        dcp_data_length=len(name_of_station)
        + (9 if len(name_of_station) % 2 == 1 else 8),
        option=0x02,
        sub_option=0x02,
        dcp_block_length=len(name_of_station)
        + 2,  # TODO calculate the dcp blocklength, not sure if correct
        block_qualifier=0x0000,
        name_of_station=name_of_station,
        netmask=netmask,
        gateway=gateway,
    )

    return ether / pnio_msg / pnio_dcp_set_ip


def get_check_arp_ip(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    return broadcast / arp_request
