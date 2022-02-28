from __future__ import annotations
from abc import ABC, abstractmethod
import uuid
import time 
from profinet_controller.protocol_machines.ppm.helper.gsdml_parser import XMLDevice
from profinet_controller.protocol_machines.ppm.messages.pnio_ps import *
from getmac import get_mac_address
import scapy.all as scapy
from scapy.contrib.pnio import *
import time
import getmac

from state.SqliteState import SQLiteState

scapy.load_contrib("pnio")

class Provider:

    _state = None

    def __init__(self, state: PPMState, iface: str, device: object, dst_adr: str, dbState: SQLiteState) -> None:
        self.setState(state)
        self.iface = iface
        self.device = device
        self.dst_adr = dst_adr
        self.dbState= dbState
        self.output_data = []
        self.id = 1

    def setState(self, state: PPMState):

        print(f"PPM: Transitioning to {type(state).__name__}")
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
    def getOutputData(self) -> int:
        print([int(self.dbState._get(("DI8", self.id)))])
        return [
            {
                "module_ident": int(0x00000080),
                "submodule_ident": int(0x00000080),
                "values": [int(self.dbState._get(("DI8", self.id)))]
            },
            {
                "module_ident": int(0x00000100),
                "submodule_ident": int(0x00000100),
                "values": list(struct.pack("f", self.dbState._get(("DI32", self.id))))
            },
            {
                "module_ident": int(0x00000200),
                "submodule_ident": int(0x00000200),
                "values": list(struct.pack("d", self.dbState._get(("DI64", self.id))))
            },
        ]

        # for entry in data: 
        #     if self.checkEntryOfOutputData(entry):
        #         for existing_entry in self.output_data: 
        #             if entry["module_ident"] == existing_entry["module_ident"] and entry["submodule_ident"] == existing_entry["submodule_ident"]:
        #                 existing_entry["values"] = entry["values"]
        #             else: 
        #                 self.output_data.append(entry)
        #             addedValues += 1

        # return addedValues

    # def checkEntryOfOutputData(self, entry) -> bool:
    #     for module_item in self.device.body.dap_list[-1].usable_modules:
    #         if (
    #             entry["module_ident"] == module_item.module_ident_number
    #             and entry["submodule_ident"] == module_item.submodule_ident_number
    #             and module_item.output_length == len(entry["values"])
    #         ):
    #             return True

    #     return False


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

class PPMSendState(PPMState):
    def __init__(self) -> None:
        super().__init__()
        self.run = False
        self.thread = None

    # SEND CYLIC MESSAGES
    def send_messages(self):
        timer = 512
        counter = 0
        while True:
            if self.run:
                ps_msg = get_data_msg(
                    src=get_mac_address(),
                    dst=self.context.dst_adr,
                    counter=counter,
                    device=self.context.device,
                    data=self.context.getOutputData(),  # TODO how to get output data -> central database to fetch data
                    timer=timer,
                )
                sendp(ps_msg, iface=self.context.iface, verbose=False)
                counter += 1
                time.sleep(
                    timer / 1000
                )  # TODO Time should be adjusted to send time -> should be parameter in context class
            else:
                break

    def abort(self) -> None:
        self.context.setState(PPMIdleState())
        return

    def sendMsgs(self) -> bool:
        if not self.run:
            # start thread with sending msgs
            self.thread = threading.Thread(target=self.send_messages)
            self.run = True
            self.thread.start()
            return True
        else:
            return False

    def stopMsgs(self) -> bool:
        if self.run:
            # stop thread
            self.run = False
            self.thread.join()

        self.context.setState(PPMIdleState())
        return True


class PPMIdleState(PPMState):
    def abort(self) -> None:
        return

    def sendMsgs(self) -> bool:
        self.context.setState(PPMSendState())
        return self.context.sendMsgs()

    def stopMsgs(self) -> bool:
        return True
