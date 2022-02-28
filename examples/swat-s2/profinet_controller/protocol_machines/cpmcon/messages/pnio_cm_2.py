from scapy.all import *
from scapy.contrib.dce_rpc import *
from scapy.contrib.pnio_rpc import *
from scapy.contrib.dce_rpc import *

load_contrib("dce_rpc")
load_contrib("pnio_rpc")


def get_connect_dcprpc_msg(ip, device, auuid):
    ip_msg = IP(dst=ip)
    udp_msg = UDP(
        sport=49153,
        dport=34964,
    )
    dcerpc = DceRpc(
        type="request",
        flags1=0x28,
        flags2=0x0,
        endianness="little",
        encoding="ASCII",
        float="IEEE",
        interface_uuid="dea00001-6c97-11d1-8271-00a02442df7d",
        activity="df16c5b3-2794-11b2-8000-a381734cba00",
    )

    ar_block_req = ARBlockReq(
        ARUUID=auuid,
        SessionKey=2,
        CMInitiatorMacAdd="C0:3E:BA:C9:19:36",
        CMInitiatorObjectUUID="dea00000-6c97-11d1-8271-0001008802cc",
        StationNameLength=10,
        CMInitiatorStationName="controller",
        ARProperties_StartupMode="Advanced",
        ARProperties_ParametrizationServer="CM_Initator",
    )
    alarm_block_req = AlarmCRBlockReq(block_type=0x0103, block_length=22)

    submodule_interface = device.body.dap_list[0].interface_submodule_item
    submodule_port = device.body.dap_list[0].port_submodule_item

    # GET ALL INPUT DATA
    usable_modules = device.body.dap_list[0].usable_modules
    input_api_objects = []
    input_iocs_objects = []

    input_frame_offset = 3

    for module in usable_modules:
        if module.used_in_slots != "" and module.input_length != 0:
            input_api_objects.append(
                IOCRAPIObject(
                    SlotNumber=int(module.used_in_slots),
                    SubslotNumber=int(0x1),
                    FrameOffset=input_frame_offset,
                ),
            )
            # +1 cause you need an additional iops in payload
            input_frame_offset = input_frame_offset + module.input_length + 1
    for module in usable_modules:
        if module.used_in_slots != "" and module.output_length != 0:
            input_iocs_objects.append(
                IOCRAPIObject(
                    SlotNumber=int(module.used_in_slots),
                    SubslotNumber=int(0x1),
                    FrameOffset=input_frame_offset,
                ),
            )
            input_frame_offset += 1

    # GET ALL OUTPUT DATA
    output_api_objects = []
    output_iocs_objects = []

    output_frame_offset = 3
    for module in usable_modules:
        if module.used_in_slots != "" and module.input_length != 0:
            output_iocs_objects.append(
                IOCRAPIObject(
                    SlotNumber=int(module.used_in_slots),
                    SubslotNumber=int(0x1),
                    FrameOffset=output_frame_offset,
                ),
            )
            output_frame_offset += 1
    for module in usable_modules:
        if module.used_in_slots != "" and module.output_length != 0:
            output_api_objects.append(
                IOCRAPIObject(
                    SlotNumber=int(module.used_in_slots),
                    SubslotNumber=int(0x1),
                    FrameOffset=output_frame_offset,
                ),
            )
            # +1 cause you need an additional iops in payload
            output_frame_offset = output_frame_offset + module.output_length + 1

    output_cr = IOCRBlockReq(
        IOCRProperties_RTClass=0x2,
        IOCRType=0x2,
        ReductionRatio=512,
        WatchdogFactor=3,
        DataLength=output_frame_offset if output_frame_offset > 40 else 40,
        DataHoldFactor=3,
        NumberOfAPIs=1,
        APIs=[
            IOCRAPI(
                IODataObjects=output_api_objects,
                IOCSs=[
                    IOCRAPIObject(SlotNumber=0x0, SubslotNumber=0x1, FrameOffset=0),
                    IOCRAPIObject(
                        SlotNumber=0x0,
                        SubslotNumber=submodule_interface.subslot_ident_number,
                        FrameOffset=1,
                    ),
                    IOCRAPIObject(
                        SlotNumber=0x0,
                        SubslotNumber=submodule_port.subslot_ident_number,
                        FrameOffset=2,
                    ),
                ]
                + output_iocs_objects,
            )
        ],
    )

    input_cr = IOCRBlockReq(
        IOCRProperties_RTClass=0x2,
        IOCRType=0x1,
        ReductionRatio=512,
        WatchdogFactor=3,
        DataHoldFactor=3,
        DataLength=input_frame_offset if input_frame_offset > 40 else 40,
        NumberOfAPIs=1,
        FrameID=0x8001,
        APIs=[
            IOCRAPI(
                IODataObjects=[
                    IOCRAPIObject(SlotNumber=0x0, SubslotNumber=0x1, FrameOffset=0),
                    IOCRAPIObject(
                        SlotNumber=0x0,
                        SubslotNumber=submodule_interface.subslot_ident_number,
                        FrameOffset=1,
                    ),
                    IOCRAPIObject(
                        SlotNumber=0x0,
                        SubslotNumber=submodule_port.subslot_ident_number,
                        FrameOffset=2,
                    ),
                ]
                + input_api_objects,
                IOCSs=input_iocs_objects,
            )
        ],
    )

    expected_submod_req = ExpectedSubmoduleBlockReq(
        NumberOfAPIs=1,
        APIs=[
            ExpectedSubmoduleAPI(
                ModuleIdentNumber=0x1,
                Submodules=[
                    ExpectedSubmodule(
                        SubslotNumber=0x0001,
                        SubmoduleIdentNumber=0x00000001,
                        DataDescription=[
                            ExpectedSubmoduleDataDescription(
                                DataDescription=1,
                                LengthIOCS=1,
                                LengthIOPS=1,
                                SubmoduleDataLength=0,
                            )
                        ],
                    ),
                    ExpectedSubmodule(
                        SubslotNumber=submodule_interface.subslot_ident_number,
                        SubmoduleIdentNumber=submodule_interface.subslot_ident_number,
                        DataDescription=ExpectedSubmoduleDataDescription(
                            DataDescription=1,
                            LengthIOCS=1,
                            LengthIOPS=1,
                            SubmoduleDataLength=0,
                        ),
                    ),
                    ExpectedSubmodule(
                        SubslotNumber=submodule_port.subslot_ident_number,
                        SubmoduleIdentNumber=submodule_port.subslot_ident_number,
                        DataDescription=ExpectedSubmoduleDataDescription(
                            DataDescription=1,
                            LengthIOCS=1,
                            LengthIOPS=1,
                            SubmoduleDataLength=0,
                        ),
                    ),
                ],
            )
        ],
    )

    # CRAFT EXPECTED SUBMODULE BLOCKS
    expected_submod_req_blocks = []

    for module in usable_modules:
        if module.used_in_slots != "" and (
            module.output_length != 0 or module.input_length != 0
        ):
            type = ""
            data_description = []
            if module.output_length != 0 and module.input_length != 0:
                type = "INPUT_OUTPUT"
                data_description = [
                    ExpectedSubmoduleDataDescription(
                        DataDescription=1,
                        LengthIOCS=1,
                        LengthIOPS=1,
                        SubmoduleDataLength=module.input_length,
                    ),
                    ExpectedSubmoduleDataDescription(
                        DataDescription=2,
                        LengthIOCS=1,
                        LengthIOPS=1,
                        SubmoduleDataLength=module.output_length,
                    ),
                ]

            elif module.output_length != 0:
                type = "OUTPUT"
                data_description = [
                    ExpectedSubmoduleDataDescription(
                        DataDescription=2,
                        LengthIOCS=1,
                        LengthIOPS=1,
                        SubmoduleDataLength=module.output_length,
                    ),
                ]

            else:
                type = "INPUT"
                data_description = [
                    ExpectedSubmoduleDataDescription(
                        DataDescription=1,
                        LengthIOCS=1,
                        LengthIOPS=1,
                        SubmoduleDataLength=module.input_length,
                    ),
                ]

            expected_submod_req_blocks.append(
                ExpectedSubmoduleBlockReq(
                    NumberOfAPIs=1,
                    APIs=[
                        ExpectedSubmoduleAPI(
                            SlotNumber=int(module.used_in_slots),
                            ModuleIdentNumber=module.module_ident_number,
                            Submodules=[
                                ExpectedSubmodule(
                                    # SubslotNumber=module.submodule_ident_number & 0xFFFF
                                    # if module.submodule_ident_number & 0xFFFF0000 == 0x0
                                    # else module.submodule_ident_number >> 16,
                                    SubmoduleIdentNumber=module.submodule_ident_number,
                                    SubslotNumber=0x1,
                                    SubmoduleProperties_Type=type,
                                    DataDescription=data_description,
                                ),
                            ],
                        )
                    ],
                )
            )

    pnio_serv_pdu = PNIOServiceReqPDU(
        args_max=16696,
        blocks=[
            ar_block_req,
            alarm_block_req,
            input_cr,
            output_cr,
            expected_submod_req,
        ]
        + expected_submod_req_blocks,
    )

    pnio_serv_pdu.max_count = 16696

    return ip_msg / udp_msg / dcerpc / pnio_serv_pdu


