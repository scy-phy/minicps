"""
HMI Class

Data objects coming from subprocess, os and signal modules are used to manage
an http server subprocess that is launched and killed by hmi.py process.
"""

import sys

import matplotlib
matplotlib.use('Agg')  # Agg backend to use matplotlib without X server
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from time import time, sleep

from subprocess import Popen
from os import setsid, kill, killpg, getpgid
from signal import SIGTERM

from multiprocessing import Process

from constants import logger
from constants import P1_PLC1_TAGS, LIT_101, LIT_301, FIT_201
from constants import T_HMI_R, TIMEOUT, DISPLAYED_SAMPLES
from constants import read_cpppo
from utils import L1_PLCS_IP


def set_delta(y_min, y_max, subplot, size):
    """Compute y axis limits for a subplot."""
    if(y_min != y_max):
        delta = size * (y_max - y_min)
        subplot.set_ylim([y_min - delta, y_max + delta])


class HMI(object):
    """Human-Machine Interface class.

    An HMI object has to query a list of tags from a PLC ENIP server,
    and log it into a .png file that will be served by a webserver.
    """

    id = 0  # count the number of instances

    def __init__(self, tags, ipaddr, filename, timer, timeout):
        """
        :tags: the ENIP tags to query
        :ipaddr: the IP address of thr PLC to query
        :filename: the name of the .png file
        :timer: period in which the HMI has to query the tags (s)
        :timeout: period of activity (s)
        """
        HMI.id += 1
        self.__id = HMI.id

        self.__tags = tags
        self.__ipaddr = ipaddr
        self.__filename = filename
        self.__timer = timer
        self.__timeout = timeout

        self.__start_time = 0.0
        self.__process = None  # save the HMI PID to kill it later

        # dict of lists
        self.__values = {}
        # ... one list for each tag
        for tag in tags:
            self.__values[tag] = []
        # ... plus a list to save timestamps
        self.__values['time'] = []

        self.__http = None  # save the HTTP server PID to kill it later

        logger.info(
            'HMI%d - monitors: %s' % (
                self.__id, ', '.join(map(str, self.__tags))))

    def __del__(self):

        # kill the HMI (opened with Process)
        if(self.__process is not None):
            self.__process.join()

        # kill the HTTP server (opened with Popen)
        self.stop_http_server()

        logger.debug('Killed HMI%d and its webserver' % self.__id)

    def start_http_server(self, port=80):
        """Starts a simple http server on a choosen port.

        :port: integer defaults to 80
        """
        if(self.__http is None):
            cmd = "python -m SimpleHTTPServer %d" % port
            try:
                self.__http = Popen(cmd, shell=True, preexec_fn=setsid)
                logger.info(
                    'HMI%d - HTTP server started on port %d' % (
                        self.__id, port))

            except OSError, e:
                emsg = repr(e)
                logger.warning(
                    'HMI%d - HTTP server cannot start: %s' % (
                        self.__id, emsg))

    def stop_http_server(self):
        """Kills the HTTP server."""
        if(self.__http is not None):
            killpg(getpgid(self.__http.pid), SIGTERM)
            logger.info('HMI%d - HTTP server stopped' % self.__id)
            self.__http = None

    def mplot(self):
        """Callback.

        Writes the three subplots in the .png file using the
        Matplotlib canvas backend.
        """

        # reference to the eaxis formatter object
        # formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)

        # number of subplots
        n = len(self.__tags)

        if len(self.__values['time']) > DISPLAYED_SAMPLES:
            x = self.__values['time'][-DISPLAYED_SAMPLES:]
        else:
            x = self.__values['time']

        # create len(self.__tags) subplots, sharing the x axis
        fig, subplots = plt.subplots(n, 1, sharex=True, sharey=False)

        # set figure title
        subplots[0].set_title('HMI%d Monitor' % self.__id)

        # set common x axis
        subplots[n - 1].set_xticks(x)
        for tick in subplots[n - 1].get_xticklabels():
                tick.set_rotation(90)
        subplots[n - 1].set_xlabel('Time')

        # set y_label and plot data
        for i in range(0, n):
            subplots[i].set_ylabel(self.__tags[i])
            subplots[i].grid('on')
            if len(self.__values[self.__tags[i]]) > DISPLAYED_SAMPLES:
                y = self.__values[self.__tags[i]][-DISPLAYED_SAMPLES:]
            else:
                y = self.__values[self.__tags[i]]

            subplots[i].scatter(x, y, color='r')

        # convert a fig to a canvans
        canvas = FigureCanvas(fig)
        canvas.print_figure('examples/swat/hmi/%s' % self.__filename)

        plt.close(fig)

    def action_wrapper(self):
        """Wraps the action() method."""
        self.__start_time = time()
        while(time() - self.__start_time < self.__timeout):
            try:
                self.action()
                sleep(self.__timer)

            except Exception, e:
                print repr(e)
                sys.exit(1)

    def action(self):
        """Defines the action of the HMI:

        - reads the tags using the cpppo helper function
        - add them to different lists
        - appends the time value to another list
        - calls the mplot function
        """

        for index in self.__tags:
            tag = read_cpppo(
                self.__ipaddr, index,
                'examples/swat/hmi_cpppo.cache')
            logger.debug('HMI%d read %s: %s' % (self.__id, index, tag))
            tag = float(tag)
            self.__values[index].append(tag)

        self.__values['time'].append(time() - self.__start_time)
        logger.debug(
            "HMI%d - self.__values['time']: %f" % (
                self.__id,
                self.__values['time'][-1]))

        self.mplot()

    def start(self):
        """Runs the action() method."""
        self.__process = Process(target=self.action_wrapper)
        self.__process.start()


if __name__ == '__main__':
    """
    The values are displayed in real-time in a pop-up window and the same
    image is served through a webserver that can be reached at
    HMI_IP:80
    """
    hmi = HMI(
        ['HMI_MV101-Status', 'HMI_LIT101-Pv', 'HMI_P101-Status'],
        L1_PLCS_IP['plc1'], 'plc1.png', T_HMI_R, TIMEOUT)
    sleep(3)

    hmi.start()
    hmi.start_http_server(80)
    hmi.stop_http_server()
