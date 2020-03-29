import random
from time import sleep
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from srv import Srv
from constants import Constants
from mininet.log import info

from Logger import hlog


class Cli:
    NAME = 'cli'
    IP = '192.168.1.10'
    MAC = '00:1D:9C:C7:B0:10'

    def __init__(self):
        hlog("Hello world")

        sleep(4)

        self.client = ModbusClient(Srv.IP, port=Constants.MODBUS_PORT)
        # retries=3, retry_on_empty=True)

        self.client.connect()

        map = {
            0: self.read_coil,
            1: self.write_coil,
            2: self.read_holding_register,
            3: self.write_register
        }

        while True:
            map[random.randrange(0, 4)]()
            sleep(1)

    def get_random_address(self):
        return random.randrange(0, 8)

    def get_random_bit(self):
        return random.randrange(0, 1)

    def get_random_short(self):
        return random.randrange(0, 65535)

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

if __name__ == "__main__":
    Cli()