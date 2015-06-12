#!/usr/bin/python

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

import sys
import subprocess
from time import sleep
from time import time
import re

def parse(string):
    """
    regular expression which parses the floats or the integers in an input string
    and return them as a list
    """
    return re.findall(r'\d+(?:\.\d+)?', string)

def hmi_action(tag1, tag2, ipaddr, flow_axis, pump_axis, x_axis):
    """
    the action the hmi does every timer seconds : queries for the flow and pump tag values
    and add them in the set of values to display them in a graph
    """
    # query for the first tag value
    proc = subprocess.Popen(["python -m cpppo.server.enip.client -p -a %s %s" % (ipaddr, tag1)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    # parse the output of the subprocess
    flow = parse(str(out))

    # query for the second tag value
    proc = subprocess.Popen(["python -m cpppo.server.enip.client -p -a %s %s" % (ipaddr, tag2)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    # parse the output of the subprocess
    pump = parse(str(out))

    # append the values in the set
    flow_axis.append(flow[1]) # take the second, as the first is the x from flowx
    pump_axis.append(pump[1]) # take the second, as the first is the x from pumpx
    x_axis.append(time())

def hmi_routine(timeout, timer, tag1, tag2, ipaddr, save_file_name):
    """
    the routine called by the main function, in order to execute the
    action every timer second during timeout seconds, and to create the graphs
    """
    # empty lists
    flow_axis = []
    pump_axis = []
    x_axis = []

    start_time = time()
    while(time() - start_time < timeout):
        sleep(timer)
        hmi_action(tag1, tag2, ipaddr, flow_axis, pump_axis, x_axis)
        
    # computes and saves the graph
    plt.figure(1)
    plt.subplot(211)
    plt.xlabel('Time (s)')
    plt.ylabel('Flow level (cm)')
    plt.plot(x_axis, flow_axis, 'bo')

    plt.subplot(212)
    plt.xlabel('Time (s)')
    plt.ylabel('Pump action')
    plt.ylim([-0.5, 1.5])
    plt.plot(x_axis, pump_axis, 'r')
    plt.savefig(save_file_name, bbox_inches='tight')
 
def main():
    if len(sys.argv) == 7:
        hmi_routine(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

if __name__ == '__main__':
    main()
