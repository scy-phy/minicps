import os

from minicps.devices import PLC
from temperature_simulator import TemperatureSimulator
from Logger import hlog

import time

class SwatPLC1(PLC):  #builds upon the tags of the swat example
    # These constants are used mostly during setting up of topology
    NAME = 'plc1'
    IP = ' 10.0.2.110'
    MAC = '00:1D:9C:C7:B0:10'

    # PLC1_PROTOCOL defines type of this PLC (see PLC class in minicps package)
    PLC1_PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': {
            'address': IP,
            'tags': (
                ('LIT101', 1, 'REAL'),
                ('LIT101', 2, 'REAL'),
                ('LIT101', 3, 'REAL'),
            )
        }
    }

    # This PLC doesn't use data yet
    PLC1_DATA = {
        'TODO': 'TODO',
    }

    # State of this PLC is stored in Sqlite database on this path
    STATE = {
        'name': 'swat_s1',
        'path': 'swat_s1_db.sqlite'
    }

    def __init__(self):
        self.temperature_simulator = TemperatureSimulator(0.0, 50.0, 5.0)
        PLC.__init__(
            self,
            name='plc1',
            state=SwatPLC1.STATE,
            protocol=SwatPLC1.PLC1_PROTOCOL,
            memory=SwatPLC1.PLC1_DATA,
            disk=SwatPLC1.PLC1_DATA)

    # Executed before main loop is started
    def pre_loop(self, sleep=0.1):

        hlog ('DEBUG:plc1 enters pre_loop')
        print

        time.sleep(sleep)

    # Main loop keeps sending ENIP messages with one LIT101 tag and value
    # obtained from temperature simulator.
    def main_loop(self):

        hlog ('DEBUG: plc1 enters main_loop.')
        print

        count = 0
        while(count <= 1000000):
            lit101 = float(self.temperature_simulator.get_next())
            hlog ('DEBUG plc1 lit101: %.5f' % lit101)
            self.send(('LIT101', 3), lit101, SwatPLC1.IP)

            count += 1

        hlog ('DEBUG plc1 shutdown')

if __name__ == "__main__":

    hlog('DEBUG plc1 start')
    plc1 = SwatPLC1()
