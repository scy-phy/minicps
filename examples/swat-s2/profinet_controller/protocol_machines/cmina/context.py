from __future__ import annotations
from abc import ABC, abstractmethod

from protocol_machines.cmina.states import *

# the context class contains a _state that references the concrete state and setState method to change between states.
class Device:

    _state = None

    def __init__(self, state: CMINAState, iface: str) -> None:
        self.setState(state)
        self.iface = iface
        self.mac_address = ""
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
        self.mac_address = ""
        self.name = ""
        self.ip = ""

    def initDevice(self, name, mac):
        self.name = name
        self.mac = mac

    def setDeviceName(self, name):
        self.name = name

    def setDeviceIp(self, ip):
        self.ip = ip

    def getDeviceName(self):
        return self.name

    def getDeviceIp(self):
        return self.ip

    def getDeviceMac(self):
        return self.mac


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

def main():
    context = Device(CMINAIdentifyState(), iface="Ethernet")
    context.identify("")
    context.setIp(ip="192.168.178.155")
    context.setName("rt-labs-dev")

if __name__ == "__main__":
    main()
