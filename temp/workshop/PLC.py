from time import time
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

    def __init__(self, tags, ipaddr, directory, timer, timeout, filename, in_pump=Pump(), out_pump=Pump(), sensor=Sensor(), tank=Tank()):
        super(PLC, self).__init__(tags, ipaddr, directory, timer, timeout)
        self.__in_pump = in_pump
        self.__out_pump = out_pump
        self.__sensor = sensor
        self.__tank = tank

        self.__file = open(self._dir + filename, 'w')
        self.__file.write("{\n")

    def __del__(self):
        self.__file.write("}")
        self.__file.close()

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
        if(self.__sensor.height() - Tank.H_LVL < EPS):
            self.fill_tank()
        else:
            self.empty_tank()

    def action(self):
        self.circular_flow()
        h = self.__tank.tank_flow([self.__in_pump], [self.__out_pump], self.__sensor, self._timer)
        self.__sensor.actualize(h)
        in_open = bool_to_int(self.__in_pump.is_open())
        out_open = bool_to_int(self.__out_pump.is_open())

        self.__file.write("\t{\n")
        self.__file.write("\t\t\"flow\": " + str(self.__sensor.height()) + ",\n")
        self.__file.write("\t\t\"pumps\": [\n")
        self.__file.write("\t\t\t\"pump1\": " + str(in_open) + ",\n")
        self.__file.write("\t\t\t\"pump2\": " + str(out_open) + "\n")
        self.__file.write("\t\t],\n")
        self.__file.write("\t\t\"time\": " + str(time()) + "\n")
        self.__file.write("\t},\n")
        
        tag_in_pump = "%s=%d" % ("pump1", in_open)
        tag_out_pump = "%s=%d" % ("pump2", out_open)
        tag_sensor = "%s=%3.2f" % ("flow", self.__sensor.height())
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_in_pump)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_out_pump)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_sensor)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
