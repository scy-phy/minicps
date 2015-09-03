"""
HMI Class
"""

import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from time import time
from time import sleep
from subprocess import Popen
from multiprocessing import Process
from os import setsid
from os import kill
from os import killpg
from signal import SIGTERM
from constants import logger
from constants import P1_PLC1_TAGS, LIT_101, LIT_301, FIT_201, PLC_NUMBER, TIMER, TIMEOUT
from constants import read_cpppo
from constants import L1_PLCS_IP

# FIXME: Pierre if you want a generic class use a list of tags instead of 3
# tags because you can potentially display any number of tags

def set_delta(values, index, axis, size):
    mini = min(values[index])
    maxi = max(values[index])
    if(mini != maxi):
        delta = size * (maxi - mini)
        axis.set_ylim([mini - delta, maxi + delta])

class HMI:
    """
    Class defining the Human-Machine Interface
    An HMI object has to query 3 tags from a PLC address, and log it into a .svg
    file. This .svg file is also available in a webserver started by the HMI.
    tags: the ENIP tags to query
    ipaddr: the IP address of thr PLC to query
    filename: the name of the .svg file
    timer: period in which the HMI has to query the tags (s)
    timeout: period of activity (s)
    """

    """
    Class variables
    """
    HMI_id = 1

    def __init__(self, tags, ipaddr, filename, timer, timeout):
        """
        constructor
        """
        self.__tags = tags
        self.__ipaddr = ipaddr
        self.__id = HMI.HMI_id
        HMI.HMI_id += 1
        self.__file = filename
        self.__timer = timer
        self.__timeout = timeout
        self.__process = None
        self.__values = {}
        for index in tags:
            self.__values[index] = []
        self.__values['time'] = []
        self.__http = None
        logger.info('Created HMI %d that will monitor [%s]' % (self.__id, ', '.join(map(str, self.__tags))))

    def __del__(self):
        """
        destructor
        """
        if(self.__process is not None):
            self.__process.join()
        if(self.__http is not None):
            kill(self.__http, SIGKILL)
            self.__http = None
        logger.info('HMI %d removed' % self.__id)

    def start_http_server(self, port):
        """
        Starts a simple http server on a choosen port
        """
        if(self.__http is None):
            cmd = "python -m SimpleHTTPServer %d" % port
            try:
                self.__http = Popen(cmd, preexec_fn=setsid)
            except OSError:
                logger.warning('HMI %d - HTTP server cannot start' % self.__id)
            logger.info('HMI %d - HTTP server started' % self.__id)

    def stop_http_server(self):
        """
        Kills the HTTP server
        """
        if(self.__http is not None):
            killpg(getpgid(self.__http.pid), SIGTERM)
            logger.info('HMI %d - HTTP server stopped' % self.__id)
            self.__http = None

    def callback(self):
        """
        Callback method, writes the three subplots in the .svg file using the
        Matplotlib canvas backend.
        """
        fig, axes = plt.subplots(len(self.__tags), sharex=True)
        canvas = FigureCanvas(fig)

        for i in range(0, len(axes)):
            set_delta(self.__values, self.__tags[i], axes[i], 0.05)

        axes[len(axes) - 1].set_xlabel('Time (s)')

        for i in range(0, len(axes)):
            axes[i].set_ylabel(self.__tags[i])

        axes[0].set_title('HMI %d' % self.__id)

        for i in range(0, len(axes)):
            axes[i].scatter(self.__values['time'], self.__values[self.__tags[i]], color='r')

        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        canvas.print_figure('examples/swat/hmi/%s' % self.__file)
        logger.debug(self.__values)
        plt.close(fig)


    def action_wrapper(self):
        """
        Wraps the action() method
        """
        start_time = time()
        while(time() - start_time < self.__timeout):
            self.action()
            sleep(self.__timer)

    def action(self):
        """
        Defines the action action of the HMI:
        -reads the tags using the cpppo helper function
        and add them to different lists
        -append the time value to another list
        -calls the callback function
        """
        for index in self.__tags:
            tag = read_cpppo(self.__ipaddr, index, 'examples/swat/hmi_cpppo.cache')
            logger.debug('HMI %d read %s: %s' % (self.__id, index, tag))
            tag = float(tag)
            self.__values[index].append(tag)

        self.__values['time'].append(time())

        self.callback()


    def start(self):
        """
        Runs the action() method
        """
        self.__process = Process(target = self.action_wrapper)
        self.__process.start()
        logger.info('HMI %d started' % self.__id)

if __name__ == '__main__':
    """
    Main function, creating 1 HMI object, which queries:
    -the Tank 1 water level
    -the Tank 1 input Motor Valve
    -the Tank 1 output pump
    Then it starts the HMI HTTP server and start its action
    """
    hmi1 = HMI( ['HMI_MV101-Status', 'HMI_LIT101-Pv', 'HMI_P101-Status'], L1_PLCS_IP['plc1'], 'plc1.png', TIMER, TIMEOUT)
    hmi1.start_http_server(80)
    sleep(3)
    hmi1.start()
    hmi1.stop_http_server()
