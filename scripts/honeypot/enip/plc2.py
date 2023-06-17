
from minicps.devices import PLC
from plc1 import SwatPLC1
from Logger import hlog

import time

class SwatPLC2(PLC): #builds upon the tags of the swat example
    # These constants are used mostly during setting up of topology
    NAME = 'plc2'
    IP = ' 10.0.2.120'
    MAC = '00:1D:9C:C7:B0:20'

    # PLC1_PROTOCOL defines type of this PLC (see PLC class in minicps package)
    PLC2_PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': {
            'address': IP,
            'tags': (
                ('LIT101', 1, 'REAL'),
            )
        }
    }

    PLC2_DATA = {
        'TODO': 'TODO',
    }

    STATE = {
        'name': 'swat_s1',
        'path': 'swat_s1_db.sqlite'
    }

    def __init__(self):
        PLC.__init__(
            self,
            name=SwatPLC2.NAME,
            state=SwatPLC2.STATE,
            protocol=SwatPLC2.PLC2_PROTOCOL,
            memory=SwatPLC2.PLC2_DATA,
            disk=SwatPLC2.PLC2_DATA)

    # Executed before main loop is started
    def pre_loop(self, sleep=0.1):
        hlog ('DEBUG: plc1 enters pre_loop')
        print

        time.sleep(sleep)

    # Main loop keeps receiving ENIP messages with one LIT101 tag and prints
    # the received value
    def main_loop(self):

        hlog ('DEBUG: plc2 enters main_loop.')
        print

        count = 0
        while(count <= 100000):
            lit = float(self.receive(('LIT101', 1), SwatPLC1.IP))
            hlog('DEBUG: plc2 received! ' + str(lit))

            time.sleep(0.4)
            count += 1

        hlog ('DEBUG plc1 shutdown')

if __name__ == "__main__":

    hlog('DEBUG plc1 start')
    # notice that memory init is different form disk init
    plc1 = SwatPLC2()
