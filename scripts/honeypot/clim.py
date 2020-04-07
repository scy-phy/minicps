import random
from time import sleep
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from srvm import Srvm
from constants import Constants
from mininet.log import info

from Logger import hlog

#client ID
class Clim:
    NAME = 'clim'
    IP = ' 10.0.2.110'
    MAC = '00:1D:9C:C7:B0:10'

    def __init__(self):
        hlog("Hello Client 1 \n")

        sleep(4)
        # Create and connect client to IP Srvm.IP and port 502
        self.client = ModbusClient(Srvm.IP, port=Constants.MODBUS_PORT)
        self.client.connect()

        # List of actions to be executed randomly
        actionList = [
            self.read_coil,
            self.write_coil,
            self.read_holding_register,
            self.write_register,
            self.read_discrete_inputs,
            self.read_input_registers
        ]

        # loop for executing actions
        while True:
            # Execute random action from actionList with index 0..6
            actionList[random.randrange(0, 6)]()
            # Sleep randomly 1 or 2 s
            sleep(random.randrange(1, 2))

    def get_random_address(self):
        return random.randrange(0, 8)

    def get_random_bit(self):
        return random.randrange(0, 1)

    def get_random_short(self):
        return random.randrange(0, 65535)

    #modbus data object definition
    def write_register(self):
        address = self.get_random_address()
        value = self.get_random_short()
        hlog("write_register (%d, %d)" % (address, value))
        self.client.write_register(address=address, value=value)

    def read_holding_register(self):
        address = self.get_random_address()
        hlog("read_holding_register (%d)" % (address))
        self.client.read_holding_registers(address=address)

    def write_coil(self):
        address = self.get_random_address()
        value = self.get_random_bit()
        hlog("write_coil (%d, %d)" % (address, value))
        self.client.write_coil(address=address, value=value)

    def read_coil(self):
        address = self.get_random_address()
        hlog("read_coil (%d)" % (address))
        self.client.read_coils(address=address)

    def read_input_registers(self):
        address = self.get_random_address()
        hlog("read_input_registers (%d)" % (address))
        self.client.read_input_registers(address=address)

    def read_discrete_inputs(self):
        address = self.get_random_address()
        hlog("read_discrete_inputs (%d)" % (address))
        self.client.read_discrete_inputs(address=address)

if __name__ == "__main__":
    Clim()