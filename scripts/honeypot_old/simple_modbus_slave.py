import os
import signal
import subprocess
from time import sleep

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.constants import Defaults


class SimpleModbusSlave:
    def __init__(self, ip='0.0.0.0', port=502, discrete_inputs=10, coils=10, input_registers=10, holding_registers=10):
        self.ip = ip
        self.port = port
        self.discrete_inputs = discrete_inputs
        self.coils = coils
        self.input_registers = input_registers
        self.holding_registers = holding_registers

    def start_server(self):
        servers = os.path.abspath(os.path.realpath(__file__) + '../../../pymodbus/servers.py')
        command = 'sudo python2 {} -i {} -p {}'.format(servers, self.ip, self.port)
        self.process = subprocess.Popen(['sudo', 'python2', servers, '-i', self.ip, '-p', str(self.port)])

        sleep(4)

        self.client = ModbusClient(self.ip, port=self.port)
        # retries=3, retry_on_empty=True)

        self.client.connect()

    def stop_server(self):
        subprocess.call(['sudo', 'kill', '-s', 'SIGKILL', str(self.process.pid)])

    def write_coil(self, address, value, unit=Defaults.UnitId):
        self.client.write_coil(address, value, unit=unit)

    def write_holdingregister(self, address, value, unit=Defaults.UnitId):
        self.client.write_register(address, value, unit=unit)
