"""
SWaT sub1 physical process
"""

# TODO: use subprocess
from minicps.devices import Tank
from time import sleep, time
from math import pow, pi
from utils import TANK_DIAMETER, PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_HEIGHT, TANK_SECTION
from utils import T_PP_R, T_PP_W, TIMEOUT, LIT_101
from utils import STATE

import sys


class Tank(object):

    """Tank in the physical process."""

    def __init__(self, fits_in, mvs, lit, pumps, fits_out,
                 subprocess, _id, diameter, height, period, timeout):
        """
        :fits_in: list of input flows tags
        :mvs: list of input of motorvalves tags controlling the fits_in
        :lit: tank level tag
        :pumps: list of output pumps tags
        :fits_out: list of output flows tags
        :subprocess: swat subprocess number
        :_id: id of the tank in the subprocess
        :diameter: in meters
        :height: in meters
        :period: in which the tank has to actualize its values (s)
        :timeout: period of activity (s)
        """
        self._fits_in = fits_in
        self._mvs = mvs
        self._lit = lit
        self._pumps = pumps
        self._fits_out = fits_out
        self._subprocess = subprocess
        self._id = _id
        self._diameter = diameter
        self._height = height
        self._period = period
        self._timeout = timeout
        self._process = None

    def __del__(self):
        if(self._process is not None):
            self._process.join()
        logger.info('PP - Tank%d0%d removed' % (self._id, self._subprocess))

    def compute_water_level(self, fits, mvs, level, pumps):
        """
        :fits: list of input flow values (m^3/h)
        :mvs: list of boolean which tell if the valve is open or not
        :level: current water level (mm)
        :pumps: list of output valves which tells if they are open or not

        returns: new water level (mm)
        """
        level /= 1000.0  # convert to m
        radius = self._diameter / 2.0
        volume = level * pi * pow(radius , 2)
        for i in range(0, len(fits)):
            if mvs[i] == '1':
                # convert fits[i] from m^3/h into m^3/s
                volume += (self._period * (fits[i] / 3600.0))

        if pumps is not None:
            for i in range(0, len(pumps)):
                if pumps[i] == '1':
                    volume -= (self._period * (PUMP_FLOWRATE_OUT / 3600.0))

        new_level = volume / (pi * pow(radius, 2))

        if new_level <= 0.0:
            logger.error('PP - Tank%d0%d empty' % (self._id,
                self._subprocess))
            new_level = 0.0
        elif new_level >= self._height:
            logger.error('PP - Tank%d0%d overflowed' % (self._id,
                self._subprocess))
            new_level = self._height

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

        if self._pumps is not None:
            output_valves = []
        else:
            output_valves = None

        water_level = 0.0  # mm
        new_water_level = 0.0  # mm
        delta_water_level = 0.0  # mm

        i = 0
        while i < len(self._fits_in):

            fit_tuple = self._fits_in[i]
            mv_tuple = self._mvs[i]

            fit_record = read_single_statedb(fit_tuple[1], fit_tuple[0])
            if fit_record is not None:
                fit_value = select_value(fit_record)
                input_flows.append(float(fit_value))
            else:
                logger.warning('PP - tank%d0%d can\'t read %s' % (self._id,
                                                                 self._subprocess,
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
                logger.warning('PP - tank%d0%d can\'t read %s' % (self._id,
                                                                 self._subprocess,
                                                                 mv_tuple[0]))
            i += 1

        if self._pumps is not None:
            for p_tuple in self._pumps:
                p_record = read_single_statedb(p_tuple[1], p_tuple[0])
                if p_record is not None:
                    output_valves.append(select_value(p_record))
                else:
                    logger.warning('PP - tank%d0%d can\'t read %s' % (self._id,
                                                                     self._subprocess,
                                                                     p_tuple[0]))

        water_level = read_single_statedb(self._lit[1], self._lit[0])
        if water_level is not None:
            water_level = float(select_value(water_level))
            # log the value in mm to be consistent with the db
            logger.debug('PP - tank%d0%d read_db %s: %f' % (self._id,
                                                                 self._subprocess,
                                                                 self._lit[0],
                                                                 water_level))

            if self._fits_out is not None:
                i = 0
                for fit_tuple in self._fits_out:
                    if output_valves[i] != '0':
                        update_statedb(str(PUMP_FLOWRATE_OUT), fit_tuple[0])
                        logger.debug('PP - tank%d0%d write_db %s: %f' % (self._id, self._subprocess,
                                                                          fit_tuple[0], PUMP_FLOWRATE_OUT))
                    else:
                        update_statedb('0.00', fit_tuple[0])
                        logger.debug('PP - tank%d0%d write_db %s: 0.00' % (self._id, self._subprocess,
                                                                          fit_tuple[0]))
                    i += 1

            new_water_level = self.compute_water_level(input_flows, input_valves,
                                                     water_level, output_valves)
            update_statedb(str(new_water_level), self._lit[0])
            delta_water_level = new_water_level - water_level
            logger.debug('PP - tank%d0%d write_db %s: %f    delta: %f mm' % (self._id, self._subprocess,
                                                              self._lit[0],
                                                              new_water_level,
                                                              delta_water_level))
        else:
            logger.warning('PP - tank%d0%d can\'t read_db %s' % (self._id,
                                                             self._subprocess,
                                                             self._lit[0]))

    def action_wrapper(self):
        """
        Wraps the action() method
        """
        start_time = time()

        while(time() - start_time < self._timeout):
            try:
                self.action()
                sleep(self._period)

            except Exception, e:
                print repr(e)
                sys.exit(1)

    def start(self):
        """
        Runs the action() method
        """
        self._process = Process(target=self.action_wrapper)
        self._process.start()

        logger.info('PP - tank%d0%d active' % (self._id, self._subprocess))

PERIOD_SEC = 0.5  # physical process sampling rate in sec
PERIOD_HOURS = PERIOD_SEC / 3600.0
MV101 = ('MV101', 1)
P101 = ('P101', 1)


class RawWaterTank(Tank):

    def main_loop(self, sleep=PERIOD_SEC):

        new_level = self.level

        mv101 = self.get(MV101)
        if int(mv101) == 1:
            inflow = PUMP_FLOWRATE_IN * PERIOD_HOURS
            print "DEBUG RawWaterTank inflow: ", inflow
            new_level += inflow

        p101 = self.get(P101)
        if int(p101) == 1:
            outflow = PUMP_FLOWRATE_OUT * PERIOD_HOURS
            print "DEBUG RawWaterTank outflow: ", outflow
            new_level -= outflow

        self.level = new_level


if __name__ == '__main__':

    rwt = RawWaterTank(
        name='rwt',
        state=STATE,
        protocol=None,

        section=TANK_SECTION,
        level=500.0
    )
