from __future__ import annotations
from abc import ABC, abstractmethod
from protocol_machines.cmina.messages.sim_pnio_dcp import *
from getmac import get_mac_address
import scapy.all as scapy
from scapy.contrib.pnio_dcp import *
from scapy.contrib.pnio import *
import time

scapy.load_contrib("pnio_dcp")
scapy.load_contrib("pnio")

# the context class contains a _state that references the concrete state and setState method to change between states.
class Device:

    _state = None

    def __init__(self, state: CMINAState, iface: str, mac_address: str = "") -> None:
        self.setState(state)
        self.iface = iface
        self.mac_address = mac_address
        self.name = ""
        self.ip = ""

    def setState(self, state: CMINAState):

        print(f"CMINA: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def getState(self):
        return self._state

    # State Methods
    def abort(self):
        self._state.abort()

    def identify(self, name):
        return self._state.identify(name)

    def setName(self, name):
        return self._state.setName(name)

    def setIp(self, ip):
        return self._state.setIp(ip)

    def reset(self): 
        return self._state.reset()

    # Service Methods
    def resetDevice(self):
        print("RESET DEVICE")
        self.mac_address = ""
        self.name = ""
        self.ip = ""

    def initDevice(self, name, mac):
        print("INIT DEVICE", name, mac)
        self.name = name
        self.mac_address = mac

    def setDeviceName(self, name):
        self.name = name

    def setDeviceIp(self, ip):
        self.ip = ip

    def getDeviceName(self):
        return self.name

    def getDeviceIp(self):
        return self.ip

    def getDeviceMac(self):
        return self.mac_address


class CMINAState(ABC):
    @property
    def context(self) -> Device:
        return self._context

    @context.setter
    def context(self, context: Device) -> None:
        self._context = context

    @abstractmethod
    def abort(self) -> None:
        pass

    @abstractmethod
    def identify(self, name) -> str:
        pass

    @abstractmethod
    def setName(self, name) -> bool:
        pass

    @abstractmethod
    def setIp(self, ip) -> bool:
        pass

    @abstractmethod
    def reset(self) -> bool:
        pass

class CMINAIdentifyState(CMINAState):
    def abort(self) -> None:
        return

    def identify(self, name) -> str:
        # Send identify message, and wait for response:
        mac_address_src = get_mac_address()
        ident_msg = get_ident_msg(src=mac_address_src, name_of_station=name)
        ans, _ = scapy.srp(
            ident_msg, iface=self.context.iface, timeout=1, multi=True, verbose=False
        )
        # PROBLEM: EVERY DEVICE RESPONDS, MULTIPLE DEVICES WILL RESPOND TO THIS MESSAGE
        dst_mac_address = ans[-1].answer["Ethernet"].src

        if dst_mac_address == mac_address_src or len(ans) < 2:
            # error:
            # set state to set_name with name
            self.context.resetDevice()
            return ""
        else:
            # success:
            # set state to identified
            self.context.setState(CMINAIdentifiedState())
            # self.context.initDevice(name, dst_mac_address)
            return dst_mac_address

    def setName(self, name) -> bool:
        # send identify
        # self.context.identify()
        # if isinstance(self.context.getState(), IdentifiedState):
        #     return self.context.setName(name)
        # else:
        #     self.abort()
        #     return False

        # If above is not allowed
        return False

    def setIp(self, ip) -> bool:
        # send identify
        # self.context.identify()
        # if isinstance(self.context.getState(), IdentifiedState):
        #     return self.context.setIp(ip, name)
        # else:
        #     self.abort()
        #     return False

        # If above is not allowed
        return False

    def reset(self) -> bool: 
        mac_address_src = get_mac_address()
        ident_msg = get_reset_factory_msg(src=mac_address_src, dst=self.context.getDeviceMac())
        ans, _ = scapy.srp(
            ident_msg, iface=self.context.iface, timeout=1, multi=True, verbose=False
        )
        self.context.resetDevice()
        ans[-1].answer.show()


class CMINAIdentifiedState(CMINAState):
    def abort(self) -> None:
        self.context.resetDevice()
        self.context.setState(CMINAIdentifyState())

    def identify(self) -> str:
        return self.context.getDeviceMac()

    def setName(self, name) -> bool:
        self.context.setState(CMINASetNameState())
        return self.context.setName(name)

    def setIp(self, ip) -> bool:
        self.context.setState(CMINAArpState())
        return self.context.setIp(ip)

    def reset(self) -> bool: 
        self.context.setStateCMINA(CMINAIdentifyState())
        return self.context.reset()



class CMINASetNameState(CMINAState):
    def abort(self) -> None:
        self.context.resetDevice()
        self.context.setState(CMINAIdentifyState())

    def identify(self, name) -> str:
        return self.context.getDeviceMac()

    def setName(self, name) -> bool:
        ident_msg = get_set_name_msg(
            src=get_mac_address(), name_of_station=name, dst=self.context.mac_address
        )
        ans, _ = scapy.srp(
            ident_msg, iface=self.context.iface, timeout=1, multi=True, verbose=False
        )
        set_name_rsp = ans[-1].answer
        if not set_name_rsp.haslayer("Profinet DCP"):
            self.abort()
            return False

        dcp_pkt = set_name_rsp["Profinet DCP"]

        # DCP_SERVICE_TYPE = 0x01: "Response Success"
        # DCP_SERVICE_ID = 0x04: "Set"
        if dcp_pkt.service_type != 0x01 or dcp_pkt.service_id != 0x04:
            self.abort()
            return False

        self.context.setDeviceName(name)
        self.context.setState(CMINAIdentifiedState())
        return True

    def setIp(self, ip) -> bool:
        self.context.setState(CMINAArpState())
        return self.context.setIp(ip)

    def reset(self) -> bool: 
        self.context.setState(CMINAIdentifyState())
        return self.context.reset()


class SetIpState(CMINAState):
    def abort(self) -> None:
        self.context.resetDevice()
        self.context.setState(CMINAIdentifyState())

    def identify(self, name) -> str:
        return self.context.getDeviceMac()

    def setName(self, name) -> bool:
        self.context.setState(CMINASetNameState())
        return self.context.setName(name)

    def setIp(self, ip) -> bool:
        set_ip_msg = get_set_ip_msg(
            src=get_mac_address(), dst=self.context.getDeviceMac(), ip=ip
        )
        ans, _ = scapy.srp(
            set_ip_msg, iface=self.context.iface, timeout=1, multi=True, verbose=False
        )

        ip_rsp = ans[-1].answer
        if not ip_rsp.haslayer("Profinet DCP"):
            self.abort()
            return False
        dcp_pkt = ip_rsp["Profinet DCP"]

        # DCP_SERVICE_TYPE = 0x01: "Response Success"
        # DCP_SERVICE_ID = 0x04: "Set"
        if dcp_pkt.service_type != 0x01 or dcp_pkt.service_id != 0x04:
            self.abort()
            return False

        self.context.setDeviceIp(ip)
        self.context.setState(CMINAIdentifiedState())
        return True
    
    def reset(self) -> bool: 
        self.context.setState(CMINAIdentifyState())
        return self.context.reset()


class CMINAArpState(CMINAState):
    def abort(self) -> None:
        self.context.setState(CMINAIdentifyState())

    def identify(self) -> str:
        return self.context.getDeviceMac()

    def setName(self, name) -> bool:
        self.context.setState(CMINASetNameState())
        return self.context.setName(name)

    def setIp(self, ip) -> bool:
        # arp request
        arp_request_broadcast = get_check_arp_ip(ip)
        answered_list = scapy.srp(
            arp_request_broadcast, timeout=3, verbose=False, iface=self.context.iface
        )[0]
        if len(answered_list) == 0:
            self.context.setState(SetIpState())
            return self.context.setIp(ip)
        else:
            self.context.setState(CMINAIdentifiedState())
            return False

    def reset(self) -> bool: 
        self.context.setState(CMINAIdentifyState())
        return self.context.reset()
