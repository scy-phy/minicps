from __future__ import annotations
from abc import ABC, abstractmethod
import uuid
from protocol_machines.cpmcon.helper.gsdml_parser import XMLDevice
from protocol_machines.cpmcon.messages.pnio_cm import *
from getmac import get_mac_address
import scapy.all as scapy
from scapy.contrib.pnio_dcp import *
from scapy.contrib.pnio import *
import time

scapy.load_contrib("pnio_dcp")
scapy.load_contrib("pnio")

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

class CPMCONConnectState(CPMCONState):
    def abort(self) -> None:
        self.context.setState(CPMCONConnectState())
        return

    def connect(self, ip) -> bool:
        connect_msg = get_connect_dcprpc_msg(
            ip=ip, device=self.context.device, auuid=self.context.auuid
        )
        ans, _ = scapy.sr(
            connect_msg, iface=self.context.iface, timeout=2, multi=True, verbose=False
        )

        if len(ans) == 0: 
            self.abort()
            return False

        connect_rsp = DceRpc(ans[-1].answer[Raw].load)

        if not connect_rsp.haslayer("PNIOServiceResPDU"):
            ping_msg = get_ping_msg(ip=self.context.ip)
            ans, _ = scapy.sr1(
                ping_msg, iface=self.context.iface, timeout=2, verbose=False
            )

            ping_rsp = DceRpc(ans[-1].answer[Raw].load)

            if not ping_rsp["type"] == 5:
                self.abort()
                return False
            else:
                return self.context.connect()

        dcp_pkt = connect_rsp["PNIOServiceResPDU"]
        # status = 0: "Ok"
        if dcp_pkt.status != 0:
            self.abort()
            return False

        self.context.ip = ip
        self.context.setState(CPMCONConnectedState())
        # START PPM AND CPM MACHINES
        return True

    def write(self, parameterList) -> bool:
        return False

    def announceEndPrm(self) -> bool:
        return False

    def ackApplicationReady(self) -> bool:
        return False


class CPMCONConnectedState(CPMCONState):
    def abort(self) -> None:
        return

    def connect(self, ip) -> bool:
        return True

    def write(self, parameterList) -> bool:
        self.context.setState(CPMCONWriteState())
        return self.context.write(parameterList)

    def announceEndPrm(self) -> bool:
        self.context.setState(CPMCONEndPrmState())
        return self.context.announceEndPrm()

    def ackApplicationReady(self) -> bool:
        return False


class CPMCONWriteState(CPMCONState):
    def abort(self) -> None:
        self.context.setState(CPMCONConnectState())
        return

    def connect(self, ip) -> bool:
        return True

    def write(self, parameterList) -> bool:
        # TODO Maybe return value amount of parameters written or array of parameter-bool written
        write_msg = get_write_request_msg(
            ip=self.context.ip,
            device=self.context.device,
            auuid=self.context.auuid,
            parameterList=parameterList,
        )
        
        ans, _ = scapy.sr(
            write_msg, iface=self.context.iface, timeout=2, multi=True, verbose=False
        )

        write_rsp = DceRpc(ans[-1].answer[Raw].load)

        if not write_rsp.haslayer("PNIOServiceResPDU"):
            ping_msg = get_ping_msg(ip=self.context.ip)
            ans, _ = scapy.sr1(
                ping_msg, iface=self.context.iface, timeout=2, verbose=False
            )

            ping_rsp = DceRpc(ans[-1].answer[Raw].load)

            if not ping_rsp["type"] == 5:
                self.abort()
                return False
            else:
                return self.context.write(parameterList)

        dcp_pkt = write_rsp["PNIOServiceResPDU"]
        # status = 0: "Ok"
        if dcp_pkt.status != 0:
            self.abort()
            return False

        self.context.setState(CPMCONEndPrmState())
        return True

    def announceEndPrm(self) -> bool:
        return False

    def ackApplicationReady(self) -> bool:
        return False


class CPMCONEndPrmState(CPMCONState):
    def abort(self) -> None:
        self.context.setState(CPMCONConnectState())
        return

    def connect(self, ip) -> bool:
        return True

    def write(self, parameterList) -> bool:
        self.abort()
        return False

    def announceEndPrm(self) -> bool:
        param_end_msg = get_parameter_end_msg(ip=self.context.ip, auuid=self.context.auuid)
        ans, _ = scapy.sr(param_end_msg, iface=self.context.iface, timeout=2, verbose=False)

        param_end_msg_rsp = DceRpc(ans[-1].answer[Raw].load)

        if not param_end_msg_rsp.haslayer("PNIOServiceResPDU"):
            ping_msg = get_ping_msg(ip=self.context.ip)
            ans, _ = scapy.sr(
                ping_msg, iface=self.context.iface, timeout=2, verbose=False
            )

            ping_rsp = DceRpc(ans[-1].answer[Raw].load)

            if not ping_rsp["type"] == 5:
                self.abort()
                return False
            else:
                return self.context.announceEndPrm()
        else:
            dcerpc_pkt = param_end_msg_rsp["PNIOServiceResPDU"]
            # status = 0: "Ok"
            if dcerpc_pkt.haslayer("IODControlRes"):
                control_res = dcerpc_pkt["IODControlRes"]
                if control_res.ControlCommand_Done == 1:
                    self.context.setState(CPMCONIdleAppRdyState())
                    return True

        self.abort()
        return False

    def ackApplicationReady(self) -> bool:
        return False


class CPMCONIdleAppRdyState(CPMCONState):
    def abort(self) -> None:
        self.context.setState(CPMCONConnectState())
        return

    def connect(self, ip) -> bool:
        return True

    def write(self, parameterList) -> bool:
        self.abort()
        return False

    def announceEndPrm(self) -> bool:
        return True

    def ackApplicationReady(self) -> bool:
        # WAIT FOR APPLICATION READY RESPONSE
        def send_application_ready_rsp_callback(pkt):
            app_rdy_rsp = DceRpc(pkt[Raw].load)
            if app_rdy_rsp.haslayer("IODControlReq"):
                if (
                    app_rdy_rsp.getlayer(
                        "IODControlReq"
                    ).ControlCommand_ApplicationReady
                    == 1
                ):
                    rpc_payload = app_rdy_rsp["DCE/RPC"]
                    obj_uuid = rpc_payload.object_uuid
                    interface_uuid = rpc_payload.interface_uuid
                    activity_uuid = rpc_payload.activity
                    application_ready_res_msg = get_application_ready_res_msg(
                        ip=self.context.ip,
                        auuid=self.context.auuid,
                        obj_uuid=obj_uuid,
                        interface_uuid=interface_uuid,
                        activity_uuid=activity_uuid,
                    )
                    send(
                        application_ready_res_msg,
                        iface=self.context.iface,
                        verbose=False,
                    )
                    self.context.setState(CPMCONEstablishedConnectionState())
                    return True
            self.context.setState(CPMCONConnectState())
            return False
            

        sniff(
            filter=f"udp and host {self.context.ip} and port 34964",
            store=0,
            count=1,
            prn=send_application_ready_rsp_callback,
            iface=self.context.iface,
        )


class CPMCONEstablishedConnectionState(CPMCONState):
    def abort(self) -> None:
        self.context.setState(CPMCONConnectState())
        return

    def connect(self, ip) -> bool:
        return True

    def write(self, parameterList) -> bool:
        return False

    def announceEndPrm(self) -> bool:
        return True

    def ackApplicationReady(self) -> bool:
        return True
