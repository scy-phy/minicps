from scapy.all import *
from scapy.contrib.pnio_rpc import *
from scapy.contrib.dce_rpc import *
from scapy.contrib.pnio import *
from profinet_controller.protocol_machines.ppm.helper.gsdml_parser import XMLDevice

load_contrib("pnio")
load_contrib("pnio_rpc")
load_contrib("dce_rpc")


def get_data_msg(dst, src, device, data, counter, timer):
    ether = Ether(dst=dst, src=src, type=0x8892)

    cyclic_packet = ProfinetIO(frameID=0x8000)

    usable_modules = device.body.dap_list[0].usable_modules
    output_data_objects = []
    output_iocs_objects = []

    first_iocs = PNIORealTime_IOxS(
        dataState=0x1, instance=0x0, reserved=0x0, extension=0x0
    )

    sec_iocs = PNIORealTime_IOxS(
        dataState=0x1, instance=0x0, reserved=0x0, extension=0x0
    )

    thir_iocs = PNIORealTime_IOxS(
        dataState=0x1, instance=0x0, reserved=0x0, extension=0x0
    )
    output_frame_offset = 3

    for module in usable_modules:
        if module.used_in_slots != "" and module.input_length != 0:
            output_iocs_objects.append(
                PNIORealTime_IOxS(
                    dataState=0x1, instance=0x0, reserved=0x0, extension=0x0
                )
            )
            output_frame_offset += 1
    for module in usable_modules:
        if module.used_in_slots != "" and module.output_length != 0:
            payload = chr(counter & 0xFF)

            for x in data:
                if (
                    x["module_ident"] == module.module_ident_number
                    and x["submodule_ident"] == module.submodule_ident_number
                ):
                    print(x["values"])
                    payload = "".join([chr(x) for x in x["values"]])

            output_data_objects.append(
                PNIORealTimeCyclicPDU.build_fixed_len_raw_type(module.output_length)(
                    data=payload
                )
                / PNIORealTime_IOxS(
                    dataState=0x1, instance=0x0, reserved=0x0, extension=0x0
                ),
            )
            output_frame_offset = output_frame_offset + module.output_length + 1

    pdu = PNIORealTimeCyclicPDU(
        cycleCounter=(32 * timer * (counter & 0xffff) & 0xffff),
        padding="".join(["\x00" for _ in range(40 - output_frame_offset)]) # data packet must have specific length -> pdu has to be minimum 40 bytes
        if output_frame_offset < 40 
        else "",
        data=[
            first_iocs,
            sec_iocs,
            thir_iocs,
        ]
        + output_iocs_objects
        + output_data_objects,
    )

    return ether / cyclic_packet / pdu


class PNIOPSMessage:
    def __init__(self) -> None:
        self.cycle_counter = 0
        self.data_status = {
            "ignore": False,  # 1: Ignore 0: Evaluate
            "reserved_2": False,  # should be zero
            "station_problem_indicator": False,  # 1: Ok, 0: Problem
            "provider_state": False,  # 1: Run 0: Stop
            "reserved_1": False,  # should be zero
            "data_valid": False,  # 1: Valid, 0: Invalid
            "redundancy": False,  # has no meaning for outputCRs
            "state": False,  # 1: primary, 0. backup
        }
        self.input_data = {"iops": [], "iocs": [], "data": []}

    def convert_number_to_state_array(self, flags):
        self.data_status = {
            "ignore": flags.ignore,  # 1: Ignore 0: Evaluate
            "reserved_2": flags.reserved_2,  # should be zero
            "station_problem_indicator": flags.no_problem,  # 1: Ok, 0: Problem
            "provider_state": flags.run,  # 1: Run 0: Stop
            "reserved_1": flags.reserved_1,  # should be zero
            "data_valid": flags.validData,  # 1: Valid, 0: Invalid
            "redundancy": flags.redundancy,  # has no meaning for outputCRs
            "state": flags.primary,  # 1: primary, 0. backup
        }

    def bitarray_to_number(self, array):
        i = 0
        for bit in array:
            i = (i << 1) | bit
        return i

    def parse_io_state(self, state, slot, subslot):
        status_array = [int(digit) for digit in bin(state + 0x100)[2:]][1:]
        return {
            "module": str(slot),
            "submodule": str(subslot),
            "data_state": bool(status_array[0]),  # 1: Good 0: Bad
            "instance": self.bitarray_to_number(
                status_array[1:3]
            ),  # should be zero 0: Detected by subslot
            "reserved": self.bitarray_to_number(status_array[3:7]),  # should be zero
            "extension": bool(
                status_array[7]
            ),  # 0: No IOxS octet follows 1: IOxS octet follows
        }

    def parse_input_data(self, data, device):
        usable_modules = device.body.dap_list[0].usable_modules

        payload_bytes = list(data)

        first_iops = self.parse_io_state(payload_bytes[0], 0x1, 0x1)

        sec_iops = self.parse_io_state(payload_bytes[1], 0x1, 0x8000)

        thir_iops = self.parse_io_state(payload_bytes[2], 0x1, 0x8001)

        iops = [first_iops, sec_iops, thir_iops]
        iocs = []
        data = []

        output_frame_offset = 3

        for module in usable_modules:
            if module.used_in_slots != "" and module.output_length != 0:
                data.append(
                    payload_bytes[
                        output_frame_offset : (
                            output_frame_offset + module.output_length
                        )
                    ]
                )
                iops.append(
                    self.parse_io_state(
                        payload_bytes[output_frame_offset + module.output_length],
                        module.module_ident_number,
                        module.submodule_ident_number,
                    )
                )
                output_frame_offset += module.output_length + 1
        for module in usable_modules:
            if module.used_in_slots != "" and module.input_length != 0:
                iocs.append(
                    self.parse_io_state(
                        payload_bytes[output_frame_offset],
                        module.module_ident_number,
                        module.submodule_ident_number,
                    )
                )
                output_frame_offset += 1

        self.input_data = {"iops": iops, "iocs": iocs, "data": data}


def parse_data_message(packet, device):
    message = PNIOPSMessage()

    if packet.haslayer("PROFINET IO Real Time Cyclic Default Raw Data"):
        pkt_rt = packet.getlayer("PROFINET Real-Time")
        pkt_raw_layer = packet.getlayer("PROFINET IO Real Time Cyclic Default Raw Data")
        message.convert_number_to_state_array(pkt_rt.dataStatus)
        message.cycle_counter = pkt_rt.cycleCounter
        message.parse_input_data(pkt_raw_layer.data, device)

        return message

    else:
        return


def main():
    pass


if __name__ == "__main__":
    main()
    scapy_cap = rdpcap("C://Users/sebas//OneDrive//Desktop//pdu_packet_rt.pcapng")
    parse_data_message(scapy_cap[0], XMLDevice("../gsdml/test_project_2.xml"))
    scapy_cap = rdpcap("C://Users/sebas//OneDrive//Desktop//pdu_packet.pcapng")
    parse_data_message(scapy_cap[0], XMLDevice("../gsdml/test_project.xml"))
