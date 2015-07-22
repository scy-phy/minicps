"""
SWaT physical process
"""

import sqlite3
from constants import TANK_DIAMETER
from constants import VALVE_DIAMETER
from constants import TIMER
from constants import TIMEOUT
from constants import GRAVITATION
from constants import P1_PLC1_TAGS
from constants import P1_PLC2_TAGS
from constants import P1_PLC3_TAGS
from constants import STATE_DB_PATH
from constants import read_single_statedb
from constants import read_statedb
from constants import update_statedb
from constants import select_value
from constants import logger
from multiprocessing import Process
from time import sleep
from time import time
from math import sqrt as sqrt
from math import pow as power
from math import pi

def flow_to_height(flow, diameter):
    """
    flow: flow value (m^3/h)
    diameter: tank diameter (m^2)
    returns: height per hour corresponding (m/h)
    """
    return flow / diameter

def speed_to_height(speed, valve_diameter, tank_diameter):
    """
    speed: speed of water in a pipe (m/s)
    valve_diameter: (m)
    tank_diamaeter: (m)

    returns: height per second corresponding in the tank (m/s)
    """
    return speed * power(valve_diameter, 2) / power(tank_diameter, 2)

def Toricelli(flow_level, valve_height=0):
    """
    Toricelli formula, which returns the speed of the flow (m/s) according to
    the flow level (m) in the tank and the valve height (m),
    considering the speed as a constant in the Bernoulli formula.
    """
    return sqrt(2 * GRAVITATION * (flow_level - valve_height))

###################################
#         PHYSICAL PROCESS
###################################
class Tank:
    def __init__(self, FIT_in, MV, LIT, P, FIT_out, subprocess, diameter, timer, timeout):
        self.__FIT_in = FIT_in
        self.__MV = MV
        self.__LIT = LIT
        self.__P = P
        self.__FIT_out = FIT_out
        self.__subprocess = subprocess
        self.__diameter = diameter
        self.__timer = timer
        self.__timeout = timeout
        self.__process = None

    def __del__(self):
        if(self.__process != None):
            self.__process.join()

    def compute_new_flow_level(self, FIT_list, MV_list, current_flow, P_list, valve_diameter):
        """
        FIT_list: list of input flow values (m^3/h)
        MV_list: list of boolean which tell if the valve is open or not
        current_flow: current flow level (m)
        P_list: list of output valves which tells if they are open or not
        tank_diameter: (m)
        valve_diameter: (m)
        timer: period in which the flow level is computed (s)

        returns: new flow level (m)
        """
        height = current_flow
        for i in (0, len(FIT_list) - 1):
            if MV_list[i] != 0:
                # FIT_list[i] is supposed to be in m^3/h and timer in seconds => conversion
                height += self.__timer * (flow_to_height(FIT_list[i], self.__diameter) / 3600)
        if P_list is not None:
            for i in (0, len(P_list) - 1):
                if P_list[i] != 0:
                    # Toricelli formula gives the speed in m/s => no conversion
                    height -= self.__timer * speed_to_height(Toricelli(current_flow), valve_diameter, self.__diameter)
        return height

    def action(self, valve_diameter):
        input_flows = []
        input_valves = []
        if self.__P is not None:
            output_valves = []
        else:
            output_valves = None

        for index in self.__FIT_in:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_flows.append(select_value(value))

        for index in self.__MV:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_valves.append(select_value(value))

        if self.__P is not None:
            for index in self.__P:
                value = read_single_statedb(self.__subprocess, index)
                if value is not None:
                    output_valves.append(select_value(value))

        current_flow = read_statedb(NAME=self.__LIT)
        print self.__subprocess
        print current_flow[0][3]
        if current_flow is not None:
            logger.debug('PP - read from state db %s' % current_flow[0][3])

            if self.__FIT_out is not None:
                v = Toricelli(float(current_flow[0][3]))  # m/s
                flow = v * power(valve_diameter/2.0, 2) * pi * 3600.0  # m^3/h
                update_statedb(flow, self.__subprocess+1, self.__FIT_out)

            new_flow = self.compute_new_flow_level(input_flows, input_valves, float(current_flow[0][3]), output_valves, valve_diameter)
            logger.debug('PP - write to state db %.4f' % new_flow)
            update_statedb(new_flow, self.__LIT)

    def action_wrapper(self, valve_diameter):
        start_time = time()
        while(time() - start_time < self.__timeout):
            self.action(valve_diameter)
            sleep(self.__timer)

    def start(self, valve_diameter):
        """
        Runs the action() process
        """
        self.__process = Process(target = self.action_wrapper, args = (valve_diameter,))
        self.__process.start()

if __name__ == '__main__':
    tank1 = Tank(['AI_FIT_101_FLOW'], ['DO_MV_101_OPEN'], 'AI_LIT_101_LEVEL', ['DO_P_101_START'], ['AI_FIT_201_FLOW'], 1, TANK_DIAMETER, TIMER, TIMEOUT)
    tank2 = Tank(['AI_FIT_201_FLOW'], ['DO_MV_201_OPEN'], 'AI_LIT_301_LEVEL', None, None, 2, TANK_DIAMETER, TIMER, TIMEOUT)
    tank1.start(VALVE_DIAMETER)
    tank2.start(VALVE_DIAMETER)
