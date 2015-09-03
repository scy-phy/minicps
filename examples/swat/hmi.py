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
class HMI:
    """
    Class defining the Human-Machine Interface
    An HMI object has to query 3 tags from a PLC address, and log it into a .svg
    file. This .svg file is also available in a webserver started by the HMI.
    tag1-3: the ENIP tag to query
    ipaddr: the IP address of thr PLC to query
    filename: the name of the .svg file
    timer: period in which the HMI has to query the tags (s)
    timeout: period of activity (s)
    """

    """
    Class variables
    """
    HMI_id = 1

    def __init__(self, tag1, tag2, tag3, ipaddr, filename, timer, timeout):
        """
        constructor
        """
        self.__tag1 = tag1
        self.__tag2 = tag2
        self.__tag3 = tag3
        self.__ipaddr = ipaddr
        self.__id = HMI.HMI_id
        HMI.HMI_id += 1
        self.__file = filename
        self.__timer = timer
        self.__timeout = timeout
        self.__process = None
        self.__values = {}
        self.__values[tag1] = []
        self.__values[tag2] = []
        self.__values[tag3] = []
        self.__values['time'] = []
        self.__HMI_http = None
        logger.info('Created HMI %d that will monitor %s %s %s tags' % (self.__id, self.__tag1, self.__tag2, self.__tag3))

    def __del__(self):
        """
        destructor
        """
        if(self.__process is not None):
            self.__process.join()
        if(self.__HMI_http is not None):
            kill(self.__HMI_http, SIGKILL)
        logger.info('HMI %d removed' % self.__id)

    def start_http_server(self, port):
        """
        Starts a simple http server on a choosen port
        """
        if(self.__HMI_http is None):
            cmd = "python -m SimpleHTTPServer %d" % port
            self.__HMI_http = Popen(cmd, shell=True, preexec_fn=setsid)
            # FIXME: check if webserver is running before returning
            logger.info('HMI %d - HTTP server started' % self.__id)

    def stop_http_server(self):
        """
        Kills the HTTP server
        """
        if(self.__HMI_http is not None):
            killpg(self.__HMI_http, SIGTERM)
            logger.info('HMI %d - HTTP server stopped' % self.__id)

    def callback(self):
        """
        Callback method, writes the three subplots in the .svg file using the
        Matplotlib canvas backend.
        """
        # Three subplots sharing x axe
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
        canvas = FigureCanvas(fig)
        mini = min(self.__values[self.__tag1])
        maxi = max(self.__values[self.__tag1])
        if(mini != maxi):
            delta = 5*(maxi - mini)/100 # 5%
            ax1.set_ylim([mini - delta, maxi + delta])
        mini = min(self.__values[self.__tag2])
        maxi = max(self.__values[self.__tag2])
        if(mini != maxi):
            delta = 5*(maxi - mini)/100 # 5%
            ax2.set_ylim([mini - delta, maxi + delta])

        mini = min(self.__values[self.__tag3])
        maxi = max(self.__values[self.__tag3])
        if(mini != maxi):
            delta = 5*(maxi - mini)/100 # 5%
            ax3.set_ylim([mini - delta, maxi + delta])

        ax3.set_xlabel('Time (s)')
        ax1.set_ylabel(self.__tag1)
        ax2.set_ylabel(self.__tag2)
        ax3.set_ylabel(self.__tag3)
        ax1.set_title('HMI %d' % self.__id)
        ax1.plot(self.__values['time'], self.__values[self.__tag1], color='g')
        ax2.scatter(self.__values['time'], self.__values[self.__tag2], color='b')
        ax3.plot(self.__values['time'], self.__values[self.__tag3], color='r')
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
            try:
                self.action()
                sleep(self.__timer)
            except Exception:
                break

    def action(self):
        """
        Defines the action action of the HMI:
        -reads the three tags using the cpppo helper function
        and add them to three different lists
        -append the time value to another list
        -calls the callback function
        """
        try: 
            tag1 = read_cpppo(self.__ipaddr, self.__tag1, 'examples/swat/hmi_cpppo.cache')
            logger.debug('HMI %d read %s: %s' % (self.__id, self.__tag1, tag1))
            tag1 = int(tag1)
            self.__values[self.__tag1].append(tag1)

            tag2 = read_cpppo(self.__ipaddr, self.__tag2, 'examples/swat/hmi_cpppo.cache')
            logger.debug('HMI %d read %s: %s' % (self.__id, self.__tag2, tag2))
            tag2 = float(tag2)
            self.__values[self.__tag2].append(tag2)

            tag3 = read_cpppo(self.__ipaddr, self.__tag3, 'examples/swat/hmi_cpppo.cache')
            logger.debug('HMI %d read %s: %s' % (self.__id, self.__tag3, tag3))
            tag3 = int(tag3)
            self.__values[self.__tag3].append(tag3)
            self.__values['time'].append(time())

            self.callback()

        except Exception, e:
            emsg = repr(e)
            logger.warning(emsg)
            raise Exception


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
    hmi1 = HMI( 'HMI_MV101-Status', 'HMI_LIT101-Pv', 'HMI_P101-Status', L1_PLCS_IP['plc1'], 'plc1.png', TIMER, TIMEOUT)
    hmi1.start_http_server(80)
    sleep(3)
    hmi1.start()
    # hmi1.stop_http_server()
