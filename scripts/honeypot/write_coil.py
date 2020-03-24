from time import sleep
import time
from simple_modbus_slave import SimpleModbusSlave


class WriteCoil:
    def run(self):
        slave = SimpleModbusSlave(port=502)
        slave.start_server()

        for t in range(10):
            slave.write_coil(address=1, value=1)
            print("COIL SENT")
            time.sleep(1)

        print("OUT OF LOOP")
        slave.stop_server()


WriteCoil().run()