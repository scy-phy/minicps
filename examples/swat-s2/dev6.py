"""
swat-s1 plc1.py
"""

from minicps.devices import IODevice
from utils import DEV6_DATA, STATE, DEV6_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN
from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES

import time

PLC3_ADDR = IP['plc3']
PLC2_ADDR = IP['plc2']
PLC1_ADDR = IP['plc1']

DEV6_ADDR = IP['dev6']

LIT301 = ('LIT301', 9)
LIT301_1 = ('LIT301', 3)

FIT201_PLC = ('FIT201', 2)
P101_PLC = ('P101', 1)
P101 = ('P101', 7)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev6(IODevice):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s2 dev2 enters pre_loop'
        start_level = 0.00
        self.set(LIT301, start_level)
        self.send(LIT301_1, start_level, PLC3_ADDR)
        self.send(LIT301, start_level, DEV6_ADDR)
        time.sleep(sleep)
        time.sleep(20)

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
            new_level = float(self.get(LIT301))
            
            water_volume = TANK_SECTION * new_level

            # inflows volumes
            p101 = float(self.get(P101))   
            if p101 > 0:
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank inflow: ", inflow
                water_volume += inflow

            # outflows volumes
            # p101 = self.get(P101)
            # if int(p101) == 1:
            #     outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
            #     print "DEBUG RawWaterTank outflow: ", outflow
            #     water_volume -= outflow

            # compute new water_level
            new_level = water_volume / TANK_SECTION

            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            # print "DEBUG new_level: %.5f \t delta: %.5f" % (
                # new_level, new_level - self.level)
            self.set(LIT301, new_level)
            self.send(LIT301_1, new_level, PLC3_ADDR)
            self.send(LIT301, new_level, DEV6_ADDR)

            # 988 sec starting from 0.500 m
            if new_level >= LIT_101_M['HH']:
                # print 'DEBUG RawWaterTank above HH count: ', count
                break

            # 367 sec starting from 0.500 m
            elif new_level <= LIT_101_M['LL']:
                # print 'DEBUG RawWaterTank below LL count: ', count
                break

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat-s2 dev6 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev6 = SwatDev6(
        name='dev6',
        state=STATE,
        protocol=DEV6_PROTOCOL,
        memory=DEV6_DATA,
        disk=DEV6_DATA)
