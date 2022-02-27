"""
swat-s1 plc1.py
"""

from minicps.devices import IODevice
from utils import DEV3_DATA, STATE, DEV3_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN
from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES

import time

PLC1_ADDR = IP['plc1']
DEV3_ADDR = IP['dev3']

LIT101 = ('LIT101', 6)
LIT101_1 = ('LIT101', 1)

MV101 = ('MV101', 5)
P101 = ('P101', 7)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev3(IODevice):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s2 dev2 enters pre_loop'
        start_level = 0.500
        time.sleep(60)        
        self.set(LIT101, start_level)
        self.send(LIT101_1, start_level, PLC1_ADDR)
        self.send(LIT101, start_level, DEV3_ADDR)
        time.sleep(sleep)


    def main_loop(self):
        """mv101 main loop.

            - reads sensors value
            - updates its enip server
        """

        print 'DEBUG: swat-s2 dev2 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS
            new_level = float(self.get(LIT101))
            
            water_volume = TANK_SECTION * new_level

            # inflows volumes
            mv101 = float(self.get(MV101))
            if int(mv101) == 1:
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                print "DEBUG RawWaterTank inflow: ", inflow
                water_volume += inflow

            # outflows volumes
            p101 = self.get(P101)
            if int(p101) == 1:
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                print "DEBUG RawWaterTank outflow: ", outflow
                water_volume -= outflow

            # compute new water_level
            new_level = water_volume / TANK_SECTION

            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            self.set(LIT101, new_level)
            self.send(LIT101_1, new_level, PLC1_ADDR)
            self.send(LIT101, new_level, DEV3_ADDR)

            # 988 sec starting from 0.500 m
            if new_level >= LIT_101_M['HH']:
                print 'DEBUG RawWaterTank above HH count: ', count
                break

            # 367 sec starting from 0.500 m
            elif new_level <= LIT_101_M['LL']:
                print 'DEBUG RawWaterTank below LL count: ', count
                break

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat-s2 dev3 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev3 = SwatDev3(
        name='dev3',
        state=STATE,
        protocol=DEV3_PROTOCOL,
        memory=DEV3_DATA,
        disk=DEV3_DATA)
