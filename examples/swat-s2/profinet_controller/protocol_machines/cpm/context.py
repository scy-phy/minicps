from __future__ import annotations
from abc import ABC, abstractmethod
import uuid
import time

from profinet_controller.protocol_machines.cpm.states import *
from profinet_controller.protocol_machines.cpm.helper.gsdml_parser import XMLDevice


class Consumer:

    _state = None

    def __init__(self, state: CPMState, iface: str, device: object, dst_adr: str) -> None:
        self.setState(state)
        self.iface = iface
        self.device = device
        self.dst_adr = dst_adr

    def setState(self, state: CPMState):

        print(f"CPM: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def getState(self):
        return self._state

    # State Methods
    def receiveMsgs(self) -> bool:
        return self._state.receiveMsgs()

    def stopReceiveMsgs(self) -> bool:
        return self._state.stopReceiveMsgs()


class CPMState(ABC):
    @property
    def context(self) -> Consumer:
        return self._context

    @context.setter
    def context(self, context: Consumer) -> None:
        self._context = context

    @abstractmethod
    def receiveMsgs(self) -> bool:
        pass

    @abstractmethod
    def stopReceiveMsgs(self) -> bool:
        pass

    @abstractmethod
    def abort(self) -> None:
        pass


def main():
    context = Consumer(
        IdleState(),
        iface="Ethernet",
        device=XMLDevice("./gsdml/test_project_2.xml"),
        dst_adr="00:0c:29:95:78:31",
    )
    context.receiveMsgs()
    time.sleep(5)
    context.stopReceiveMsgs()
    time.sleep(1)
    context.receiveMsgs()
    time.sleep(5)
    context.stopReceiveMsgs()


if __name__ == "__main__":
    main()
