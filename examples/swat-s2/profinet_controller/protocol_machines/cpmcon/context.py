from __future__ import annotations
from abc import ABC, abstractmethod
import uuid

from protocol_machines.cpmcon.helper.gsdml_parser import XMLDevice

from protocol_machines.cpmcon.states import *


class Connection:

    _state = None

    def __init__(
        self, state: CPMCONState, iface: str, device: object, auuid: str
    ) -> None:
        self.setState(state)
        self.iface = iface
        self.device = device
        self.ip = ""
        # self.auuid = str(uuid.uuid4())
        self.auuid = auuid

    def setState(self, state: CPMCONState):

        print(f"CPMCON: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def getState(self):
        return self._state

    # State Methods
    def abort(self) -> None:
        self._state.abort()

    def connect(self, ip) -> bool:
        self._state.connect(ip)

    def write(self, parameterList) -> bool:
        self._state.write(parameterList)

    def announceEndPrm(self) -> bool:
        self._state.announceEndPrm()

    def ackApplicationReady(self) -> bool:
        self._state.ackApplicationReady()

    # Service Methods


class CPMCONState(ABC):
    @property
    def context(self) -> Connection:
        return self._context

    @context.setter
    def context(self, context: Connection) -> None:
        self._context = context

    @abstractmethod
    def abort(self) -> None:
        pass

    @abstractmethod
    def connect(self, ip) -> bool:
        pass

    @abstractmethod
    def write(self, parameterList) -> bool:
        pass

    @abstractmethod
    def announceEndPrm(self) -> bool:
        pass

    @abstractmethod
    def ackApplicationReady(self) -> bool:
        pass


def main():
    context = Connection(
        CPMCONConnectState(),
        iface="Ethernet",
        device=XMLDevice("./gsdml/test_project_2.xml"),
        auuid=str(uuid.uuid4()),
    )
    context.connect("192.168.178.155")
    context.write("test")
    context.announceEndPrm()
    context.ackApplicationReady()

    # time.sleep(20)

    # context.connect()
    # context.write("test")
    # context.announceEndPrm()
    # context.ackApplicationReady()


if __name__ == "__main__":
    main()
