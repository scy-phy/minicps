from protocol_machines.cmina.context import Device, CMINAState
from protocol_machines.cmina.states import *
from protocol_machines.cpm.context import Consumer, CPMState
from protocol_machines.cpm.states import *
from protocol_machines.cpmcon.helper.device import GSDMLDevice
from protocol_machines.ppm.context import Provider, PPMState
from protocol_machines.ppm.states import *
from protocol_machines.cpmcon.context import Connection, CPMCONState
from protocol_machines.cpmcon.states import *
from protocol_machines.cpmcon.helper.gsdml_parser import XMLDevice
from state.SqliteState import SQLiteState
import argparse
from scapy.contrib.pnio_rpc import *
from scapy.contrib.dce_rpc import *
import argparse

load_contrib("dce_rpc")
load_contrib("pnio_rpc")

class PNConnection:
    def __init__(self, iface, mac_address, device_path, state) -> None:
        print(mac_address)
        self.device = Device(CMINAIdentifyState(), iface=iface)
        self.connection = Connection(
            CPMCONConnectState(),
            iface=iface,
            device=GSDMLDevice(XMLDevice(device_path)),
            auuid=str(uuid.uuid4()),
        )
        self.consumer = Consumer(
            CPMIdleState(),
            iface=iface,
            device=XMLDevice(device_path),
            dst_adr=mac_address,
            dbState=state,
        )
        self.provider = Provider(
            PPMIdleState(),
            iface=iface,
            device=XMLDevice(device_path),
            dst_adr=mac_address,
            dbState=state,
        )

    def initialize_device(self, ip, name, prev_device_name="") -> CMINAState:
        self.device.identify(prev_device_name)
        self.device.setIp(ip=ip)
        self.device.setName(name)

        return self.device.getState()

    def connect_device(self, ip, parameter_list="") -> CPMCONState:
        self.connection.connect(ip)
        self.connection.write(parameter_list)

        self.start_consumer_provider()

        self.connection.announceEndPrm()
        self.connection.ackApplicationReady()

        time.sleep(30)

        self.stop_consumer_provider()

        return self.connection.getState()

    def start_consumer_provider(self) -> bool:
        self.provider.sendMsgs()
        self.consumer.receiveMsgs()
        return True

    def stop_consumer_provider(self) -> bool:
        self.provider.stopMsgs()
        self.consumer.stopReceiveMsgs()
        return True


# IMPORTANT: IP MUST BE IN SUBNET AND GATEWAY!!!

# PATH = "profinet_device.sqlite"
# NAME = "profinet_device"
# STATE = {"name": NAME, "path": PATH}


def main():
    # Create the parser
    pnio_parser = argparse.ArgumentParser(
        description="Create a connection to a ProfiNet Device", allow_abbrev=False
    )

    # Add the arguments
    pnio_parser.add_argument(
        "-p",
        "--path",
        action="store",
        metavar="path",
        type=str,
        help="the path to the GSDML File of the IO-Device",
        default="./gsdml/test_project.xml",
    )

    pnio_parser.add_argument(
        "-m",
        "--mac",
        action="store",
        metavar="mac",
        type=str,
        help="the mac of the IO-Device",
        required=True,
    )

    pnio_parser.add_argument(
        "-if",
        "--iface",
        action="store",
        metavar="iface",
        type=str,
        help="the interface used to connect to the IO-Device",
        default="eth0",
        required=True,
    )

    pnio_parser.add_argument(
        "-ip",
        "--ip",
        action="store",
        metavar="ip",
        type=str,
        help="the IP the IO-Device should use",
        required=True,
    )

    pnio_parser.add_argument(
        "-n",
        "--name",
        action="store",
        metavar="name",
        type=str,
        help="the NameOfStation the IO-Device should use",
        default="rt-labs-dev",
        required=True,
    )

    pnio_parser.add_argument(
        "-dn",
        "--dbname",
        action="store",
        metavar="dbname",
        type=str,
        help="name of sqlite table",
        default="profinet_device",
        required=True,
    )

    pnio_parser.add_argument(
        "-dp",
        "--dbpath",
        action="store",
        metavar="dbpath",
        type=str,
        help="path to sqlite table",
        default="profinet_device.sqlite",
        required=True,
    )

    # Execute the parse_args() method
    args = pnio_parser.parse_args()

    # Sleep 15 Seconds to wait for IO-Device
    # time.sleep(15)

    # TODO: CHECK THE ARGUMENTS

    dbstate = {"name": args.dbname, "path": args.dbpath}

    state = SQLiteState(dbstate)

    print("---INIT START---")
    connection = PNConnection(
        iface=args.iface, mac_address=args.mac, device_path=args.path, state=state
    )
    print("---INIT END---")
    print("---INIT DEVICE START---")
    connection.initialize_device(ip=args.ip, name=args.name, prev_device_name="")
    # set mac adress for corresponding device otherwise no messages are received
    connection.consumer.dst_adr = connection.device.getDeviceMac()
    print("---INIT DEVICE END---")
    print("---CONNECT DEVICE START---")
    connection.connect_device(ip=args.ip)
    print("---CONNECT DEVICE END---")


if __name__ == "__main__":
    main()
