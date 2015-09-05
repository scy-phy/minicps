"""
SWaT physical process
"""

from constants import TANK_DIAMETER
from constants import VALVE_DIAMETER
from constants import TIMER
from constants import TIMEOUT
from constants import P_XX
from constants import TANK_HEIGHT
from constants import read_single_statedb
from constants import read_statedb
from constants import update_statedb
from constants import logger
from constants import select_value
from multiprocessing import Process
from time import sleep
from time import time
from math import pow as power
from math import pi

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
    def __init__(self, FIT_in, MV, LIT, P, FIT_out,
                 subprocess, tank_number, diameter, height, timer, timeout):
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
        self.__height = height / 1000.0  # convert to m
        self.__timer = timer
        self.__timeout = timeout
        self.__process = None
        logger.info('PP - Tank: %d,%d created' % (self.__id, self.__subprocess))
        if(self.__P is None):
            logger.warning('PP - Tank: %d,%d : no output valves' % (self.__id,
                                                                 self.__subprocess))
        if(self.__FIT_out is None):
            logger.warning('PP - Tank: %d,%d has no output flows' % (self.__id,
                                                                  self.__subprocess))


    def __del__(self):
        """
        destructor
        """
        if(self.__process is not None):
            self.__process.join()
        logger.info('PP - Tank: %d,%d removed' % (self.__id, self.__subprocess))

    def compute_new_water_level(self, FIT_list, MV_list,
                                current_level, P_list, valve_diameter):
        """
        FIT_list: list of input flow values (m^3/h)
        MV_list: list of boolean which tell if the valve is open or not
        current_level: current water level (m)
        P_list: list of output valves which tells if they are open or not
        tank_diameter: (m)
        valve_diameter: (m)
        timer: period in which the water level is computed (s)

        returns: new water level (m)
        """
        level = current_level
        volume = level * pi * power((self.__diameter / 2.0),2)
        for i in (0, len(FIT_list) - 1):
            if MV_list[i] != 0:
                # FIT_list[i] is supposed to be in m^3/h and timer in seconds
                volume += (self.__timer * FIT_list[i]) / 3600.0
        if P_list is not None:
            for i in (0, len(P_list) - 1):
                if int(P_list[i]) == 1:
                    volume -= (self.__timer * P_XX) / 3600.0

        level = volume / (pi * power((self.__diameter / 2.0),2))
        if level <= 0.0:
            logger.error('PP - Tank: %d,%d empty' % (self.__id,
                self.__subprocess))
            level = 0.0
        elif level >= self.__height:
            logger.error('PP - Tank: %d,%d overflowed' % (self.__id,
                self.__subprocess))
            level = self.__height
        return level

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

        for index in self.__FIT_in:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_flows.append(select_value(value))
            else:
                logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                                 self.__subprocess, index))

        for index in self.__MV:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_valves.append(select_value(value))
            else:
                logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                                 self.__subprocess,
                                                                 index))

        if self.__P is not None:
            for index in self.__P:
                value = read_single_statedb(self.__subprocess, index)
                if value is not None:
                    output_valves.append(select_value(value))
                else:
                    logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                                     self.__subprocess,
                                                                     index))

        current_level = read_statedb(NAME=self.__LIT)
        if current_level is not None:
            current_level = float(select_value(current_level[0])) / 1000.0
            logger.debug('PP - Tank: %d,%d current level: %f' % (self.__id,
                                                                 self.__subprocess,
                                                                 current_level))
            if self.__FIT_out is not None:
                i = 0
                for index in self.__FIT_out:
                    if output_valves[i] != 0:
                        update_statedb(str(P_XX), index)
                        logger.debug('PP - Tank: %d,%d %s -> %f written into DB' % (self.__id,
                                                                                    self.__subprocess,
                                                                                    index,
                                                                                    P_XX))
                    else:
                        update_statedb(str(0.0), index)
                        logger.debug('PP - Tank: %d,%d %s -> 0.0 written into DB' % (self.__id,
                                                                                    self.__subprocess,
                                                                                    index))
                    i += 1
            new_level = self.compute_new_water_level(input_flows, input_valves,
                                                     current_level, output_valves,
                                                     valve_diameter)
            new_level *= 1000.0 # convert m to mm
            update_statedb(str(new_level), self.__LIT)
            logger.debug('PP - Tank: %d,%d %s -> %f written into DB' % (self.__id,
                                                                        self.__subprocess,
                                                                        self.__LIT,
                                                                        new_level))
        else:
            logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                             self.__subprocess,
                                                             self.__LIT))

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
        self.__process = Process(target = self.action_wrapper,
                                 args = (valve_diameter,))
        self.__process.start()
        logger.info('PP - Tank: %d,%d started' % (self.__id, self.__subprocess))

if __name__ == '__main__':
    """
    Main function in order to be used as a independant script
    -constructs all the subprocess tanks
    -runs them in parallel
    """
    tank1 = Tank(['AI_FIT_101_FLOW'], ['DO_MV_101_OPEN'], 'AI_LIT_101_LEVEL',
                 ['DO_P_101_START'], ['AI_FIT_201_FLOW'], 1, 1, TANK_DIAMETER,
                 TANK_HEIGHT, TIMER, TIMEOUT)
    tank2 = Tank(['AI_FIT_201_FLOW'], ['DO_MV_201_OPEN'], 'AI_LIT_301_LEVEL',
                 None, None, 2, 1, TANK_DIAMETER, TANK_HEIGHT, TIMER, TIMEOUT)

    tank1.start(VALVE_DIAMETER)
    tank2.start(VALVE_DIAMETER)
