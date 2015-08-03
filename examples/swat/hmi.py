from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from time import time
from time import sleep
from subprocess import Popen
from os import setsid
from constants import logger
from constants import P1_PLC1_TAGS, LIT_101, LIT_301, FIT_201, PLC_NUMBER, TIMER, TIMEOUT
from constants import read_cpppo
from constants import L1_PLCS_IP

def start_http_server(port):
    """
    Starts a simple http server on a choosen port
    """
    cmd = "python -m SimpleHTTPServer %d" % port
    return Popen(cmd, shell=True, preexec_fn=setsid)

def callback(time, flow, valve, pump, file):
    # Three subplots sharing x axe
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

    # fig = Figure()
    canvas = FigureCanvas(fig)

    # The pump has only two values 0 and 1
    # ax2.set_ylim([-0.5, 1.5])
    # ax3.set_ylim([-0.5, 1.5])
    ax3.set_xlabel('Time (s)')
    ax1.set_ylabel('Flow level (cm)')
    ax2.set_ylabel('Valve')
    ax3.set_ylabel('Pump')

    ax1.set_title('Flow level and pumps reactions')
    ax1.scatter(time, flow, color='b')
    ax2.plot(time, pump, color='g')
    ax3.plot(time, valve, color='r')
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    fig.subplots_adjust(hspace=0)

    canvas.print_figure('examples/swat/hmi/%s' % file)


if __name__ == '__main__':
    """
    Init cpppo enip server.

    Execute an infinite routine loop
        - bla
        - bla
    """

    sleep(4)

    # start_http_server(80)
    values = {}
    values['time'] = []

    start_time = time()
    while(time() - start_time < TIMEOUT):
        for i in range (1, 2): #PLC_NUMBER
            key = 'plc%d' % i
            if not key in values:
                values[key] = [[], [], []]
            flow = read_cpppo(L1_PLCS_IP[key], 'HMI_LIT101-Pv', 'examples/swat/hmi_cpppo.cache')
            (values[key])[0].append(flow)
            pump = read_cpppo(L1_PLCS_IP[key], 'HMI_P101-Status', 'examples/swat/hmi_cpppo.cache')
            values[key][1].append(pump)
            valve = read_cpppo(L1_PLCS_IP[key], 'HMI_MV101-Status', 'examples/swat/hmi_cpppo.cache')
            values[key][2].append(valve)
            if i == 1:
                values['time'].append(time())

            callback(values['time'], values[key][0], values[key][1], values[key][2], '%s.png' % key)

            sleep(TIMER)
