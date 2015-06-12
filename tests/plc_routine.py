#!/usr/bin/python

from time import sleep
import sys
import os
from RepeatedTimer import RepeatedTimer # to change with a while(sleep(x)) ?

def pump_action(action, flow_lvl, hh_lvl, ll_lvl):
    if flow_lvl <= hh_lvl:
        return 1
    elif flow_lvl >= hh_lvl:
        return 0
    else:
        return action
    
def sensor_next_value(sensor_file):
    line = sensor_file.readline()
    if not line:
        return -1
    else:
        return float(line.rstrip('\n\r'))

def sensor_action_wrapper(sensor_file, action_file, action, hh_lvl, ll_lvl, tag1, tag2, ipaddr, logfile, rt):
    flow_lvl = sensor_next_value(sensor_file)
    if flow_lvl == -1:
        rt.stop()
    else:
        action = pump_action(action, flow_lvl, hh_lvl, ll_lvl)
        action_file.write(str(action))
        tags_string1 = "%s=%3.2f" % (
            tag1,
            flow_lvl)
        os.system("python -m cpppo.server.enip.client -vv -l %s -a %s %s" % (logfile, ipaddr, tags_string1))
        tags_string2 = "%s=%d" % (
            tag2,
            action)
        os.system("python -m cpppo.server.enip.client -vv -l %s -a %s %s" % (logfile, ipaddr, tags_string2))

        
def plc_routine(sensor_file_name, action_file_name, timeout, timer, hh_lvl, ll_lvl, tag1, tag2, ipaddr, logfile):
    sensor_file = open(sensor_file_name, 'r')
    action_file = open(action_file_name, 'w')

    action = 0
    rt = None
    
    rt = RepeatedTimer(timer, sensor_action_wrapper, sensor_file, action_file, action, hh_lvl, ll_lvl, tag1, tag2, ipaddr, logfile, rt)

    try:
        sleep(timeout)
    finally:
        rt.stop()

    action_file.close()
    sensor_file.close()

def main():
    if len(sys.argv) == 11:
        plc_routine(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])

if __name__ == '__main__':
    main()
