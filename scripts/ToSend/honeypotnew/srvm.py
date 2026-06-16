import os
import subprocess
import random
from threading import Thread
from time import sleep
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.asynchronous import StartTcpServer
from constants import Constants
from Logger import hlog

#srv ID
from temperature_simulator import TemperatureSimulator

# Implements a Modbus server which reads a stream of values from TemperatureSimulator
# and sends them to clients as input_register 1.
class Srvm:
    # These constants are used mostly during setting up of topology
    NAME = 'srvm'
    IP = '10.0.2.120'
    MAC = '00:1D:9C:C7:B0:20'

    def __init__(self):
        self.coils = None

    def out_of_process_server(self):
        #start server from directory then sleep
        servers = os.path.abspath(os.path.realpath(__file__) + '../../../pymodbus/servers.py')
        self.process = subprocess.Popen(['sudo', 'python2', servers, '-i', Srvm.IP, '-p', str(Constants.MODBUS_PORT)])
        sleep(3600)

    def change_temp(self):
        hlog("Server in thread")
        while True:
            try:
                hlog("Server changing temperature")
                self.input_registers.setValues(1, self.temperature_simulator.get_next())
                sleep(random.randrange(1, 2)) #sleep in range
            except Exception as e:
                hlog("Exception: " + str(e))

    # Created mostly as copy paste from pymodbus/servers.py
    #data blocks sent by modbus
    def in_process_server(self):
        self.coils = ModbusSequentialDataBlock(0, [0] * 10)
        self.coils.setValues(0, 32)
        self.coils.setValues(1, 33)
        self.coils.setValues(2, 34)

        hlog("Server starting thread")
        self.temperature_simulator = TemperatureSimulator(-110.0, 150.0, 5.0)
        self.thread = Thread(target=self.change_temp,args=())
        self.thread.daemon = True
        self.thread.start()
        hlog("Server started thread")

        self.discrete_inputs = ModbusSequentialDataBlock(0, [0] * 10)
        self.discrete_inputs.setValues(0, 32)
        self.discrete_inputs.setValues(1, 33)
        self.discrete_inputs.setValues(2, 34)

        self.input_registers = ModbusSequentialDataBlock(0, [0] * 10)
        self.input_registers.setValues(0, 32)
        self.input_registers.setValues(1, 33)
        self.input_registers.setValues(2, 34)
        self.input_registers.setValues(3, 35)

        # This defines number of coils/registers on server
        # Number 10 below specifies that there are 0..8 addressable
        # coils/registers on server.
        store = ModbusSlaveContext(
            di=self.discrete_inputs,
            co=self.coils,
            ir=self.input_registers,
            hr=ModbusSequentialDataBlock(0, [0] * 10),
            zero_mode=False,
        )


        context = ModbusServerContext(slaves=store, single=True)

        # server ID - copied from servers.py
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Pymodbus'
        identity.ProductCode = 'PM'
        identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
        identity.ProductName = 'Pymodbus Server'
        identity.ModelName = 'Pymodbus Server'
        identity.MajorMinorRevision = '1.0'

        # Starts MODBUS server on interface with IP Srvm.IP and port Constants.MODBUS_PORT
        StartTcpServer(context, identity=identity,
                       address=(Srvm.IP, Constants.MODBUS_PORT))

    def __init__(self):
        self.in_process_server()

if __name__ == "__main__":
    Srvm()