"""
swat-s1 plc1.py
"""

from minicps.devices import IODevice
from utils import DEV1_DATA, STATE, DEV1_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN

import time

PLC1_ADDR = IP['plc1']
DEV1_ADDR = IP['dev1']

FIT101 = ('FIT101', 4)
FIT101_PLC = ('FIT101', 1)

MV101 = ('MV101', 5)


# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev1(IODevice):

    def __init__(self, name, protocol, state):
        super(IODevice, self).__init__(name, protocol, state)

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s2 dev1 enters pre_loop'
        print

        time.sleep(sleep)

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
            mv101 = float(self.get(MV101))
            fit101 = float(self.get(FIT101))

            if (mv101 == 1 and fit101 == 0): 
                # lit101 [meters]
                self.set(FIT101, PUMP_FLOWRATE_IN)
            else: 
                self.set(FIT101, 0)
                        
            fit101 = float(self.get(FIT101))

            print 'DEBUG dev1 fit101: %.5f' % fit101
            self.send(FIT101_PLC, fit101, PLC1_ADDR)
            self.send(FIT101, fit101, DEV1_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat-s2 dev1 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev1 = SwatDev1(
        name='dev1',
        state=STATE,
        protocol=DEV1_PROTOCOL,
        memory=DEV1_DATA,
        disk=DEV1_DATA)
