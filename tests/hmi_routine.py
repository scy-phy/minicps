#!/usr/bin/python

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

import sys
import subprocess
from time import sleep
from time import time
import re
from RepeatedTimer import RepeatedTimer

def parse(string):
    return re.findall(r'\d+(?:\.\d+)?', string)

def hmi_action(tag1, tag2, ipaddr, flow_axis, pump_axis, x_axis):
    proc = subprocess.Popen(["python -m cpppo.server.enip.client -p -a %s %s" % (ipaddr, tag1)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    flow = parse(str(out))
    
    proc = subprocess.Popen(["python -m cpppo.server.enip.client -p -a %s %s" % (ipaddr, tag2)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    pump = parse(str(out))

    flow_axis.append(flow[0])
    pump_axis.append(pump[0])
    x_axis.append(time())

def hmi_routine(timeout, timer, tag1, tag2, ipaddr, save_file_name):
    flow_axis = []
    pump_axis = []
    x_axis = []

    rt = RepeatedTimer(timer, hmi_action, tag1, tag2, ipaddr, flow_axis, pump_axis, x_axis)
    try:
        sleep(timeout)
    finally:
        rt.stop()

    plt.plot(flow_axis)
    plt.savefig(save_file_name, bbox_inches='tight')
 
def main():
    if len(sys.argv) == 7:
        hmi_routine(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

if __name__ == '__main__':
    main()
