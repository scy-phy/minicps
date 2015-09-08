"""
SWaT physical process
"""

from constants import TANK_DIAMETER
from constants import VALVE_DIAMETER
from constants import T_PP_R, T_PP_W
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
from math import pow
from math import pi

        
class Tank(object):
    """
    Class defining a tank in the physical process.
    """
    def __init__(self, fits_in, mvs, lit, pumps, fits_out,
                 subprocess, tank_number, diameter, height, period, timeout):
        """
        :fits_in: list of input flows tags
        :mvs: list of input of motorvalves tags controlling the fits_in
        :lit: tank level tag
        :pumps: list of output pumps tags
        :fits_out: list of output flows tags
        :subprocess: number of subprocess in which the tank belongs
        :tank_number: id of the tank in the subprocess
        :diameter: in meters
        :height: in meters
        :period: in which the tank has to actualize its values (s)
        :timeout: period of activity (s)
        """
        self.__fits_in = fits_in
        self.__mvs = mvs
        self.__lit = lit
        self.__pumps = pumps
        self.__fits_out = fits_out
        self.__subprocess = subprocess
        self.__id = tank_number
        self.__diameter = diameter
        self.__height = height
        self.__period = period
        self.__timeout = timeout
        self.__process = None

        logger.debug('PP - Tank: %d,%d created' % (self.__id, self.__subprocess))

        # if(self.__pumps is None):
        #     logger.warning('PP - Tank: %d,%d : no output valves' % (self.__id,
        #                                                          self.__subprocess))
        # if(self.__fits_out is None):
        #     logger.warning('PP - Tank: %d,%d has no output flows' % (self.__id,
        #                                                           self.__subprocess))

    def __del__(self):
        """
        destructor
        """
        if(self.__process is not None):
            self.__process.join()
        logger.info('PP - Tank: %d,%d removed' % (self.__id, self.__subprocess))

    def compute_new_water_level(self, fits, mvs,
                                current_level, pumps, valve_diameter):
        """
        fits: list of input flow values (m^3/h)
        mvs: list of boolean which tell if the valve is open or not
        current_level: current water level (m)
        pumps: list of output valves which tells if they are open or not
        tank_diameter: (m)
        valve_diameter: (m)
        period: physical process read/write 

        returns: new water level (m)
        """
        level = current_level
        volume = level * pi * pow((self.__diameter / 2.0), 2)
        for i in (0, len(fits) - 1):
            if mvs[i] != 0:
                # fits[i] is supposed to be in m^3/h and period in seconds
                volume += (self.__period * fits[i]) / 3600.0
        if pumps is not None:
            for i in (0, len(pumps) - 1):
                if int(pumps[i]) == 1:
                    volume -= (self.__period * P_XX) / 3600.0

        level = volume / (pi * pow((self.__diameter / 2.0), 2))

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

        if self.__pumps is not None:
            output_valves = []
        else:
            output_valves = None

        for index in self.__fits_in:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_flows.append(select_value(value))
            else:
                logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                                 self.__subprocess, index))

        for index in self.__mvs:
            value = read_single_statedb(self.__subprocess, index)
            if value is not None:
                input_valves.append(select_value(value))
            else:
                logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                                 self.__subprocess,
                                                                 index))

        if self.__pumps is not None:
            for index in self.__pumps:
                value = read_single_statedb(self.__subprocess, index)
                if value is not None:
                    output_valves.append(select_value(value))
                else:
                    logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                                     self.__subprocess,
                                                                     index))

        current_level = read_statedb(NAME=self.__lit)
        if current_level is not None:
            current_level = float(select_value(current_level[0])) / 1000.0
            logger.debug('PP - Tank: %d,%d current level: %f' % (self.__id,
                                                                 self.__subprocess,
                                                                 current_level))
            if self.__fits_out is not None:
                i = 0
                for index in self.__fits_out:
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
            update_statedb(str(new_level), self.__lit)
            logger.debug('PP - Tank: %d,%d %s -> %f written into DB' % (self.__id,
                                                                        self.__subprocess,
                                                                        self.__lit,
                                                                        new_level))
        else:
            logger.warning('PP - Tank: %d,%d can\'t read %s' % (self.__id,
                                                             self.__subprocess,
                                                             self.__lit))

    def action_wrapper(self, valve_diameter):
        """
        Wraps the action() method
        """
        start_time = time()
        while(time() - start_time < self.__timeout):
            self.action(valve_diameter)
            sleep(self.__period)

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

    rw_tank = Tank(['AI_FIT_101_FLOW'], ['DO_MV_101_OPEN'], 'AI_LIT_101_LEVEL',
                 ['DO_P_101_START'], ['AI_FIT_201_FLOW'], 1, 1, TANK_DIAMETER,
                 TANK_HEIGHT, T_PP_R, TIMEOUT)
    uf_tank = Tank(['AI_FIT_201_FLOW'], ['DO_MV_201_OPEN'], 'AI_LIT_301_LEVEL',
                 None, None, 1, 3, TANK_DIAMETER, TANK_HEIGHT, T_PP_R, TIMEOUT)

    rw_tank.start(VALVE_DIAMETER)
    uf_tank.start(VALVE_DIAMETER)
