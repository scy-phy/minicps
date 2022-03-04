from __future__ import annotations
from abc import ABC, abstractmethod
from email import message
import netaddr

from numpy import float64
from protocol_machines.cpm.helper.gsdml_parser import XMLDevice
from protocol_machines.cpm.messages.pnio_ps import *
from getmac import get_mac_address
import scapy.all as scapy
from scapy.contrib.pnio import *
import time

from state.SqliteState import SQLiteState

scapy.load_contrib("pnio")


class Consumer:

    _state = None

    def __init__(
        self,
        state: CPMState,
        iface: str,
        device: object,
        dst_adr: str,
        dbState: SQLiteState,
    ) -> None:
        self.setState(state)
        self.iface = iface
        self.device = device
        self.dst_adr = dst_adr
        self.dbState = dbState
        self.id = 1

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


class CPMReceiveState(CPMState):
    def __init__(self) -> None:
        super().__init__()
        self.run = False
        self.thread = None

    def receive_messages(self):

        def update_load(pkt):
            if pkt.haslayer("PROFINET IO Real Time Cyclic Default Raw Data"):
                message_data = parse_data_message(pkt, self.context.device)
                self.context.dbState._set(
                    ("DO8", self.context.id), int(message_data.input_data["data"][0][0])
                )
                self.context.dbState._set(
                    ("DO32", self.context.id),
                    struct.unpack("f", bytearray(message_data.input_data["data"][1]))[
                        0
                    ],
                )
                self.context.dbState._set(
                    ("DO64", self.context.id),
                    struct.unpack("d", bytearray(message_data.input_data["data"][2]))[
                        0
                    ],
                )
                print(
                    "value DO32: ", self.context.dbState._get(("DO32", self.context.id))
                )

            elif pkt.haslayer("ProfinetIO"):
                # TODO: In Case of Alarm Message change state to IDLE and fire event
                # TODO: Maybe make network event queue, which transfers messages to right
                # State Machine, dependent on in which states the machines are
                data = pkt.getlayer("ProfinetIO")
                if data.frameID == 0xFE01:
                    print("ALARM LOW")
                    Alarm_Low(pkt[Raw].load).show()
                elif data.frameID == 0xFC01:
                    print("ALARM HIGH")
                    Alarm_High(pkt[Raw].load).show()

        def stop_filter(x):
            if self.run:
                return False
            else:
                return True


        sniff(
            filter=f'ether dst {self.context.dst_adr}',
            store=0,
            count=-1,
            prn=update_load,
            iface=self.context.iface,
            stop_filter=stop_filter,
        )

    def abort(self) -> None:
        self.context.setState(CPMIdleState())
        return

    def receiveMsgs(self) -> bool:
        if not self.run:
            # start thread with receiving msgs
            self.thread = threading.Thread(target=self.receive_messages)
            self.run = True
            self.thread.start()
            return True
        else:
            return False

    def stopReceiveMsgs(self) -> bool:
        if self.run:
            # stop thread
            self.run = False
            self.thread.join()

        self.context.setState(CPMIdleState())
        return True


class CPMIdleState(CPMState):
    def abort(self) -> None:
        return

    def receiveMsgs(self) -> bool:
        self.context.setState(CPMReceiveState())
        return self.context.receiveMsgs()

    def stopReceiveMsgs(self) -> bool:
        return True