def get_write_request_msg(ip, device, auuid, parameterList):
    ip_msg = IP(dst=ip)
    udp_msg = UDP(
        sport=49153,
        dport=34964,
    )
    dcerpc = DceRpc(
        type="request",
        flags1=0x28,
        flags2=0x0,
        endianness="little",
        encoding="ASCII",
        float="IEEE",
        # IMPORTANT FOR WRITE REQUEST AND OPERATION OF PNIO CONTEXT MANAGER MESSAGES
        opnum=3,
        interface_uuid="dea00001-6c97-11d1-8271-00a02442df7d",
        activity="df16c5b3-2794-11b2-8000-a381734cba00",
    )

    seqNum = 1

    pnio_iod_multiple_write_req = IODWriteReq(
        seqNum=seqNum,
        ARUUID=auuid,
        API=0x0,
        slotNumber=0x0,
        subslotNumber=0x8000,
        index=0x8071,
        recordDataLength=12,
    )
    seqNum += 1

    parameter_entrys = []

    for module in device.body.dap_list[0].usable_modules:
        if module.used_in_slots != "" and module.parameters != []:
            for parameter in module.parameters:
                parameter_entrys.append(
                    IODWriteReq(
                        seqNum=seqNum,
                        ARUUID=auuid,
                        API=0x0,
                        slotNumber=int(module.used_in_slots),
                        subslotNumber=0x01, # TODO check if this is correct -> subslotnumber could be different
                        index=parameter.index,
                        recordDataLength=parameter.length,
                    )
                    / Raw(
                        # TODO fill in the values in parameterlist
                        load="".join(
                            [chr(counter & 0xFF) for counter in range(parameter.length)]
                        )
                    )
                )
                seqNum += 1

    pnio_iod_mult_write_req = IODWriteMultipleReq(
        ARUUID=auuid,
        API=0x00,
        slotNumber=0x0,
        subslotNumber=0x0,
        index=0xE040,
        recordDataLength=212,
        blocks=[
            pnio_iod_multiple_write_req
            / Raw(load="\x02\x50\x00\x08\x01\x00\x00\x00\x00\x00\x00\x01"),
        ]
        + parameter_entrys,
    )

    pnio_serv_pdu = PNIOServiceReqPDU(args_max=16696, blocks=[pnio_iod_mult_write_req])

    pnio_serv_pdu.max_count = 16696

    return ip_msg / udp_msg / dcerpc / pnio_serv_pdu


