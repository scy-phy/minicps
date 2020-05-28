import os
import subprocess
from threading import Thread
from time import sleep

from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.asynchronous import StartTcpServer

from constants import Constants
from Logger import hlog

from cpppo.server import enip

class Srve:
    NAME = 'srve'
    IP = '192.168.1.20'
    MAC = '00:1D:9C:C7:B0:20'

    def __init__(self):
        hlog("Hello server0")
        self.out_of_process()

    def in_process(self):
        self.thread = Thread(target=self.run_server)
        self.thread.start()

    def run_server(self):
        hlog("Hello server")
        enip.main(argv=[
            '--verbose',
            '--print',
            '--address', Srve.IP + ":" + str(Constants.ENIP_TCP_PORT),
            '--log', Constants.ENIP_SRV_LOG_FILE,
            'Scada=DINT[1000]'])
        hlog("Hello server2")

    def out_of_process(self):
        subprocess.Popen(args=[
            'python2',
            '-m', 'cpppo.server.enip',
            '--verbose',
            '--print',
            '--address', Srve.IP + ":" + str(Constants.ENIP_TCP_PORT),
            '--log', Constants.ENIP_SRV_LOG_FILE,
            'Scada=DINT[1000]'])


#sudo python2 -m cpppo.server.enip -v Scada=DINT[1000]
#python -m cpppo.server.enip.client -v --print Scada[1]=99
if __name__ == "__main__":
    Srve()