import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import subprocess
import abc
from ICS import ICS
from time import time
from Utils import parse

class HMI(ICS):

    def __init__(self, tags, ipaddr, timer, timeout, output_file_name):
        super(HMI, self).__init__(tags, ipaddr, timer, timeout)
        self.__file_name = output_file_name
        self.__in_pump = []
        self.__out_pump = []
        self.__flow = []
        self.__x = []


    def __del__(self):
        # computes and saves the graph
        # Three subplots sharing both x/y axes
        f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
        ax1.scatter(self.__x, self.__flow, color='b')
        ax2.plot(self.__x, self.__in_pump, color='g')
        ax3.plot(self.__x, self.__out_pump, color='r')
        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        f.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        plt.savefig(self.__file_name, bbox_inches='tight')

    def action(self):
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
