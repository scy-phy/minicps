"""
SWaT sub1 physical process

RawWaterTank has an inflow pipe and outflow pipe, both are modeled according
to the equation of continuity from the domain of hydraulics
(pressurized liquids) and a drain orefice modeled using the Bernoulli's
principle (for the trajectories).
"""


from minicps.devices import Tank

from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT, TANK2_INFLOW, TANK2_OUTFLOW
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL, LIT_301_M
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES
import pandas as pd

import sys
import time


# SPHINX_SWAT_TUTORIAL TAGS(
MV101 = ('MV101', 1)
P101 = ('P101', 1)
LIT101 = ('LIT101', 1)
LIT301 = ('LIT301', 3)
FIT101 = ('FIT101', 1)
FIT201 = ('FIT201', 2)
# SPHINX_SWAT_TUTORIAL TAGS)


# TODO: implement orefice drain with Bernoulli/Torricelli formula
class RawWaterTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(MV101, 1)
        self.set(P101, 0)
        self.level1 = self.set(LIT101, 0.800)
        self.level2 = self.set(LIT301,0.850)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

        # test underflow
        # self.set(MV101, 0)
        # self.set(P101, 1)
        # self.level1 = self.set(LIT101, 0.500)

    def main_loop(self):

        count = 0
        columns = ['Time', 'MV101', 'P101', 'LIT101', 'LIT301', 'FIT101', 'FIT201']
        df = pd.DataFrame(columns=columns)
        timestamp=0
        while(count <= PP_SAMPLES):

            tank1_level = self.level1
            tank2_level = self.level2

            # compute water volume
            tank1_volume = self.section * tank1_level

            # inflows volumes
            mv101 = self.get(MV101)
            if int(mv101) == 1:
                self.set(FIT101, PUMP_FLOWRATE_IN)
                tank1_inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print("DEBUG RawWaterTank tank1_inflow: ", tank1_inflow)
                tank1_volume += tank1_inflow
            else:
                self.set(FIT101, 0.00)

            # outflows volumes
            p101 = self.get(P101)
            if int(p101) == 1:
                self.set(FIT201, PUMP_FLOWRATE_OUT)
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                # print("DEBUG RawWaterTank outflow: ", outflow)
                tank1_volume -= outflow
                tank2_level += TANK2_INFLOW - TANK2_OUTFLOW
            else:
                tank2_level -= TANK2_OUTFLOW
                self.set(FIT201, 0.00)

            # compute new water_level
            tank1_level = tank1_volume / self.section

            # level cannot be negative
            if tank1_level <= 0.0:
                tank1_level = 0.0

            # update internal and state water level
            print("DEBUG tank1_level: %.5f \t delta: %.5f" % (
                tank1_level, tank1_level - self.level1))
            self.level1 = self.set(LIT101, tank1_level)
            self.level2 = self.set(LIT301, tank2_level)

            # 988 sec starting from 0.500 m
            if tank1_level >= LIT_101_M['HH']:
                print('DEBUG RawWaterTank above HH count: ', count)
                break
            
            if tank2_level >= LIT_301_M['HH']:
                print('DEBUG WaterTank2 above HH count: ', count)
                break

            # 367 sec starting from 0.500 m
            elif tank1_level <= LIT_101_M['LL']:
                print('DEBUG RawWaterTank below LL count: ', count)
                break 
            new_data = pd.DataFrame(data = [[timestamp, self.get(MV101), self.get(P101), self.get(LIT101), self.get(LIT301), self.get(FIT101), self.get(FIT201)]], columns=columns)
            df = pd.concat([df,new_data])
            df.to_csv('logs/data.csv', index=False)
            count += 1
            time.sleep(PP_PERIOD_SEC)
            timestamp+=PP_PERIOD_SEC


if __name__ == '__main__':

    rwt = RawWaterTank(
        name='rwt',
        state=STATE,
        protocol=None,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )
