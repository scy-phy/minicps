import subprocess
import sys
from Pump import Pump
from Sensor import Sensor
from Tank import Tank
from Utils import bool_to_int
from Utils import EPS
import abc
from ICS import ICS

class PLC(ICS):

    def __init__(self, tags, ipaddr, timer, timeout, in_pump_filename, out_pump_filename, sensor_filename, in_pump=Pump(), out_pump=Pump(), sensor=Sensor(), tank=Tank()):
        super(PLC, self).__init__(tags, ipaddr, timer, timeout)
        self.__in_pump = in_pump
        self.__out_pump = out_pump
        self.__sensor = sensor
        self.__tank = tank

        self.__in_pump_file = open(in_pump_filename, 'w')
        self.__out_pump_file = open(out_pump_filename, 'w')
        self.__sensor_file = open(sensor_filename, 'w')

    def __del__(self):
        self.__in_pump_file.close()
        self.__out_pump_file.close()
        self.__sensor_file.close()

    def fill_tank(self):
        self.__in_pump.open()
        self.__out_pump.close()

    def empty_tank(self):
        self.__in_pump.close()
        self.__out_pump.open()

    def hold_tank(self):
        self.__in_pump.close()
        self.__out_pump.close()

    def circular_flow(self):
        if(self.__sensor.height() - Tank.HH_LVL < EPS):
            self.fill_tank()
        else:
            self.empty_tank()

    def action(self):
        self.circular_flow()
        h = self.__tank.tank_flow([self.__in_pump], [self.__out_pump], self.__sensor, self._timer)
        self.__sensor.actualize(h)
        in_open = bool_to_int(self.__in_pump.is_open())
        out_open = bool_to_int(self.__out_pump.is_open())
        
        self.__in_pump_file.write(str(in_open) + '\n')
        self.__out_pump_file.write(str(out_open) + '\n')
        self.__sensor_file.write(str(self.__sensor.height()) + '\n')

        print in_open
        print out_open
        print self.__sensor.height()
        tag_in_pump = "%s=%d" % (self._tags["pump1"], in_open)
        tag_out_pump = "%s=%d" % (self._tags["pump2"], out_open)
        tag_sensor = "%s=%3.2f" % (self._tags["flow"], self.__sensor.height())
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_in_pump)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_out_pump)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_sensor)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

def main():
    tags = {}
    tags["flow"] = "REAL"
    tags["pump1"] = "INT"
    tags["pump2"] = "INT"
    plc = PLC(tags, "192.168.1.10", 1, 120, "in.lol", "out.lol", "sens.lol")
    plc.run()

if __name__ == '__main__':
    main()
