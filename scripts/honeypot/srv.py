import os
import subprocess
from time import sleep

from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.asynchronous import StartTcpServer

from constants import Constants
from Logger import hlog


class Srv:
    NAME = 'srv'
    IP = '192.168.1.20'
    MAC = '00:1D:9C:C7:B0:20'

    def out_of_process_server(self):
        hlog("Here!")
        servers = os.path.abspath(os.path.realpath(__file__) + '../../../pymodbus/servers.py')
        self.process = subprocess.Popen(['sudo', 'python2', servers, '-i', Srv.IP, '-p', str(Constants.MODBUS_PORT)])
        sleep(3600)

    def in_process_server(self):
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 10),
            co=ModbusSequentialDataBlock(0, [0] * 10),
            ir=ModbusSequentialDataBlock(0, [0] * 10),
            hr=ModbusSequentialDataBlock(0, [0] * 10),
            zero_mode=False,
        )

        # NOTE: use 0-based addressing mapped internally to 1-based
        context = ModbusServerContext(slaves=store, single=True)

        # TODO: server id information
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Pymodbus'
        identity.ProductCode = 'PM'
        identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
        identity.ProductName = 'Pymodbus Server'
        identity.ModelName = 'Pymodbus Server'
        identity.MajorMinorRevision = '1.0'

        StartTcpServer(context, identity=identity,
            address=(Srv.IP, Constants.MODBUS_PORT))

    def __init__(self):
        self.in_process_server()

if __name__ == "__main__":
    Srv()