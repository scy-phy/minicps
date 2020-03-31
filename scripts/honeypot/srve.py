import os
import subprocess
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
        enip.main(argv=['-a', '1.2.3.4'])
#sudo python2 -m cpppo.server.enip -v Scada=DINT[1000]
#python -m cpppo.server.enip.client -v --print Scada[1]=99
if __name__ == "__main__":
    Srve()