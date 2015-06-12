#!/usr/bin/python

from time import sleep
from time import time
import os
import sys

epsilon = sys.float_info.epsilon

def pump_action(action, flow_lvl, hh_lvl, ll_lvl):
    """
    defines the behavior of the pump, when the water flow is normal or too high
    """
    if flow_lvl - hh_lvl < epsilon:
        return 1
    elif flow_lvl - hh_lvl > epsilon:
        return 0
    else:
        return action
    
def sensor_next_value(sensor_file):
    """
    read a line of the sensor file and return the float read
    """
    line = sensor_file.readline()
    if not line:
        return -1
    else:
        return float(line.rstrip('\n\r'))

def sensor_action_wrapper(sensor_file, action_file, action, hh_lvl, ll_lvl, tag1, tag2, ipaddr, logfile):
    """
    defines the action executed by the plc each timer seconds:
    -reads the current flow value
    -decides if it opens or closes the pump
    -writes its decision into the action file
    -updates the flow and pump values on the enip server
    """
    flow_lvl = sensor_next_value(sensor_file)
    if flow_lvl != -1:
        action = pump_action(action, flow_lvl, hh_lvl, ll_lvl)
        action_file.write(str(action))
        tags_string1 = "%s=%3.2f" % (
            tag1,
            flow_lvl)
        # updates the flow and pump values on the cpppo server with a cpppo write order
        os.system("python -m cpppo.server.enip.client -v -l %s -a %s %s" % (logfile, ipaddr, tags_string1))
        tags_string2 = "%s=%d" % (
            tag2,
            action)
        os.system("python -m cpppo.server.enip.client -v -l %s -a %s %s" % (logfile, ipaddr, tags_string2))
        
def plc_routine(sensor_file_name, action_file_name, timeout, timer, hh_lvl, ll_lvl, tag1, tag2, ipaddr, logfile):
    """
    the routine called by the main function, in order to execute the
    action every timer second during timeout seconds
    """
    sensor_file = open(sensor_file_name, 'r')
    action_file = open(action_file_name, 'w')

    action = 0

    start_time = time()
    while(time() - start_time < timeout):
        sleep(timer)
        sensor_action_wrapper(sensor_file, action_file, action, hh_lvl, ll_lvl, tag1, tag2, ipaddr, logfile)

    action_file.close()
    sensor_file.close()

def main():
    if len(sys.argv) == 11:
        plc_routine(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])

if __name__ == '__main__':
    main()
