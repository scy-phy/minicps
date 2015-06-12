#!/usr/bin/python

import random

nb_values = 100000
sensor_file = open("plc1/plc1_sensor.txt", 'w')
start = 5.0
delta = 5.0
hh_lvl = 1500.0
ll_lvl = 500.0
value = 50.0

increase = True
for i in range(nb_values):
    nb = random.uniform(start-delta, start+delta)
    if(increase and (nb < hh_lvl)):
        start += value
    elif(nb > hh_lvl):
        increase = False
        start -= value
    elif((not increase) and (nb > ll_lvl)):
        start -= 20
    elif(nb < ll_lvl):
        increase = True
        start += value
    sensor_file.write("{:3.2f}\n".format(nb))

sensor_file.close()
