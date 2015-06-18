from ICS import ICS
from Pump import Pump
from Sensor import Sensor
from Tank import Tank
from time import time
from Utils import bool_to_int
from Utils import EPS
import abc
import subprocess
import sys

class PLC(ICS):
    """
    This class represents a HMI machine, subclass of a ICS machine
    HMI machine is designed to monitor ENIP servers and draw the graphs representing flow level and pump actions in function of time
    """
    def __init__(self, tags, ipaddr, directory, timer, timeout, filename, in_pump=Pump(), out_pump=Pump(), sensor=Sensor(), tank=Tank()):
        """
        Constructor calling the super (ICS) constructor
        A PLC also has two pumps, a sensor and a tank
        It records all the outputs in a json file
        """
        super(PLC, self).__init__(tags, ipaddr, directory, timer, timeout)
        self.__in_pump = in_pump
        self.__out_pump = out_pump
        self.__sensor = sensor
        self.__tank = tank
        self.__increase = True

        self.__file = open(self._dir + filename, 'w')
        self.__file.write("{\n")

    def __del__(self):
        """
        The destructor closes the file
        """
        self.__file.write("}")
        self.__file.close()

    def fill_tank(self):
        """
        Opens the incoming flow and closes the outgoing one
        """
        self.__in_pump.open()
        self.__out_pump.close()

    def empty_tank(self):
        """
        Closes the incoming flow and opens the outgoing one
        """
        self.__in_pump.close()
        self.__out_pump.open()

    def hold_tank(self):
        """
        Close all the flows
        """
        self.__in_pump.close()
        self.__out_pump.close()

    def maintain_level(self, level):
        """
        Maintain the flow level to the level given opening and closing pumps
        """
        if(self.__sensor.height() - level < EPS):
            self.fill_tank()
        else:
            self.empty_tank()

    def circular_flow(self, high, low, increase):
        if(increase and (self.__sensor.height() - high < EPS)):
            self.fill_tank()
            print "ici"
            return increase
        elif(increase and (self.__sensor.height() - high >= EPS)):
            self.empty_tank()
            print "da"
            return False
        elif(not increase and (self.__sensor.height() - low < EPS)):
            self.fill_tank()
            print "here"
            return True
        elif(not increase and (self.__sensor.height() - low >= EPS)):
            self.empty_tank()
            print "poule"
            return increase
        
    def action(self):
        """
        The PLC action is:
        To change the state of its pumps according to the current flow level
        To write the pump actions and the flow level in the json file
        To updates its ENIP server values
        """
        # Flow order
        # self.maintain_level(Tank.H_LVL)
        
        self.__increase = self.circular_flow(Tank.H_LVL, Tank.L_LVL, self.__increase)
        # Computes the new flow level
        h = self.__tank.tank_flow([self.__in_pump], [self.__out_pump], self.__sensor, self._timer)
        self.__sensor.actualize(h)
        in_open = bool_to_int(self.__in_pump.is_open())
        out_open = bool_to_int(self.__out_pump.is_open())

        # Writes the file
        self.__file.write("\t{\n")
        self.__file.write("\t\t\"flow\": " + str(self.__sensor.height()) + ",\n")
        self.__file.write("\t\t\"pumps\": [\n")
        self.__file.write("\t\t\t\"pump1\": " + str(in_open) + ",\n")
        self.__file.write("\t\t\t\"pump2\": " + str(out_open) + "\n")
        self.__file.write("\t\t],\n")
        self.__file.write("\t\t\"time\": " + str(time()) + "\n")
        self.__file.write("\t},\n")

        # Updates the ENIP server
        tag_in_pump = "%s=%d" % ("pump1", in_open)
        tag_out_pump = "%s=%d" % ("pump2", out_open)
        tag_sensor = "%s=%3.2f" % ("flow", self.__sensor.height())
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_in_pump)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_out_pump)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc = subprocess.Popen(["python -m cpppo.server.enip.client -a %s %s" % (self._ipaddr, tag_sensor)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
