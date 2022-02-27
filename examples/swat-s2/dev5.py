"""
swat-s1 plc1.py
"""

from minicps.devices import  IODevice
from utils import DEV5_DATA, STATE, DEV5_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_OUT

import time

PLC2_ADDR = IP['plc2']
DEV5_ADDR = IP['dev5']

P101 = ('P101', 7)
FIT201 = ('FIT201', 8)
FIT201_PLC = ('FIT201', 2)


# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev5(IODevice):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s2 dev1 enters pre_loop'
        print
        self.set(FIT201, 0)
        self.send(FIT201_PLC, 0, PLC2_ADDR)
        self.send(FIT201, 0, DEV5_ADDR)

        time.sleep(sleep)
        time.sleep(120)


    def main_loop(self):
        """fit101 main loop.

            - reads sensors value
            - updates its enip server
        """

        print 'DEBUG: swat-s2 dev1 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS VALUE SHOULD NOT DEPEND FROM MV101 but normal deviations
            mv101 = float(self.get(P101))
            fit201 = float(self.get(FIT201))

            if (mv101 == 1 and fit201 == 0): 
                # lit101 [meters]
                self.set(FIT201, PUMP_FLOWRATE_OUT)
            else: 
                self.set(FIT201, 0)
                        
            fit201 = float(self.get(FIT201))

            print 'DEBUG dev1 fit101: %.5f' % fit201
            self.send(FIT201_PLC, fit201, PLC2_ADDR)
            self.send(FIT201, fit201, DEV5_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat-s2 dev1 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev5 = SwatDev5(
        name='dev5',
        state=STATE,
        protocol=DEV5_PROTOCOL,
        memory=DEV5_DATA,
        disk=DEV5_DATA)
