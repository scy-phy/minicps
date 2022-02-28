from __future__ import annotations
from abc import ABC, abstractmethod
import uuid
import time 

from protocol_machines.ppm.helper.gsdml_parser import XMLDevice


class Provider:

    _state = None

    def __init__(self, state: PPMState, iface: str, device: object, dst_adr: str) -> None:
        self.setState(state)
        self.iface = iface
        self.device = device
        self.dst_adr = dst_adr
        self.output_data = []

    def setState(self, state: PPMState):

        print(f"CPM: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def getState(self):
        return self._state

    # State Methods
    def sendMsgs(self) -> bool:
        return self._state.sendMsgs()

    def stopMsgs(self) -> bool:
        return self._state.stopMsgs()

    # Service Methods
    # outputdata has following structure:
    # module_ident, submodule_ident, values[]
    def setOutputData(self, data) -> int:
        addedValues = 0
        for entry in data: 
            if self.checkEntryOfOutputData(entry):
                for existing_entry in self.output_data: 
                    if entry["module_ident"] == existing_entry["module_ident"] and entry["submodule_ident"] == existing_entry["submodule_ident"]:
                        existing_entry["values"] = entry["values"]
                    else: 
                        self.output_data.append(entry)
                    addedValues += 1

        return addedValues

    def checkEntryOfOutputData(self, entry) -> bool:
        for module_item in self.device.body.dap_list[-1].usable_modules:
            if (
                entry["module_ident"] == module_item.module_ident_number
                and entry["submodule_ident"] == module_item.submodule_ident_number
                and module_item.output_length == len(entry["values"])
            ):
                return True

        return False


class PPMState(ABC):
    @property
    def context(self) -> Provider:
        return self._context

    @context.setter
    def context(self, context: Provider) -> None:
        self._context = context

    @abstractmethod
    def sendMsgs(self) -> bool:
        pass

    @abstractmethod
    def stopMsgs(self) -> bool:
        pass


def main():
    context = Provider(
        PPMIdleState(),
        iface="Ethernet",
        device=XMLDevice("./gsdml/test_project_2.xml"),
        dst_adr="01:80:c2:00:00:0e",
    )
    context.sendMsgs()
    time.sleep(5)
    context.stopMsgs()
    time.sleep(1)
    context.sendMsgs()      
    time.sleep(5)
    context.stopMsgs()

if __name__ == "__main__":
    main()
