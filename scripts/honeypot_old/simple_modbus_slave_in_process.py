import threading
from time import sleep

from pymodbus.constants import Defaults
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import StartTcpServer, ModbusTcpServer, ModbusSocketFramer
from pymodbus.client.sync import ModbusTcpClient as ModbusClient


class SimpleModbusSlaveInProcess:
    def __init__(self, ip='0.0.0.0', port=502, discrete_inputs=10, coils=10, input_registers=10, holding_registers=10):
        self.ip = ip
        self.port = port
        self.discrete_inputs = discrete_inputs
        self.coils = coils
        self.input_registers = input_registers
        self.holding_registers = holding_registers
        self.closing = False

    def start_server_impl(self):
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * self.discrete_inputs),
            co=ModbusSequentialDataBlock(0, [0] * self.coils),
            ir=ModbusSequentialDataBlock(0, [0] * self.input_registers),
            hr=ModbusSequentialDataBlock(0, [0] * self.holding_registers),
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

        self.server = ModbusTcpServer(context, ModbusSocketFramer, identity=identity, address=(self.ip, self.port))
        try:
            self.server.serve_forever()
        except:
            if not self.closing:
                raise

        # StartTcpServer(context, identity=identity, address=(self.ip, self.port))


    def start_server(self):
        self.thread = threading.Thread(target=self.start_server_impl)
        self.thread.start()

        sleep(1)

        self.client = ModbusClient(self.ip, port=self.port)
        # retries=3, retry_on_empty=True)

        self.client.connect()

    def stop_server(self):
        self.client.close()
        self.closing = True
        self.server.server_close()


    def write_coil(self, address, value, unit=Defaults.UnitId):
        self.client.write_coil(address, value, unit=unit)

    def write_holdingregister(self, address, value, unit=Defaults.UnitId):
        self.client.write_register(address, value, unit=unit)