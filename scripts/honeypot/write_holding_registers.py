from simple_modbus_slave_in_process import SimpleModbusSlaveInProcess


class WriteHoldingRegister:
    def run(self):
        slave = SimpleModbusSlaveInProcess(port=502)
        slave.start_server()

        slave.write_holdingregister(address=1, value=1)

        slave.stop_server()


WriteHoldingRegister().run()
