"""
SWaT physical process
"""

from constants import TANK_DIAMETER
from constants import VALVE_DIAMETER
from constants import TIMER
from constants import TIMEOUT
from constants import GRAVITATION
from constants import read_single_statedb
from constants import read_statedb
from constants import update_statedb
from constants import logger
from constants import select_value
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
    """
    Class defining a tank in the physical process.
    A Tank has:
    -FIT_in: list of input flows tags
    -MV: list of input of motorvalves tags controlling the FIT_in
    -LIT: tank level tag
    -P: list of output pumps tags
    -FIT_out: list of output flows tags
    -subprocess: number of subprocess in which the tank belongs
    -tank_number: id of the tank in the subprocess
    -diameter: tank diameter (m)
    -timer: period in which the tank has to actualize its values (s)
    -timeout: period of activity (s)
    """
    def __init__(self, FIT_in, MV, LIT, P, FIT_out, subprocess, tank_number, diameter, timer, timeout):
        """
        constructor
        """
        self.__FIT_in = FIT_in
        self.__MV = MV
        self.__LIT = LIT
        self.__P = P
        self.__FIT_out = FIT_out
        self.__subprocess = subprocess
        self.__id = tank_number
        self.__diameter = diameter
        self.__timer = timer
        self.__timeout = timeout
        self.__process = None
        logger.info('PP - tank number %d in subprocess %d created' % (self.__id, self.__subprocess))

    def __del__(self):
        """
        destructor
        """
        if(self.__process != None):
            self.__process.join()
        logger.info('PP - tank number %d in subprocess %d removed' % (self.__id, self.__subprocess))

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
        """
        Defines the action of a tank:
        -queries all the input, output and level tags values
        -computes the new flow level and the output flows
        -updates the database
        """
        input_flows = []
        input_valves = []
        if self.__P is not None:
            output_valves = []
        else:
            output_valves = None
            logger.warn('PP - tank number %d in subprocess %d has no output valves' % (self.__id, self.__subprocess))

        for index in self.__FIT_in:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_flows.append(select_value(value))
            else:
                logger.warn('PP - tank number %d in subprocess %d can\'t read %s' % (self.__id, self.__subprocess, index))

        for index in self.__MV:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_valves.append(select_value(value))
            else:
                logger.warn('PP - tank number %d in subprocess %d can\'t read %s' % (self.__id, self.__subprocess, index))

        if self.__P is not None:
            for index in self.__P:
                value = read_single_statedb(self.__subprocess, index)
                if value is not None:
                    output_valves.append(select_value(value))
                else:
                    logger.warn('PP - tank number %d in subprocess %d can\'t read %s' % (self.__id, self.__subprocess, index))

        current_flow = read_statedb(NAME=self.__LIT)
        logger.debug('PP - tank number %d in subprocess %d current flow: %f' % (self.__id, self.__subprocess, float(current_flow[0][3])))
        if current_flow is not None:
            if self.__FIT_out is not None:
                v = Toricelli(float(current_flow[0][3]))  # m/s
                flow = v * power(valve_diameter/2.0, 2) * pi * 3600.0  # m^3/h
                for index in self.__FIT_out:
                    update_statedb(flow, index)
                    logger.debug('PP - tank number %d in subprocess %d output flow: %f written into DB' % (self.__id, self.__subprocess, flow))
            else:
                logger.warn('PP - tank number %d in subprocess %d has no output flows' % (self.__id, self.__subprocess))
            new_flow = self.compute_new_flow_level(input_flows, input_valves, float(current_flow[0][3]), output_valves, valve_diameter)
            update_statedb(new_flow, self.__LIT)
            logger.debug('PP - tank number %d in subprocess %d new flow: %f written into DB' % (self.__id, self.__subprocess, new_flow))
        else:
            logger.warn('PP - tank number %d in subprocess %d can\'t read %s' % (self.__id, self.__subprocess, self.__LIT))

    def action_wrapper(self, valve_diameter):
        """
        Wraps the action() method
        """
        start_time = time()
        while(time() - start_time < self.__timeout):
            self.action(valve_diameter)
            sleep(self.__timer)

    def start(self, valve_diameter):
        """
        Runs the action() method
        """
        self.__process = Process(target = self.action_wrapper, args = (valve_diameter,))
        self.__process.start()
        logger.info('PP - tank number %d in subprocess %d started' % (self.__id, self.__subprocess))

if __name__ == '__main__':
    """
    Main function in order to be used as a independant script
    -constructs all the subprocess tanks
    -runs them in parallel
    """
    tank1 = Tank(['AI_FIT_101_FLOW'], ['DO_MV_101_OPEN'], 'AI_LIT_101_LEVEL', ['DO_P_101_START'], ['AI_FIT_201_FLOW'], 1, 1, TANK_DIAMETER, TIMER, TIMEOUT)
    tank2 = Tank(['AI_FIT_201_FLOW'], ['DO_MV_201_OPEN'], 'AI_LIT_301_LEVEL', None, None, 2, 1, TANK_DIAMETER, TIMER, TIMEOUT)
    tank1.start(VALVE_DIAMETER)
    tank2.start(VALVE_DIAMETER)
