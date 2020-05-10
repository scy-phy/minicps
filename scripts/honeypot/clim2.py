import random
from time import sleep
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from srvm import Srvm
from constants import Constants
from Logger import hlog
from temperature_simulator import TemperatureSimulator


#client ID
class Clim2:
    NAME = 'clim2'
    IP = '10.0.2.130'
    MAC = '00:1D:9C:C7:B0:30'

    def __init__(self):
        hlog("Hello Client 2")

        sleep(4)
        #start on 502 port from constants.py
        self.client = ModbusClient(Srvm.IP, port=Constants.MODBUS_PORT)
        #

        self.client.connect()

        self.temperature_simulator = TemperatureSimulator(-110.0, 150.0, 5.0)

        while True:
            self.read_coil()
            sleep(random.randrange(1, 2))

    def read_coil(self):
        address = 0
        value = self.temperature_simulator.get_next()
        hlog("write_temperature (%d, %d)" % (address, int(value)))
        self.client.read_input_registers(address=address)


if __name__ == "__main__":
    Clim2()