"""
SWaT physical process
"""

import sys
from multiprocessing import Process
from time import sleep, time
from math import pow, pi

from constants import logger
from constants import read_single_statedb, read_statedb, update_statedb, select_value
# TODO: move to utils
from constants import TANK_DIAMETER, PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT, TANK_HEIGHT
from constants import T_PP_R, T_PP_W, TIMEOUT


class Tank(object):
    """
    Class defining a tank in the physical process.

    # TODO: better docstring
    """
    def __init__(self, fits_in, mvs, lit, pumps, fits_out,
                 subprocess, tank_number, diameter, height, period, timeout):
        """
        :fits_in: list of input flows tags
        :mvs: list of input of motorvalves tags controlling the fits_in
        :lit: tank level tag
        :pumps: list of output pumps tags
        :fits_out: list of output flows tags
        :subprocess: swat subprocess number
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

    def __del__(self):
        if(self.__process is not None):
            self.__process.join()
        logger.info('PP - Tank%d0%d removed' % (self.__id, self.__subprocess))

    def compute_water_level(self, fits, mvs, level, pumps):
        """
        fits: list of input flow values (m^3/h)
        mvs: list of boolean which tell if the valve is open or not
        level: current water level (mm)
        pumps: list of output valves which tells if they are open or not

        returns: new water level (mm)
        """
        level /= 1000.0  # convert to m
        radius = self.__diameter / 2.0
        volume = level * pi * pow(radius , 2)
        for i in range(0, len(fits)):
            if mvs[i] == '1':
                # convert fits[i] from m^3/h into m^3/s
                volume += (self.__period * (fits[i] / 3600.0))

        if pumps is not None:
            for i in range(0, len(pumps)):
                if pumps[i] == '1':
                    volume -= (self.__period * (PUMP_FLOWRATE_OUT / 3600.0))

        new_level = volume / (pi * pow(radius, 2))

        if new_level <= 0.0:
            logger.error('PP - Tank%d0%d empty' % (self.__id,
                self.__subprocess))
            new_level = 0.0
        elif new_level >= self.__height:
            logger.error('PP - Tank%d0%d overflowed' % (self.__id,
                self.__subprocess))
            new_level = self.__height

        return new_level * 1000.0

    def action(self):
        """
        # TODO: rewrite a better doctring documenting each list
        Defines the action of a tank:
        -queries all the input, output and level tags values
        -computes the new flow level and the output flows
        -updates the database
        """

        # Acquire values from the statedb and save them in dedicated lists
        input_flows = []
        # FIXME: I don't like input_valves and output_valves names
        input_valves = []

        if self.__pumps is not None:
            output_valves = []
        else:
            output_valves = None

        water_level = 0.0  # mm
        new_water_level = 0.0  # mm
        delta_water_level = 0.0  # mm

        i = 0
        while i < len(self.__fits_in):

            fit_tuple = self.__fits_in[i]
            mv_tuple = self.__mvs[i]

            fit_record = read_single_statedb(fit_tuple[1], fit_tuple[0])
            if fit_record is not None:
                fit_value = select_value(fit_record)
                input_flows.append(float(fit_value))
            else:
                logger.warning('PP - tank%d0%d can\'t read %s' % (self.__id,
                                                                 self.__subprocess,
                                                                 fit_tuple[0]))

            mv_record = read_single_statedb(mv_tuple[1], mv_tuple[0])
            if mv_record is not None:
                mv_value = select_value(mv_record)
                input_valves.append(mv_value)
                # update FIT according to MV
                if mv_value == '0':
                    update_statedb('0.00', fit_tuple[0])
                else:
                    update_statedb(str(PUMP_FLOWRATE_IN), fit_tuple[0])

            else:
                logger.warning('PP - tank%d0%d can\'t read %s' % (self.__id,
                                                                 self.__subprocess,
                                                                 mv_tuple[0]))
            i += 1

        if self.__pumps is not None:
            for p_tuple in self.__pumps:
                p_record = read_single_statedb(p_tuple[1], p_tuple[0])
                if p_record is not None:
                    output_valves.append(select_value(p_record))
                else:
                    logger.warning('PP - tank%d0%d can\'t read %s' % (self.__id,
                                                                     self.__subprocess,
                                                                     p_tuple[0]))

        water_level = read_single_statedb(self.__lit[1], self.__lit[0])
        if water_level is not None:
            water_level = float(select_value(water_level))
            # log the value in mm to be consistent with the db
            logger.debug('PP - tank%d0%d read_db %s: %f' % (self.__id,
                                                                 self.__subprocess,
                                                                 self.__lit[0],
                                                                 water_level))

            if self.__fits_out is not None:
                i = 0
                for fit_tuple in self.__fits_out:
                    if output_valves[i] != '0':
                        update_statedb(str(PUMP_FLOWRATE_OUT), fit_tuple[0])
                        logger.debug('PP - tank%d0%d write_db %s: %f' % (self.__id, self.__subprocess,
                                                                          fit_tuple[0], PUMP_FLOWRATE_OUT))
                    else:
                        update_statedb('0.00', fit_tuple[0])
                        logger.debug('PP - tank%d0%d write_db %s: 0.00' % (self.__id, self.__subprocess,
                                                                          fit_tuple[0]))
                    i += 1

            new_water_level = self.compute_water_level(input_flows, input_valves,
                                                     water_level, output_valves)
            update_statedb(str(new_water_level), self.__lit[0])
            delta_water_level = new_water_level - water_level
            logger.debug('PP - tank%d0%d write_db %s: %f    delta: %f mm' % (self.__id, self.__subprocess,
                                                              self.__lit[0],
                                                              new_water_level,
                                                              delta_water_level))
        else:
            logger.warning('PP - tank%d0%d can\'t read_db %s' % (self.__id,
                                                             self.__subprocess,
                                                             self.__lit[0]))

    def action_wrapper(self):
        """
        Wraps the action() method
        """
        start_time = time()

        while(time() - start_time < self.__timeout):
            try:
                self.action()
                sleep(self.__period)

            except Exception, e:
                print repr(e)
                sys.exit(1)

    def start(self):
        """
        Runs the action() method
        """
        self.__process = Process(target=self.action_wrapper)
        self.__process.start()

        logger.info('PP - tank%d0%d active' % (self.__id, self.__subprocess))


if __name__ == '__main__':
    """
    Main function in order to be used as a independant script
    -constructs all the subprocess tanks
    -runs them in parallel
    """
    sleep(3)

    rw_tank = Tank(
                [('AI_FIT_101_FLOW', '1')],
                [('DO_MV_101_OPEN', '1')],
                ('AI_LIT_101_LEVEL', '1'),
                [('DO_P_101_START', '1')],
                [('AI_FIT_201_FLOW', '2')],
                1, 1,
                TANK_DIAMETER, TANK_HEIGHT,
                T_PP_R, TIMEOUT)

    uf_tank = Tank(
                [('AI_FIT_201_FLOW', '2')],
                [('DO_MV_201_OPEN', '2')],
                ('AI_LIT_301_LEVEL', '3'),
                None,  # No pump
                None,  # No output flowmeter
                1, 3,
                TANK_DIAMETER, TANK_HEIGHT,
                T_PP_R, TIMEOUT)

    rw_tank.start()
    uf_tank.start()