def get_application_ready_res_msg(ip, auuid, obj_uuid, interface_uuid, activity_uuid):
    ip_msg = IP(dst=ip)
    udp_msg = UDP(
        sport=49152,
        dport=49153,
    )
    dcerpc = DceRpc(
        type="response",
        flags1=0x0A,
        flags2=0x0,
        opnum=4,
        endianness="little",
        encoding="ASCII",
        float="IEEE",
        object_uuid=obj_uuid,
        interface_uuid=interface_uuid,
        activity=activity_uuid,
    )

    pnio_iod_control_res = IODControlRes(
        block_type=0x8112, SessionKey=2, ControlCommand_Done=0x0001, ARUUID=auuid
    )

    pnio_serv_pdu = PNIOServiceResPDU(blocks=[pnio_iod_control_res])

    pnio_serv_pdu.max_count = 1340

    return ip_msg / udp_msg / dcerpc / pnio_serv_pdu


def get_parameter_end_msg(ip, auuid):
    ip_msg = IP(dst=ip)
    udp_msg = UDP(
        sport=49153,
        dport=34964,
    )
    dcerpc = DceRpc(
        type="request",
        flags1=0x28,
        flags2=0x0,
        opnum=4,
        endianness="little",
        encoding="ASCII",
        float="IEEE",
        interface_uuid="dea00001-6c97-11d1-8271-00a02442df7d",
        activity="df16c5b3-2794-11b2-8000-a381734cba00",
    )

    pnio_iod_control_req = IODControlReq(ControlCommand_PrmEnd=0x0001, ARUUID=auuid)

    pnio_serv_pdu = PNIOServiceReqPDU(args_max=16696, blocks=[pnio_iod_control_req])

    return ip_msg / udp_msg / dcerpc / pnio_serv_pdu


def get_ping_msg(ip):
    ip_msg = IP(dst=ip)
    udp_msg = UDP(
        sport=49153,
        dport=34964,
    )
    dcerpc = DceRpc(
        type="request",
        flags1=0x28,
        flags2=0x0,
        opnum=0,
        endianness="little",
        encoding="ASCII",
        float="IEEE",
        interface_uuid="dea00001-6c97-11d1-8271-00a02442df7d",
        activity="df16c5b3-2794-11b2-8000-a381734cba00",
    )

    return ip_msg / udp_msg / dcerpc


def main():
    get_ping_msg("192.168.178.155")


if __name__ == "__main__":
    main()
