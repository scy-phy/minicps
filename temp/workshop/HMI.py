from ICS import ICS
from time import time
from Utils import parse # parse function read a string and extract all numbers (integers or floats)
import abc
import matplotlib
# matplotlib.use('pdf')
import matplotlib.pyplot as plt
import subprocess

class HMI(ICS):
    """
    This class represents a HMI machine, subclass of a ICS machine
    HMI machine is designed to monitor ENIP servers and draw the graphs representing flow level and pump actions in function of time
    """
    def __init__(self, tags, ipaddr, directory, timer, timeout, output_file_name):
        """
        Constructor calling the super (ICS) constructor
        Lists are here to record data and a file in order to save the graphs
        """
        super(HMI, self).__init__(tags, ipaddr, directory, timer, timeout)
        self.__file_name = output_file_name
        self.__in_pump = []
        self.__out_pump = []
        self.__flow = []
        self.__x = []

    def __del__(self):
        """
        The destructor computes and saves the graphs
        """
        # Three subplots sharing x axe
        f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

        # The pump has only two values 0 and 1
        ax2.set_ylim([-0.5, 1.5])
        ax3.set_ylim([-0.5, 1.5])
        
        ax3.set_xlabel('Time (s)')
        ax1.set_ylabel('Flow level (cm)')
        ax2.set_ylabel('In pump')
        ax3.set_ylabel('Out pump')

        ax1.set_title('Flow level and pumps reactions')

        ax1.scatter(self.__x, self.__flow, color='b')
        ax2.plot(self.__x, self.__in_pump, color='g')
        ax3.plot(self.__x, self.__out_pump, color='r')
        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        f.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        # Save the file
        plt.savefig(self.__file_name, bbox_inches='tight')

    def action(self):
        """
        Implements abstract method
        The action for a HMI is to query a ENIP server, on the IP adress passed in the contructor
        Then the HMI records the tag values in lists
        """
        for tag_name in self._tags:
            # query for the tag value
            proc = subprocess.Popen(["python -m cpppo.server.enip.client -p -a %s %s" % (self._ipaddr, tag_name)], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            # parse the output of the subprocess
            ret = parse(str(out))

            # append the values in the set
            if(tag_name == "pump1"):
                self.__in_pump.append(ret[1])
            elif(tag_name == "pump2"):
                self.__out_pump.append(ret[1])
            elif(tag_name == "flow"):
                self.__flow.append(ret[0])
                self.__x.append(time())
