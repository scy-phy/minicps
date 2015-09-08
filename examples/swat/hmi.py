"""
HMI Class
"""

import matplotlib
matplotlib.use('Agg')  # Agg backend to use matplotlib without X server

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
from constants import P1_PLC1_TAGS, LIT_101, LIT_301, FIT_201, T_HMI_R, TIMEOUT
from constants import read_cpppo
from constants import L1_PLCS_IP


def set_delta(y_min, y_max, subplot, size):
    """
    Compute y axis limits for a subplot
    """
    if(y_min != y_max):
        delta = size * (y_max - y_min)
        subplot.set_ylim([y_min - delta, y_max + delta])


class HMI(object):
    """
    Class defining the Human-Machine Interface
    An HMI object has to query a list of tags from a PLC ENIP server,
    and log it into a .png file that will be served by a webserver.
    """
    id = 1  # class variable

    def __init__(self, tags, ipaddr, filename, timer, timeout):
        """
        :tags: the ENIP tags to query
        :ipaddr: the IP address of thr PLC to query
        :filename: the name of the .png file
        :timer: period in which the HMI has to query the tags (s)
        :timeout: period of activity (s)
        """
        self.__tags = tags
        self.__ipaddr = ipaddr
        self.__id = HMI.id
        HMI.id += 1
        self.__filename = filename
        self.__timer = timer
        self.__timeout = timeout
        self.__process = None  # save the HMI PID to kill it later

        self.__values = {}  # dict of lists, keys are tagnames
        for tag in tags:
            self.__values[tag] = []
        self.__values['time'] = []  # special list

        self.__http = None  # save the HTTP server PID to kill it later
        logger.debug('Created HMI %d that will monitor [%s]' % (self.__id, ', '.join(map(str, self.__tags))))

    def __del__(self):
        """
        destructor
        """
        # kill the HMI (opened with Process)
        if(self.__process is not None):
            self.__process.join()

    
        # kill the HTTP server (opened with Popen)
        self.stop_http_server()

        logger.debug('Killed HMI and its webserver' % self.__id)

    def start_http_server(self, port):
        """
        Starts a simple http server on a choosen port
        """
        if(self.__http is None):
            cmd = "python -m SimpleHTTPServer %d" % port
            try:
                self.__http = Popen(cmd, preexec_fn=setsid)
                logger.info('HMI %d - HTTP server started' % self.__id)

            except OSError:
                logger.warning('HMI %d - HTTP server cannot start' % self.__id)

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
        Callback method, writes the three subplots in the .png file using the
        Matplotlib canvas backend.
        """

        # create len(self.__tags_ subplots, sharing the x axis 
        fig, subplots = plt.subplots(len(self.__tags), sharex=True)

        # with canvans you can update the fig in real-time
        canvas = FigureCanvas(fig)

        for i in range(0, len(subplots)):
            y_min = min(self.__values[self.__tags[i]])
            y_max = max(self.__values[self.__tags[i]])
            set_delta(y_min, y_max, subplots[i], 0.05)

        # set time as a comming x axis
        subplots[len(subplots) - 1].set_xlabel('Time (s)')

        for i in range(0, len(subplots)):
            subplots[i].set_ylabel(self.__tags[i])

        subplots[0].set_title('HMI %d' % self.__id)

        for i in range(0, len(subplots)):
            # scatter use points
            subplots[i].scatter(self.__values['time'], self.__values[self.__tags[i]], color='r')

        # save file
        canvas.print_figure('examples/swat/hmi/%s' % self.__filename)

        plt.close(fig)

    def action_wrapper(self):
        """
        Wraps the action() method
        """
        start_time = time()
        while(time() - start_time < self.__timeout):

            try:
                self.action()
                sleep(self.__timer)

            except Exception, e:
                print repr(e)
                sys.exit(1)


    def action(self):
        """
        Defines the action of the HMI:
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
        self.__process = Process(target=self.action_wrapper)
        self.__process.start()
        logger.info('HMI %d started' % self.__id)


if __name__ == '__main__':
    """
    Main function, creating an HMI object, which queries some tags from
    the Raw water tank:
        - water level
        - input Motor Valve
        - output pump

    The values are displayed in real-time in a pop-up window and the same
    image is served through a webserver that can be reached at 192.168.1.100
    """

    hmi = HMI(['HMI_MV101-Status', 'HMI_LIT101-Pv', 'HMI_P101-Status'],
            L1_PLCS_IP['plc1'], 'plc1.png', T_HMI_R, TIMEOUT)

    sleep(3)

    hmi.start()
    hmi.start_http_server(80)

    hmi.stop_http_server()
